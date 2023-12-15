from flask import Blueprint, request, jsonify, session, request
from datetime import datetime
import logging
import jsonschema
from app.extensions import flask_bcrypt, db, limiter
from app.account.schemas import sign_up_schema, log_in_schema
from app.account.helpers import is_good_password
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper
from app.utils.log_event_utils.helpers import log_event
from app.utils.detect_html.detect_html import check_for_html
from app.models.user import User

account = Blueprint("account", __name__)

# SIGN UP
@account.route("/signup", methods=["POST"])
@limiter.limit("20/day")
def signup_user():
    """
    signup_user() -> JsonType
    ----------------------------------------------------------
    Route with no parameters.
    Sets a session cookie in response.
    Returns Json object containing strings.
    "response" value is always included.  
    "user" value only included if response is "success".
    ----------------------------------------------------------
    Response example:
    response_data = {
            "response":"success",
            "user": {
                "id": "16fd2706-8baf-433b-82eb-8c7fada847da", 
                "name": "John", 
                "email": "john@email.com"}, 
        } 
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    name = json_data["name"]
    email = json_data["email"]
    password = json_data["password"]

    # Get the client's IP address - if html is found in input, ip address will be logged
    client_ip = request.remote_addr

    # Check for html in user input
    html_in_name = check_for_html(name, "signup - name field", client_ip)
    html_in_email = check_for_html(email, "signup - email field", client_ip)

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=json_data, schema=sign_up_schema)
    except jsonschema.exceptions.ValidationError as e:
        logging.info(f"Jsonschema validation error. Input name: {name} Input email: {email}")
        log_event("LOG_EVENT_SIGNUP", "LES_02")
        return jsonify({"response": "Invalid JSON data.", "error": str(e)}), 400

    # Check if user already exists
    user_exists = User.query.filter_by(_email=email).first() is not None
    if user_exists:
        user = User.query.filter_by(_email=email).first()
        logging.info(f"User already in db: {user.email}")
        log_event("LOG_EVENT_SIGNUP", "LES_03", user.uuid)
        return jsonify({"response":"user already exists"}), 409
    
    # Check if password meets safe password criteria
    if not is_good_password(password):
        logging.info("Weak password provided.")
        log_event("LOG_EVENT_SIGNUP", "LES_04")
        return jsonify({"response": "Weak password."}), 400

    # Not to use same pepper for every user, pepper array has 6 values, and pepper will rotate according to the month the user created the account. If pepper array does not contain 6 values, this will fail. Make sure pepper array is setup correctly in env file.
    date = datetime.utcnow()
    salt = generate_salt()
    pepper = get_pepper(date)
    salted_password = salt + password + pepper

    #create user
    try:
        hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode("utf-8")
        new_user = User(name=name, email=email, password=hashed_password, salt=salt, created_at=date)
        db.session.add(new_user)
        db.session.commit()
        the_session = new_user.session

    except Exception as e:
        logging.error(f"User registration failed. Returned 500. Error: {e}")
        try:
            log_event("LOG_EVENT_SIGNUP", "LES_05")
        except Exception as e:
            logging.error(f"Log event error. Error: {e}")
        return jsonify({"response": "There was an error registering user", "error": str(e)}), 500
    
    # create session
    session["session_id"] = the_session

    # log event and system
    logging.info(f"New user created.")
    log_event("LOG_EVENT_SIGNUP", "LES_01", new_user.uuid)
    if html_in_name or html_in_email:
        log_event("LOG_EVENT_SIGNUP", "LES_06", new_user.uuid)
    
    response_data ={
            "response":"success",
            "user": {
                "id": new_user.uuid, 
                "name": new_user.name, 
                "email": new_user.email},
        }
    return jsonify(response_data)

# Log IN
@account.route("/login", methods=["POST"])
def login_user():
    """
    login_user() -> JsonType
    ----------------------------------------------------------
    Route with no parameters.
    Sets a session cookie in response.
    Returns Json object containing strings.
    "response" value is always included.  
    "user" value only included if response is "success".
    ----------------------------------------------------------
    Response example:
    response_data = {
            "response":"success",
            "user": {
                "id": "16fd2706-8baf-433b-82eb-8c7fada847da", 
                "name": "John", 
                "email": "john@email.com"}, 
        } 
    """
    # Get the JSON data from the request body 
    json_data = request.get_json()
    email = json_data["email"]
    password = json_data["password"]

    # Get the client's IP address - if html is found in input, ip address will be logged
    client_ip = request.remote_addr

    # Check for html in user input
    html_in_email = check_for_html(email, "login - email field", client_ip)

    # validate Json against the schema
    try:
        jsonschema.validate(instance=json_data, schema=log_in_schema)
    except jsonschema.exceptions.ValidationError as e:
        logging.info(f"Jsonschema validation error. Input email: {json_data["email"]}")
        try:
            log_event("LOG_EVENT_LOGIN", "LEL_02")
        except Exception as e:
            logging.error(f"Failed to log event. Error: {e}")
        return jsonify({"response": "Invalid JSON data.", "error": str(e)}), 400

    # Check if user exists
    user = User.query.filter_by(_email=email).first()

    if user is None:
        logging.info(f"User not in DB. Input email: {email}")
        try:
            log_event("LOG_EVENT_LOGIN", "LEL_03")
        except Exception as e:
            logging.error(f"Failed to log event. Error: {e}")
        return jsonify({"response":"unauthorized"}), 401
    
    # Check if the user was blocked by an admin
    if user.has_access_blocked():
        logging.info(f"User blocked. Input email: {email}")
        try:
            log_event("LOG_EVENT_LOGIN", "LEL_04", user.uuid)
        except Exception as e:
            logging.error(f"Failed to log event. Error: {e}")
        return jsonify({"response": "blocked"}), 401
    
    # Check if the user is temporarily blocked from logging in due to mistyping password > 3x
    if user.is_login_blocked():
        remaining_time = max(0, round((user.login_blocked_until - datetime.utcnow()).total_seconds() / 60))
        if user.login_attempts < 4:
            logging.info(f"User temporarily blocked. Input email: {email}. Failed login attemps: {user.login_attempts}")
            try:
                log_event("LOG_EVENT_LOGIN", "LEL_07", user.uuid)
            except Exception as e:
                logging.error(f"Failed to log event. Error: {e}")
        else:
            logging.warn(f"User temporarily blocked. Input email: {email}. Failed login attemps: {user.login_attempts}")
            try:
                log_event("LOG_EVENT_LOGIN", "LEL_06", user.uuid)
            except Exception as e:
                logging.error(f"Failed to log event. Error: {e}")
        
        return jsonify({f"response": "temporarily blocked for {remaining_time} minutes"}), 401
    
    # Add salt and pepper to password and check if matches with db
    pepper = get_pepper(user.created_at) 
    salted_password = user.salt + password + pepper

    if not flask_bcrypt.check_password_hash(user.password, salted_password):
        logging.info(f"Wrong password input.")
        # Increment login attempts and block if necessary
        try:
            user.increment_login_attempts()
            db.session.commit()
        except Exception as e:
            logging.error(f"Login attempt counter could not be incremented, function will continue. Error: {e}")
        # Check if the user is now blocked
        if user.is_login_blocked():
            remaining_time = max(0, round((user.login_blocked_until - datetime.utcnow()).total_seconds() / 60))
            return jsonify({f"response": "temporarily blocked for {remaining_time} minutes"}), 401
        return jsonify({"response":"unauthorized"}), 401
    
    # Reset login attempts counter upon successful login, set last seen, & create session
    try:
        user.reset_login_attempts()
        user._last_seen = datetime.utcnow()
        new_session = user.new_session()
        db.session.commit()
    except Exception as e:
        logging.error(f"Login attempt counter could not be reset, function will continue. Error: {e}")

    session["session_id"] = new_session

    # event and system logs
    logging.info("A user logged in.")
    try:
        log_event("LOG_EVENT_LOGIN", "LEL_01", user.uuid)
        if html_in_email:
            log_event("LOG_EVENT_LOGIN", "LEL_08", user.uuid)
    except Exception as e:
        logging.error(f"Failed to create event log. Error: {e}")
    
    response_data ={
            "response":"success",
            "user": {
                "id": user.uuid, 
                "name": user.name, 
                "email": user.email}, 
        }
    return jsonify(response_data)

# Log OUT
@account.route("/logout", methods=["POST"])
def logout_user():
    session_id = session.get("session_id")
    if not session_id:
        return jsonify({"response":"unauthorized"}), 401
    # Check if user exists
    try:
        user = User.query.filter_by(_session=session_id).first()
        if user is None:
            logging.error(f"Session_id did not match any user. Session_id: {session_id} Error: {e}")
        else:
            user.end_session()
            db.commit()
    except Exception as e:
        logging.error(f"Failed to erase session in db. Error: {e}")
    
    session.pop("session_id", None)
    logging.info(f"Successful logout") 
    return jsonify({"response":"success"}), 200

# get current user
@account.route("/@me")
def get_current_user():
    session_id = session.get("session_id")
    if not session_id:
        return jsonify({"response":"unauthorized"}), 401
    
    user = User.query.filter_by(_uuid = session_id).first()

    if user is None:
        logging.error(f"Session id does not match user: {session_id}")
        return jsonify({"response":"unauthorized"}), 401

    response_data ={
            "response":"success",
            "user": {
                "id": user.uuid, 
                "name": user.name, 
                "email": user.email},
        }
    return jsonify(response_data)