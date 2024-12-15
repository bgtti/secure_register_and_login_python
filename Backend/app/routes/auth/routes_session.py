"""
**ABOUT THIS FILE**

auth/routes_session.py contains routes responsible for core authentication and authorization functionalities.
Here you will find the following routes:
- **login** route starts the session when mfa is not enabled or sends an otp as the first login step #TODO: otp part
- **login_mfa** route starts the session (when mfa enabled) as the second step of the mfa login process #TODO
- **logout** route ends a session
- **@me** route delivers user information given a session cookie

The format of data sent by the client is validated using Json Schema. 
Reoutes receiving client data are decorated with `@validate_schema(name_of_schema)` for this purpose. 

------------------------
## More information

This app relies on Flask-Login (see `app/extensions`) to handle authentication. It provides user session management, allowing us to track user logins, manage sessions, and protect routes.

Checkout the docs for more information about how Flask-Login works: https://flask-login.readthedocs.io/en/latest/#configuring-your-application

------------------------
## Route testing

Status:
- **login** last test ran on XX December 2024 TODO: testing
- **login_mfa** last test ran on XX December 2024 TODO: testing
- **logout** last test ran on XX December 2024 TODO: testing
- **@me** last test ran on XX December 2024 TODO: testing

"""
############# IMPORTS ##############

# Python/Flask libraries
import logging
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, session
import re
from typing import Dict, Any

# Extensions
from flask_login import (
    current_user,
    login_user as flask_login_user,
    login_required,
    logout_user as flask_logout_user,
)
from app.extensions.extensions import db, flask_bcrypt, limiter, login_manager

# Database models
from app.models.user import User

# Utilities
from app.utils.bot_detection.bot_detection import bot_caught
from app.utils.constants.account_constants import OTP_PATTERN
from app.utils.constants.enum_class import LoginMethods,modelBool
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.utils.detect_html.detect_html import check_for_html
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.ip_utils.ip_anonymization import anonymize_ip
from app.utils.ip_utils.ip_geolocation import geolocate_ip
from app.utils.log_event_utils.log import log_event
from app.utils.profanity_check.profanity_check import has_profanity
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper

# Auth helpers
from app.routes.auth.auth_helpers import get_hashed_pw, is_good_password, reset_user_session, get_user_or_none,check_if_user_blocked
from app.routes.auth.email_helpers import send_otp_email
from app.routes.auth.schemas import login_schema, signup_schema, get_otp_schema

# Blueprint
from . import auth


############# ROUTES ###############

####################################
#             GET OTP              #
####################################

@auth.route("/get_otp", methods=["POST"])
@limiter.limit("20/minute;50/day")
@validate_schema(get_otp_schema)
def get_otp(): 
    """
    get_otp() -> JsonType
    ----------------------------------------------------------

    Generates and sends a One-Time Password (OTP) for a user.

    The OTP will be sent to the registered user via email.
    Requires json data from the client (the user's email and honeypot). 
    
    Returns Json object containing strings:
    - "response" value is always included. 

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
            }
    ``` 
    ----------------------------------------------------------
    **About errors:**

    Error messages sent to the front-end are ambiguous by design. Check the logs to understand the error.
    The reason for this is to pass ambiguity to the front end so as not to give a malicious actor information about whether a certain email address is or not registered with the website.
    """
    # Standard error response
    error_response = {"response": "There was an error generating OTP."} 
    success_response = {"response": "success"}

    # Get the JSON data from the request body 
    json_data = request.get_json()
    email = json_data["email"]
    honeypot = json_data["honeypot"]

    # Filter out bots
    if len(honeypot) > 0:
        bot_caught(request, "login")
        return jsonify(error_response), 418

    # Check if user exists
    user = get_user_or_none(email, "get_otp")

    # Return success even if user does not exist (to avoid information leakage)
    if user is None:
        return jsonify(success_response)

    # Create OTP
    try:
        otp = user.generate_otp()
    except Exception as e:
        logging.warning(f"Failed to generate OTP. Error: {e}") 
        return jsonify(error_response), 500

    # Send email
    email_sent = False
    try:
        email_sent = send_otp_email(user.name, otp, user.email)
    except Exception as e:
        logging.warning(f"Failed to send email with otp. Error: {e}") 

    if email_sent is False:
        return jsonify(error_response), 500
    
    # Return success response
    return jsonify(error_response)



####################################
#             LOG IN               #
####################################

