"""
**ABOUT THIS FILE**

auth/routes_recovery.py contains routes responsible for a user's account recovery.
Here you will find the following routes:
- **set_recovery_email** sets second email in case user looses access to his/her registered email
- **recover_account** TODO: not implemented

The format of data sent by the client is validated using Json Schema. 
Reoutes receiving client data are decorated with `@validate_schema(name_of_schema)` for this purpose. 

------------------------
## More information

This app relies on Flask-Login (see `app/extensions`) to handle authentication. It provides user session management, allowing us to track user logins, manage sessions, and protect routes.

Checkout the docs for more information about how Flask-Login works: https://flask-login.readthedocs.io/en/latest/#configuring-your-application

------------------------
## Route testing

Status:
- **set_recovery_email** last test ran on XX December 2024 TODO: testing

"""
############# IMPORTS ##############

# Python/Flask libraries
import logging
from datetime import datetime, timezone
from flask import request, jsonify

# Extensions and third-party libs
from flask_login import (
    current_user,
    login_user as flask_login_user,
    login_required,
    logout_user as flask_logout_user,
)
from app.extensions.extensions import db, cipher, flask_bcrypt, limiter, login_manager

# Database models
from app.models.user import User

# Utilities
from app.utils.bot_detection.bot_detection import bot_caught
from app.utils.constants.enum_class import LoginMethods,modelBool
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.utils.detect_html.detect_html import check_for_html
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.log_event_utils.log import log_event
from app.utils.profanity_check.profanity_check import has_profanity
from app.utils.salt_and_pepper.helpers import get_pepper

# Auth helpers
from app.routes.auth.auth_helpers import anonymize_email, check_if_user_blocked, get_user_or_none, reset_user_session
from app.routes.auth.email_helpers import send_email_recovery_set
from app.routes.auth.schemas import set_recovery_email_schema, get_recovery_email_schema

# Blueprint
from . import auth


############# ROUTES ###############

####################################
#         SET RECOVERY EMAIL       #
####################################

@auth.route("/set_recovery_email", methods=["POST"])
@login_required
@limiter.limit("5/minute;6/day")
@validate_schema(set_recovery_email_schema) 
def set_recovery_email(): 
    """
    get_otp() -> JsonType
    ----------------------------------------------------------

    Sets a recovery email to the user's account.
    
    Returns Json object containing strings:
    - "response" value is always included. 

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "recovery_email": "john@doe.com"
            }
    ``` 
    """
    # Standard error response
    error_response = {"response": "There was an error saving recovery email."} 

    # Get the JSON data from the request body 
    json_data = request.get_json()
    recovery_email = json_data["recovery_email"]
    password = json_data["password"]
    otp = json_data["otp"]
    user_agent = json_data.get("user_agent", "") #TODO log this in event

    # Get the user from cookie --- try to call method directly on current_user to see if it works!
    try:
        user = User.query.filter_by(email=current_user.email).first()
    except Exception as e:
        logging.error(f"Failed to get user. Error: {e}")
        return jsonify(error_response), 500

    # Check password and OTP
    if user.check_otp(otp) is False:
        return jsonify({"response": "Provided OTP is wrong or expired."} ), 401
    
    salted_password = user.salt + password + get_pepper(user.created_at)
    if not flask_bcrypt.check_password_hash(user.password, salted_password):
        return jsonify({"response": "Password incorrect."} ), 401

    try:
        if check_for_html(recovery_email, "set recovery email", recovery_email):
            user.flag = "YELLOW"
        elif has_profanity(recovery_email):
                user.flag = "PURPLE"
        # TODO: if old recovery email, send message it is no longer (it has been changed)
        user.recovery_email = recovery_email
        db.session.commit()
    except Exception as e:
        logging.error(f"Failed to save recovery email. Error: {e}")
        return jsonify(error_response), 500
    
    # Send confirmation emails that new recovery has been added
    try:
        mail_sent = send_email_recovery_set(user.name, user.email, recovery_email)
        if not mail_sent:
            logging.error(f"Failed to send confirmation emails of set account recovery email.")
    except Exception as e:
        logging.error(f"Error encountered while trying to send confirmation of setting recovery email. Error: {e}")

    # Anonymize recovery email
    anonymized_recovery_email = anonymize_email(recovery_email)

    response_data = {
            "response":"Recovery email added successfully!",
            "recovery_email_added": True,
            "recovery_email_preview": anonymized_recovery_email
        }
    return jsonify(response_data)

####################################
#        GET RECOVERY STATUS       #
####################################

@auth.route("/get_recovery_status")
@login_required
def get_recovery_status():
    """
    get_recovery_status() -> JsonType
    ----------------------------------------------------------

    Route sends user's recovery_email. 
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "recovery_email_preview" value only included if recovery_email_added is true.

    ----------------------------------------------------------
    **Response example:**

    # If recovery_email is "john@email.com", it's preview will be:

    ```python
        response_data = {
                "response":"success",
                "recovery_email_added": true,
                "recovery_email_preview": "j***@e***.com" 
            }
    ``` 
    """
    # Get the recovery email (it may be None or a string)
    recovery_email = current_user.recovery_email

    # Determine if a recovery email was added
    recovery_email_added = recovery_email is not None and recovery_email.strip() != ""

    # Anonymize email if it's provided
    anonymized_recovery_email = anonymize_email(recovery_email) if recovery_email_added else ""

    response_data = {
            "response":"success",
            "recovery_email_added": recovery_email_added,
            "recovery_email_preview": anonymized_recovery_email
        }
    return jsonify(response_data)

####################################
#        GET RECOVERY EMAIL        #
####################################

@auth.route("/get_recovery_email", methods=["POST"])
@login_required
@limiter.limit("5/minute;10/day")
@validate_schema(get_recovery_email_schema) 
def get_recovery_email():
    """
    get_recovery_email() -> JsonType
    ----------------------------------------------------------

    Route sends user's recovery_email. 
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "recovery_email" value only included if response is "success".

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "recovery_email": john@email.com" 
            }
    ``` 
    """
    # Get the JSON data from the request body 
    json_data = request.get_json()
    password = json_data["password"]
    user_agent = json_data.get("user_agent", "") #TODO log this in event

    # Get the user from cookie --- try to call method directly on current_user to see if it works!
    try:
        user = User.query.filter_by(email=current_user.email).first()
    except Exception as e:
        logging.error(f"Database query failed: {e}")
        return jsonify({"response": "An error occurred while fetching the user."}), 500

    # Check password     
    salted_password = user.salt + password + get_pepper(user.created_at)
    if not flask_bcrypt.check_password_hash(user.password, salted_password):
        return jsonify({"response": "Password incorrect."} ), 401

    # Get the recovery email (it may be None or a string)
    recovery_email = user.recovery_email

    if not recovery_email:
        return jsonify({"response": "No recovery email found."} ), 404
    

    response_data = {
            "response":"success",
            "recovery_email": recovery_email
        }
    return jsonify(response_data)