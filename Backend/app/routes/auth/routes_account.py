"""
**ABOUT THIS FILE**

auth/routes_account.py contains routes responsible for account management functionalities related to authentication.
Here you will find the following routes:
- **change_user_name** route
- **change_email** route #TODO
- **change_password** route #TODO
- **reset_password** route #TODO

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
from app.models.validation_token import ValidationToken
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper
from app.utils.log_event_utils.log import log_event
from app.utils.detect_html.detect_html import check_for_html
from app.utils.profanity_check.profanity_check import has_profanity
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.ip_utils.ip_geolocation import geolocate_ip 
from app.utils.ip_utils.ip_anonymization import anonymize_ip
from app.utils.bot_detection.bot_detection import bot_caught
from app.routes.auth.schemas import change_name_schema, auth_change_req_schema
from app.routes.auth.helpers import is_good_password, send_pw_change_email, send_email_change_emails, send_email_change_sucess_emails, send_pw_change_sucess_email
from . import auth

# CHAGE USER'S NAME
@auth.route("/change_user_name", methods=["POST"])
@login_required
@validate_schema(change_name_schema)
@limiter.limit("10/day")
def change_user_name(): # TODO --> Add to logs so user actions can show in history
    """
    change_user_name() -> JsonType
    ----------------------------------------------------------

    Route changes the name associated with the user's account. 
    
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
    # Standard error response
    error_response = {"response": "There was an error changing user's name."}

    # Get the JSON data from the request body
    json_data = request.get_json()
    new_name = json_data["new_name"]

    the_user = User.query.filter_by(email=current_user.email).first()
    old_name = the_user.name

    try:
        the_user.name = new_name
        db.session.commit()
        logging.info(f"User {current_user.email} name changed from {old_name} to {new_name}.")
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"User could not change name. Error: {e}")
        return jsonify(error_response), 500

    flag = False

    html_in_name = check_for_html(new_name, "auth - change_user_name", current_user.email)
    if html_in_name:
        flag = "YELLOW"
        the_user.flag_change(flag)
    else:
        profanity_in_name = has_profanity(new_name) 
        if profanity_in_name:
            flag = "PURPLE"
            the_user.flag_change(flag)
    
    if flag:
            the_user.flag_change(flag)
            db.session.commit()

    response_data ={
            "response":"success",
            "user": {
                "access": the_user.access_level.value, 
                "name": the_user.name, 
                "email": the_user.email},
        }
    return jsonify(response_data)

# REQUEST TO CHAGE USER'S  EMAIL OR PASSWORD (STEP 1)
@auth.route("/request_auth_change", methods=["POST"])
@login_required
@validate_schema(auth_change_req_schema)
@limiter.limit("5/day")
def change_user_email(): # TODO --> Add to logs so user actions can show in history
    """
    change_user_email() -> JsonType
    ----------------------------------------------------------

    Route changes the email associated with the user's account. # TODO
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "mail_sent" value only included if response is "success".

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "mail_sent": True, 
            }
    ``` 
    """
    # Standard error response
    error_response = {"response": "There was an error changing the user's credentials."}

    # Get the JSON data from the request body
    json_data = request.get_json()
    change_request_type = json_data["type"]
    user_agent = json_data.get("user_agent", "")

    client_ip = get_client_ip(request)

    user = User.query.filter_by(email=current_user.email).first()

    # Create verification token TODO

    try:
        token = ValidationToken(user_id=user.id, ip_address=client_ip, user_agent=user_agent) 
        db.session.add(token)
        db.session.commit()

    except Exception as e:
        logging.error(f"Token creation failed. Error: {e}")
        return jsonify(error_response), 500

    # Send token by email TODO: check helper function and add verification link
    if change_request_type == "password":
        mail_sent = send_pw_change_email(user.name, token.token, user.email)
    else:
        new_email = json_data["new_email"]
        if new_email is None:
            return jsonify(error_response), 400
        try:
            user.new_email = new_email
            db.session.add(token)
            db.session.commit()
        except Exception as e:
            logging.error(f"New email could not be added to user. Error: {e}")
            return jsonify(error_response), 500
        mail_sent = send_email_change_emails(user.name, token.token, token.new_email_token, new_email)

    
    # Log this event TODO

    # Log event to user and system logs
    # try:
    #     logging.info(f"Initiated auth credential change")
    #     log_event("ACCOUNT_....", "... successful", user.id)

    # except Exception as e:
    #     logging.error(f"Log event error. Error: {e}")

    response_data ={
            "response":"success",
            "mail_sent": mail_sent,
        }
    return jsonify(response_data)