@auth.route("/login", methods=["POST"])
@limiter.limit("20/minute;50/day")
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
                    "access": "user",
                    "email_is_verified": False
                    },
                "preferences":{
                    "mfa_enabled": False,
                    "in_mailing_list": False,
                    "night_mode_enabled": True,
                } 
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
    method =json_data["method"] # login method can be "otp" or "password"
    honeypot = json_data["honeypot"]

    # Filter out bots
    if len(honeypot) > 0:
        bot_caught(request, "login")
        return jsonify(error_response), 418
    
    # TODO: 2) if both email and password are correct, but the user is blocked:
    #           a) if mfa enabled, send user an email saying the user is blocked
    #           b) if mfa is not enabled, send to FE the information that the user is blocked

    # Check if user exists
    invalid_email = False
    invalid_pw = False
    user_is_blocked = False

    user = get_user_or_none(email)

    if user is None:
        invalid_email = True

    # Check password or otp accordingly
    if not invalid_email:
        if method == LoginMethods.PASSWORD.value:
            salted_password = user.salt + password + get_pepper(user.created_at)
            if not flask_bcrypt.check_password_hash(user.password, salted_password):
                invalid_pw = True
        elif method == LoginMethods.OTP.value:
            if user.check_otp(password) is False:
                invalid_pw = True
    
        if invalid_pw:
            # Increment login attempts and block if necessary
                try:
                    user.increment_login_attempts()
                    db.session.commit()
                except Exception as e:
                    logging.error(f"Login attempt counter could not be incremented, function will continue. Error: {e}")

        blocked_status = check_if_user_blocked(user, get_client_ip(request))
        user_is_blocked = blocked_status["blocked"]

    if user_is_blocked:
        return jsonify(blocked_status["message"]), 403

    # If either email and pw/otp are invalid, return
    if invalid_pw or invalid_email:
        return jsonify(error_response), 401
    
    # TODO If user DOES NOT have mfa enabled, then reset counter here. If not, reset counter at mfa route
    mfa_enabled = user.mfa_enabled == modelBool.TRUE

    if mfa_enabled:
        is_first_factor = user.first_factor_used == modelBool.FALSE
        if is_first_factor:
            user.mfa_first_factor_used(LoginMethods(method).name)
            if method == LoginMethods.PASSWORD.value:
                msg = "Please confirm the OTP sent to your email address."
                try:
                    otp = user.generate_otp()
                    send_otp_email(user.name, otp, user.email)
                except Exception as e:
                    logging.warning(f"Failed to generate OTP and/or send it per email. Error: {e}") 
                    return jsonify(error_response), 500
            else: 
                msg = "Please confirm your password."
            res = {
                "message": f"First authentication factor accepted. {msg}",
                "response": "pending"
                }
            return jsonify(res), 202
        else:
            second_factor_success = user.mfa_second_factor_check(LoginMethods(method).name)
            if second_factor_success is False:
                # Likely the user failed to submit the second factor within a specific time frame
                res = {"response": "Request Timeout (process abandoned) . Please re-start login process."}
                return jsonify(error_response), 408
            
    # Reset login attempts counter upon successful login, set last seen, & create session
    try:
        user.reset_login_attempts()
        user._last_seen = datetime.now(timezone.utc)
        # new_session = user.new_session()
        db.session.commit()
    except Exception as e:
        logging.error(f"Login attempt counter could not be reset, function will continue. Error: {e}")

    try:
        log_event("ACCOUNT_LOGIN", "login successful", user.id)
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
    
    response_data ={
            "response":"success",
            "user": {
                "access": user.access_level.value,
                "name": user.name, 
                "email": user.email,
                "email_is_verified": user.email_is_verified.value
                },
            "preferences":{
                "mfa_enabled": user.mfa_enabled.value,
                "in_mailing_list": user.in_mailing_list.value,
                "night_mode_enabled": user.night_mode_enabled.value,
            } 
        }
    return jsonify(response_data)


####################################
#           LOG IN: MFA            #
####################################
@auth.route("/login_mfa", methods=["POST"])
@limiter.limit("30/minute;50/day")
@validate_schema(login_schema) # TODO: schema
def login_user_mfa():
    """
    TODO: docstring
    """
    # Standard error response
    error_response = {"response": "There was an error logging in user."} 

    # Get the JSON data from the request body 
    # TODO: get json: email, pw/otp, honeypot necessary

    # Check if user exists/ get user
    # TODO: check if user in the db, if not, return error

    # If user exists, check whether the is a missing verification step
    # TODO: get the missing verification step:
    #       - if no verification step missing, return error
    #       - if verification step missing, but step one was too far in the past ( 30 mins?), return error

    # Check the set 2 credential
    # TODO: if now an otp was sent, validate otp
    # TODO: if now a password was sent, validate pw

    # TODO: If second validation step fails, return

    # if second validation step suceeds
    # Reset login attempts counter, set last seen, erase mfa first step on user DB
    # TODO: reset login attempts counter
    # TODO: set last seen 
    # TODO: erase mfa first step and timestamp

    # Use Flask-Login to log in the user
    # TODO: create session

    # Log 
    # TODO: log event
    # TODO: log to system

    # Return
    # TODO: return 200
    print("mfa")



####################################
#            LOG OUT               #
####################################

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

####################################
#  GET CURRENT USER FROM COOKIE    #
####################################

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
                    "access": "user",
                    "email_is_verified": False
                    }, 
                "preferences":{
                    "mfa_enabled": False,
                    "in_mailing_list": True,
                    "night_mode_enabled": False,
                }
            }
    ``` 
    """

    user = current_user

    response_data ={
            "response":"success",
            "user": {
                "access": user.access_level.value, 
                "name": user.name, 
                "email": user.email,
                "email_is_verified": user.email_is_verified.value
                },
            "preferences":{
                "mfa_enabled": user.mfa_enabled.value,
                "in_mailing_list": user.in_mailing_list.value,
                "night_mode_enabled": user.night_mode_enabled.value,
            }
        }
    return jsonify(response_data)