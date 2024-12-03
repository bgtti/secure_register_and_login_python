"""
**ABOUT THIS FILE**

auth/routes_main.py contains routes responsible for core authentication and authorization functionalities.
Here you will find the following routes:
- **signup** route
- **login** route
- **logout** route
- **@me** route (delivers user information given session cookie)

The format of data sent by the client is validated using Json Schema. 
Reoutes receiving client data are decorated with `@validate_schema(name_of_schema)` for this purpose. 

------------------------
## More information

This app relies on Flask-Login (see `app/extensions`) to handle authentication. It provides user session management, allowing us to track user logins, manage sessions, and protect routes.

Checkout the docs for more information about how Flask-Login works: https://flask-login.readthedocs.io/en/latest/#configuring-your-application

"""
import logging
from flask import Blueprint, request, jsonify, session
from flask_login import login_user as flask_login_user, current_user, logout_user as flask_logout_user, login_required
from datetime import datetime, timezone
from app.extensions.extensions import flask_bcrypt, db, limiter, login_manager
from app.models.user import User
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper
from app.utils.log_event_utils.log import log_event
from app.utils.detect_html.detect_html import check_for_html
from app.utils.profanity_check.profanity_check import has_profanity
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.ip_utils.ip_geolocation import geolocate_ip 
from app.utils.ip_utils.ip_anonymization import anonymize_ip
from app.utils.bot_detection.bot_detection import bot_caught
from app.routes.auth.schemas import signup_schema, login_schema
from app.routes.auth.auth_helpers import reset_user_session, get_hashed_pw, is_good_password
from . import auth

# SIGN UP
@auth.route("/signup", methods=["POST"])
@limiter.limit("2/minute;5/day")
@validate_schema(signup_schema)
def signup_user():
    """
    signup_user() -> JsonType
    ----------------------------------------------------------

    Route registers a new user.
    
    Requires json data from the client. 
    Sets a session cookie in response.
    Returns Json object containing strings:
    - "response" value is always included.  
    - "user" value only included if response is "success".

    ----------------------------------------------------------
    **Response example:**
    ```python
        response_data = {
                "response":"success",
                "user": {
                    "access": "user"
                    "name": "John", 
                    "email": "john@email.com"}, 
            } 
    ```
    ----------------------------------------------------------
    **About errors:**

    Error messages sent to the front-end are ambiguous by design. Check the logs to understand the error.
    The password validation and 'user exists' will both return the same error response.
    The reason for this is to pass ambiguity to the front end so as not to give a malicious actor information about whether a certain email address is or not registered with the website.
    """
    # Standard error response
    error_response = {"response": "There was an error registering user."}

    # Get the JSON data from the request body
    json_data = request.get_json()
    name = json_data["name"]
    email = json_data["email"]
    password = json_data["password"]
    honeypot = json_data["honeypot"]

    if len(honeypot) > 0:
        bot_caught(request, "signup")
        return jsonify(error_response), 418

    # Check if user already exists 
    try:
        user_exists = User.query.filter_by(email=email).first() is not None 
    except Exception as e:
        logging.error(f"Could not check if user exists in db: {e}")

    if user_exists:
        user = User.query.filter_by(email=email).first()
        logging.info(f"User already in db (error 409 in reality): {user.email}")
        try:
            log_event("ACCOUNT_SIGNUP", "user exists", user.id)
        except Exception as e:
            logging.error(f"Could not log event in signup: {e}")
    
    # Check if password meets safe password criteria, salt and pepper password, then hash it
    date = datetime.now(timezone.utc) # date is required to get apropriate Pepper value
    salt = generate_salt()
    hashed_password = get_hashed_pw(password, date, salt) # will be null if password does not meet criteria
    
    # Determine if the new user should be flagged on the base of possible html or profanity in input (so admin could check). Flag colours described in enum in user's model page.
    flag = False

    html_in_name = check_for_html(name, "signup - name field", email)
    html_in_email = check_for_html(email, "signup - email field", email)

    if html_in_email or html_in_name:
        flag = "YELLOW"
    else:
        profanity_in_name = has_profanity(name) 
        profanity_in_email = has_profanity(email)
        if profanity_in_name or profanity_in_email:
            flag = "PURPLE"
    
    # Return if: user already exists or hashed_password is Null
    # Note we ran most of the function before returning. The reason is to diminish the response time discrepancy between a successfully created user and a failed response. The difference in response time can be used by bad actors to deduce whether an account exists or not in the system.
    
    if user_exists or not hashed_password:
        return jsonify({"response": "There was an error registering user."}), 400 

    # Create user
    try:
        # hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode("utf-8")
        new_user = User(name=name, email=email, password=hashed_password, salt=salt, created_at=date) # passing on the creation date to make sure it is the same used for pepper
        db.session.add(new_user)
        if flag:
            new_user.flag_change(flag)
        new_user.new_session() # an alternative id should be created to be used in session management
        db.session.commit()

    except Exception as e:
        logging.error(f"User registration failed. Error: {e}")
        try:
            log_event("ACCOUNT_SIGNUP", "signup failed")
        except Exception as e:
            logging.error(f"Log event error. Error: {e}")
        return jsonify(error_response), 500

    # Log event to user and system logs
    try:
        logging.info(f"New user created.")
        log_event("ACCOUNT_SIGNUP", "signup successful", new_user.id)

        if flag:
            if html_in_name or html_in_email:
                log_event("ACCOUNT_SIGNUP", "html detected", new_user.id)
            else:
                log_event("ACCOUNT_SIGNUP", "profanity", new_user.id)
    except Exception as e:
        logging.error(f"Log event error. Error: {e}")

    # Use Flask-Login to log in the user
    flask_login_user(new_user)

    # Note we are not encoding user input when sending to FE because the FE is built with React with JSX
    # JSX auto-escapes the data before putting it into the page, so deemed escaping to be unecessary.

    # POSSIBLE IMPLEMENTATION:
    # - Consider 2-factor authentication mandatory for admins
    # - Send an email to the user in case of 409 (user already exists).

    response_data ={
            "response":"success",
            "user": {
                "access": new_user.access_level.value, 
                "name": new_user.name, 
                "email": new_user.email},
        }
    return jsonify(response_data)