@limiter.limit("5/day")
@auth.route('/confirm_email_change/<token>', methods=['GET'])
def confirm_email_change(token):
    """
    confirm_email_change() -> JsonType 
    ----------------------------------------------------------

    Route changes the email associated with the user's account. # TODO
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "mail_sent" value only included if response is "success".

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "mail_sent": True, 
            }
    ``` 
    """
    # Standard error response
    error_response = {"response": "Invalid or expired token."}

    the_token = ValidationToken.query.filter_by(token=token).first()

    if not the_token:
        return jsonify(error_response), 400
    
    validated = the_token.validate_token()

    if validated is False:
        return jsonify(error_response), 400
    
    user_may_change_email = the_token.user_may_change_email


    if user_may_change_email is False:
        response_data ={
            "response":"success",
            "cred_changed": False,
        }
        return jsonify(response_data), 200

    # Update the email 
    user = the_token.user
    new_email = user.new_email
    old_email = user.email
    user.change_email()
    db.session.delete(the_token)
    db.session.commit()

    # TODO: log event

    # Notify the old email
    email_sent = send_email_change_sucess_emails(user.name, old_email, new_email)

    response_data ={
            "response":"success",
            "cred_changed": True,
            "mail_sent": email_sent,
        }
    return jsonify(response_data)

@limiter.limit("5/day")
@auth.route('/confirm_new_email/<token>', methods=['GET'])
def confirm_new_email(token):
    """
    confirm_new_email() -> JsonType 
    ----------------------------------------------------------

    Route changes the email associated with the user's account. # TODO
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "mail_sent" value only included if response is "success".

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "mail_sent": True, 
            }
    ``` 
    """
    # Standard error response
    error_response = {"response": "Invalid or expired token."}

    the_token = ValidationToken.query.filter_by(new_email_token=token).first()

    if not the_token:
        return jsonify(error_response), 400
    
    validated = the_token.validate_email_token()

    if validated is False:
        return jsonify(error_response), 400
    
    user_may_change_email = the_token.user_may_change_email


    if user_may_change_email is False:
        response_data ={
            "response":"success",
            "cred_changed": False,
        }
        return jsonify(response_data), 200

    # Update the email 
    user = the_token.user
    new_email = user.new_email
    old_email = user.email
    user.change_email()
    db.session.delete(the_token)
    db.session.commit()

    # TODO: log event

    # Notify the old email
    email_sent = send_email_change_sucess_emails(user.name, old_email, new_email)

    response_data ={
            "response":"success",
            "cred_changed": True,
            "mail_sent": email_sent,
        }
    return jsonify(response_data)


@limiter.limit("5/day")
@auth.route('/confirm_password_change/<token>', methods=['GET'])
def confirm_password_change(token):
    """
    confirm_password_change() -> JsonType 
    ----------------------------------------------------------

    Route changes the password associated with the user's account. # TODO
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "mail_sent" value only included if response is "success".

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "mail_sent": True, 
            }
    ``` 
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    password = json_data["password"]

    # Standard error response
    error_response = {"response": "Invalid or expired token."}

    the_token = ValidationToken.query.filter_by(token=token).first()

    if not the_token:
        return jsonify(error_response), 400
    
    validated = the_token.validate_token()

    if validated is False:
        return jsonify(error_response), 400
    

    # Check if password meets safe password criteria
    if not is_good_password(password):
            has_weak_password = True
            logging.info("Weak password provided.")
            # log_event("ACCOUNT_SIGNUP", "weak password") TODO
            return jsonify({"response": "There was an error registering user."}), 400 

    # Prepare pw to save in db
    user = the_token.user

    date = user.created_at
    salt = generate_salt()
    pepper = get_pepper(date)
    salted_password = salt + password + pepper
    hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode("utf-8")
    
    
    # Update the password 

    user.password = hashed_password
    db.session.delete(the_token)
    db.session.commit()

    # TODO: log event

    # Notify the old email
    email_sent = send_pw_change_sucess_email(user.name, user.email)

    response_data ={
            "response":"success",
            "cred_changed": True,
            "mail_sent": email_sent,
        }
    return jsonify(response_data)