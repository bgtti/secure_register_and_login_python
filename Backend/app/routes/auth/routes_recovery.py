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
from app.routes.auth.auth_helpers import check_if_user_blocked, get_user_or_none, reset_user_session
from app.routes.auth.email_helpers import send_email_recovery_set
from app.routes.auth.schemas import set_recovery_email_schema

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
    email = json_data["email"]
    password = json_data["password"]
    otp = json_data["otp"]

    # Get the user from cookie
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
        try:
            user.increment_login_attempts()
            db.session.commit()
        except Exception as e:
            logging.error(f"Login attempt counter could not be incremented, function will continue. Error: {e}")
        return jsonify({"response": "Password incorrect."} ), 401

    try:
        if check_for_html(email, "set recovery email", email):
            user.flag = "YELLOW"
        elif has_profanity(email):
                user.flag = "PURPLE"

        user.recovery_email = email
        db.session.commit()
    except Exception as e:
        logging.error(f"Failed to get user. Error: {e}")
        return jsonify(error_response), 500
    
    # TODO: confirmation email that recovery email has been added
    try:
        mail_sent = send_email_recovery_set(user.email, email)
        if not mail_sent:
            logging.error(f"Failed to send confirmation emails of set account recovery email.")
    except Exception as e:
        logging.error(f"Error encountered while trying to send confirmation of setting recovery email. Error: {e}")

    success_response = {
        "response": "success",
        "recovery_email": email
        }

    return jsonify(success_response)



####################################
#        GET RECOVERY EMAIL        #
####################################

# Standard error response
@auth.route("/get_recovery_email")
@login_required
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

    response_data = {
            "response":"success",
            "recovery_email": current_user.recovery_email
        }
    return jsonify(response_data)