# LOG IN
@auth.route("/login", methods=["POST"])
@limiter.limit("30/minute;50/day")
@validate_schema(login_schema)
def login_user():
    """
    login_user() -> JsonType
    ----------------------------------------------------------

    Route logs-in a user.
    
    Requires json data from the client. 
    Sets a session cookie in response.
    Returns Json object containing strings:
    - "response" value is always included.  
    - "user" value only included if response is "success".

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "user": {
                    "name": "John", 
                    "email": "john@email.com",
                    "access": "user"
                    }, 
            }
    ``` 
    ----------------------------------------------------------
    **About errors:**

    Error messages sent to the front-end are ambiguous by design. Check the logs to understand the error.
    The blocked and failed credentials will all return the same error response.
    The reason for this is to pass ambiguity to the front end so as not to give a malicious actor information about whether a certain email address is or not registered with the website.
    """
    # Standard error response
    error_response = {"response": "There was an error logging in user."} 

    # Get the JSON data from the request body 
    json_data = request.get_json()
    email = json_data["email"]
    password = json_data["password"]
    honeypot = json_data["honeypot"]

    if len(honeypot) > 0:
        bot_caught(request, "signup")
        return jsonify(error_response), 418

    # Check if user exists
    invalid_credentials = False
    
    try:
        user = User.query.filter_by(email=email).first()
    except Exception as e:
        logging.error(f"Failed to access db. Error: {e}")

    if user is None:
        invalid_credentials = True
        logging.info(f"User not in DB. Input email: {email}.")
        try:
            log_event("ACCOUNT_LOGIN", "user not found")
        except Exception as e:
            logging.error(f"Failed to log event. Error: {e}")

    # Check if the user was blocked by an admin
    if not invalid_credentials and user.has_access_blocked():
        logging.info(f"User blocked. Input email: {email}. (typically error code: 403)")
        try:
            log_event("ACCOUNT_LOGIN", "user blocked", user.id)
        except Exception as e:
            logging.error(f"Failed to log event. Error: {e}")
        invalid_credentials = True

    # Check if the user is temporarily blocked from logging in due to mistyping password > 3x
    if not invalid_credentials and user.is_login_blocked():
        if user.login_attempts < 6:
            logging.info(f"User temporarily blocked. Input email: {email}. Failed login attemps: {user.login_attempts}")
            try:
                log_event("ACCOUNT_LOGIN", "wrong credentials 3x", user.id)
            except Exception as e:
                logging.error(f"Failed to log event. Error: {e}")
        else:
            client_ip = get_client_ip(request)
            if client_ip:
                geolocation = geolocate_ip(client_ip) 
                anonymized_ip = anonymize_ip(client_ip)
                logging.warning(f"{user.login_attempts} wrong login attempts for email: {email}. From IP {anonymized_ip}. Geolocation: country = {geolocation["country"]}, city = {geolocation["city"]}. (typically error code: 403)")
            try:
                log_event("ACCOUNT_LOGIN", "wrong credentials 5x", user.id, f"Login attempt from IP {anonymized_ip}. Geolocation: country = {geolocation["country"]}, city = {geolocation["city"]}.")
            except Exception as e:
                logging.error(f"Failed to log event. Error: {e}")
        
        invalid_credentials = True

    if not invalid_credentials:
        # Add salt and pepper to password and check if matches with db
        pepper = get_pepper(user.created_at) 
        salted_password = user.salt + password + pepper

        if not flask_bcrypt.check_password_hash(user.password, salted_password):
            # Increment login attempts and block if necessary
            try:
                user.increment_login_attempts()
                db.session.commit()
            except Exception as e:
                logging.error(f"Login attempt counter could not be incremented, function will continue. Error: {e}")
            # Check if the user is now blocked
            if user.is_login_blocked():
                logging.info(f"Successive failed log-in attempts lead user to be temporarily blocked. {user.email}")
            invalid_credentials = True
    
    if invalid_credentials:
        return jsonify(error_response), 401
    # Reset login attempts counter upon successful login, set last seen, & create session
    try:
        user.reset_login_attempts()
        user._last_seen = datetime.now(timezone.utc)
        # new_session = user.new_session()
        db.session.commit()
    except Exception as e:
        logging.error(f"Login attempt counter could not be reset, function will continue. Error: {e}")

    # Check for html in user input
    html_in_email = check_for_html(email, "login - email field")
    try:
        log_event("ACCOUNT_LOGIN", "login successful", user.id)
        if html_in_email:
            log_event("ACCOUNT_LOGIN", "html detected", user.id, f"Email provided: {email}")
    except Exception as e:
        logging.error(f"Failed to create event log. Error: {e}")

    # TODO: consider the bellow if user does not want to be remembered:
    # user.new_session() 
    # db.session.commit()

    # Use Flask-Login to log in the user
    flask_login_user(user)

    # event and system logs
    logging.info("A user logged in.")
    # logging.debug(f"Session after login: {session}") # Uncomment to debug session

    # TODO POSSIBLE IMPLEMENTATION:
    # - Send an email to the user in case of user being blocked.
    
    response_data ={
            "response":"success",
            "user": {
                "access": user.access_level.value,
                "name": user.name, 
                "email": user.email}, 
        }
    return jsonify(response_data)

# LOG OUT
@auth.route("/logout", methods=["POST"])
@login_required
def logout_user():
    """
    logout_user() -> JsonType
    ----------------------------------------------------------

    Route logs out a user.
    
    Returns Json object if successfull.

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success"
            }
    ``` 
    """
    reset_user_session(current_user) # invalidate old auth sessions
    flask_logout_user() # classic flask-login log out
    logging.info(f"Successful logout") 
    return jsonify({"response":"success"})

# GET CURRENT USER FROM SESSION COOKIE
@auth.route("/@me")
@login_required
def get_current_user():
    """
    get_current_user() -> JsonType
    ----------------------------------------------------------

    Route re-logs a user in (using the session cookie). 
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "user" value only included if response is "success".

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "user": {
                    "name": "John", 
                    "email": "john@email.com",
                    "access": "user"
                    }, 
            }
    ``` 
    """

    user = current_user

    response_data ={
            "response":"success",
            "user": {
                "access": user.access_level.value, 
                "name": user.name, 
                "email": user.email},
        }
    return jsonify(response_data)