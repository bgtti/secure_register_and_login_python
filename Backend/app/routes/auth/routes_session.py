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

"""
############# IMPORTS ##############

# Python/Flask libraries
import logging
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, session
from flask_login import (
    current_user,
    login_user as flask_login_user,
    login_required,
    logout_user as flask_logout_user,
)

# Extensions
from app.extensions.extensions import db, flask_bcrypt, limiter, login_manager

# Database models
from app.models.user import User

# Utilities
from app.utils.bot_detection.bot_detection import bot_caught
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.utils.detect_html.detect_html import check_for_html
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.ip_utils.ip_anonymization import anonymize_ip
from app.utils.ip_utils.ip_geolocation import geolocate_ip
from app.utils.log_event_utils.log import log_event
from app.utils.profanity_check.profanity_check import has_profanity
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper

# Auth helpers
from app.routes.auth.auth_helpers import get_hashed_pw, is_good_password, reset_user_session, get_user_or_none
from app.routes.auth.email_helpers import send_otp_email
from app.routes.auth.schemas import login_schema, signup_schema

# Blueprint
from . import auth


############# ROUTES ###############

####################################
#             GET OTP              #
####################################

@auth.route("/get_otp", methods=["POST"])
@limiter.limit("30/minute;50/day")
@validate_schema(login_schema)#==>TODO
def get_otp():
    # Standard error response
    error_response = {"response": "There was an error generating OTP."} 

    # Get the JSON data from the request body 
    json_data = request.get_json()
    email = json_data["email"]
    honeypot = json_data["honeypot"]

    # Filter out bots
    if len(honeypot) > 0:
        bot_caught(request, "login")
        return jsonify(error_response), 418

    # Check if user exists
    # TODO: Check existence = test
    user = get_user_or_none(email)
    # TODO: DB errors should return error_response + 500 

    # Case 1: user does not exist
    # TODO: If user does not exist, return 200 (bad actors must not know if users exist or not)

    # Case 2: user exists
    # Create OTP
    # TODO: Create OTP in the DB with a timestamp.
    # Send email
    # TODO: send the user an email with the OTP
    # TODO: if error, return error_response + 500
    # TODO: return 200



####################################
#             LOG IN               #
####################################

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
    honeypot = json_data["honeypot"]
    #TODO: check whether login is via pw or otp (get json)

    # Filter out bots
    if len(honeypot) > 0:
        bot_caught(request, "login")
        return jsonify(error_response), 418
    
    # TODO: 1) separate the credentials check between email and password validation
    # TODO: 2) if both email and password are correct, but the user is blocked:
    #           a) if mfa enabled, send user an email saying the user is blocked
    #           b) if mfa is not enabled, send to FE the information that the user is blocked

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

    # Check if the user is trying to sign in with PW or OTP
    # TODO: if pw, check pw credentials (adapt bellow code)

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

    
    # TODO: if otp, check if otp is valid


    # If either email and pw/otp are invalid, return
    if invalid_credentials:
        return jsonify(error_response), 401
    
    # TODO If user DOES NOT have mfa enabled, then reset counter here. If not, reset counter at mfa route

    # Reset login attempts counter upon successful login, set last seen, & create session
    try:
        user.reset_login_attempts()
        user._last_seen = datetime.now(timezone.utc)
        # new_session = user.new_session()
        db.session.commit()
    except Exception as e:
        logging.error(f"Login attempt counter could not be reset, function will continue. Error: {e}")

    # Check for html in user input TODO: why html detection here? only makes sense if accnt doesnt exist...delete or modify!
    html_in_email = check_for_html(email, "login - email field")
    try:
        log_event("ACCOUNT_LOGIN", "login successful", user.id)
        if html_in_email:
            log_event("ACCOUNT_LOGIN", "html detected", user.id, f"Email provided: {email}")
    except Exception as e:
        logging.error(f"Failed to create event log. Error: {e}")

    #TODO: if mfa enabled:
    #      1) check the missing step. 
    #      2) save to the DB the fact that step 1 of verification was completed (inform the db which step was used now otp/pw)
    #      3) save the date/time of step 1 verification to the db
    #      4) action if...
    #         otp was used now, then simply return 200 informing PW is missing
    #         pw was used now, a) send otp to user email, b) return 200 to FE informing OTP is missing

    # MFA not enabled: log user in

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