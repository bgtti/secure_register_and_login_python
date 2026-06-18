"""
**ABOUT THIS FILE**

auth/session/routes.py contains routes responsible for core authentication and authorization functionalities.
Here you will find the following routes:
- **get_otp** sends an otp to the registered user's email to enable login (in some cases: not required)
- **login** route starts the session
- **logout** route ends a session
- **@me** route delivers user information given a valid session cookie

The format of data sent by the client is validated using Json Schema. 
Reoutes receiving client data are decorated with `@validate_schema(name_of_schema)` for this purpose. 

------------------------
## More information

This app relies on Flask-Login (see `app/extensions`) to handle authentication. It provides user session management, allowing us to track user logins, manage sessions, and protect routes.

Checkout the docs for more information about how Flask-Login works: https://flask-login.readthedocs.io/en/latest/#configuring-your-application

------------------------
## Route testing

Status:
- **get_otp** last test ran on XX December 2024 TODO: testing
- **login** last test ran on XX December 2024 TODO: testing
- **logout** last test ran on XX December 2024 TODO: testing
- **@me** last test ran on XX December 2024 TODO: testing

"""
############# IMPORTS ##############

# Python/Flask libraries
import logging
from datetime import datetime, timezone
import random
import time
from flask import request, jsonify, session

# Extensions
from flask_login import (
    current_user,
    login_user as flask_login_user,
    login_required,
    logout_user as flask_logout_user,
)
from app.extensions.extensions import db, limiter

# Constants
from app.constants.auth_methods import AuthMethods

# Utilities
from app.common.custom_decorators.json_schema_validator import validate_schema
from app.common.ip_utils.ip_address_validation import get_client_ip

# Services
from app.services.auth.user_block_service import svc_check_if_user_blocked
from app.services.auth.user_login_service import svc_register_failed_login, svc_reset_failed_logins
from app.services.auth.user_mfa_service import svc_mark_mfa_first_factor_success, svc_check_mfa_second_factor
from app.services.auth.user_otp_and_pw_service import svc_generate_otp, svc_is_pw_or_otp_valid
from app.services.auth.user_session_service import svc_reset_user_session
from app.services.bot.bot_service import svc_bot_caught
from app.services.user.user_service import svc_get_user_or_none

# Email services
from app.emails.auth.otp_and_pw_email import send_otp_email, send_multiple_failed_pw_input_email
from app.emails.auth.user_blocked_email import send_admin_blocked_email

# Log helpers
from app.routes.auth.session.log import (
    log_get_otp,
    log_login_logout
)

# Schema
from app.routes.auth.session.schemas import login_schema, get_otp_schema

# Blueprint
from . import session


############# ROUTES ###############

####################################
#             GET OTP              #
####################################

@session.route("/get_otp", methods=["POST"])
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
    # Standard response
    error_response = {"response": "there was an error generating OTP."} 
    success_response = {"response": "success"}
    bot_response = {"response": "verification required"}

    # Get the JSON data from the request body 
    json_data = request.get_json()
    email = json_data["email"]
    honeypot = json_data["honeypot"] #TODO: rename!
    user_agent = json_data.get("user_agent", "") 
    form_name = json_data.get("form_name", "Unknown") 

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Filter out bots
    if len(honeypot) > 0:
        # Quietly neutralize request: don't send error because bots adapt
        log_get_otp(418, f"Email given: {email}", user_agent, client_ip, 0)
        svc_bot_caught(request, form_name, "auth/session/get_otp")
        return jsonify(bot_response), 202

    # Check if user exists
    # user_email_addr = email if current_user.is_anonymous else current_user.email
    user = svc_get_user_or_none(email, "get_otp")

    # Return success even if user does not exist (to avoid information leakage)
    if user is None:
        log_get_otp(404, f"Email given: {email}", user_agent, client_ip, 0)
        return jsonify(success_response)

    # Create OTP
    otp = svc_generate_otp(user)

    if not otp:
        log_message = f"Failed to generate OTP. Error: {str(e)}"
        log_get_otp(500, log_message, user_agent, client_ip, user.id)
        return jsonify(error_response), 500

    # Send OTP
    try:
        send_otp_email(user.name, otp, email) # not using user.email because otp can be used to confirm recovery email address
    except Exception as e:
        log_message = f"Failed to send OTP it per email. Error: {str(e)}"
        logging.warning(log_message) 
        log_get_otp(500, log_message, user_agent, client_ip, user.id)
        return jsonify(error_response), 500
    
    log_get_otp(200, "", user_agent, client_ip, user.id)

    # Return success response
    return jsonify(success_response)



####################################
#             LOG IN               #
####################################

@session.route("/login", methods=["POST"])
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
                    "email_is_verified": False,
                    "mfa_enabled": False,
                    },
                "preferences":{
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
    # Standard response
    error_response = {"response": "There was an error logging in user."} 
    bot_response = {"response": "Verification required"}

    # Get the JSON data from the request body 
    json_data = request.get_json()
    email = json_data["email"]
    password = json_data["password"]
    method =json_data["method"] # login method can be "otp" or "password"
    honeypot = json_data["honeypot"] #TODO: rename!
    is_first_factor = json_data["is_first_factor"]
    user_agent = json_data.get("user_agent", "") 
    
    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Filter out bots
    if len(honeypot) > 0:
        svc_bot_caught(request, "login form", "auth/session/login_user")
        log_login_logout(418, f"Email given: {email}", user_agent, client_ip, 0)
        # --> send a 202!!
        #TODO:
        # A honeypot hit should be a risk signal, not a final verdict, especially if you know false positives can happen.
        # Email OTP / magic link / “Confirm login attempt” email (“Yes it was me / No it wasn’t me”)
        # Sign-in required extra verification - “We asked for extra verification to protect your account.”
        # Date/time, device
        # screen show: “We need to verify it’s you”
        return jsonify(bot_response), 202
    
    # Check if user exists
    user = svc_get_user_or_none(email, "login")

    # Delay response in case user does not exist to mitigate timing attacks
    if user is None:
        log_login_logout(404, f"Email given: {email}", user_agent, client_ip, 0)
        time.sleep(random.uniform(1, 6)) # Added delay
        return jsonify(error_response), 401 # Avoid leaking info about existing users

    # Check password/otp svc_register_failed_login
    password_is_valid = svc_is_pw_or_otp_valid(user, password, method)

    if not password_is_valid:
        # Count failed logins and warn if too many
        i = svc_register_failed_login(user, client_ip, user_agent)
        log_login_logout(i["log_code"], i["log_message"], user_agent, client_ip, user.id)
        if i["failed_attempts"] == 8:
            send_multiple_failed_pw_input_email(user.name, i["geo_location"], user.email)
        # return when pw/otp invalid
        return jsonify(error_response), 401
    
    # Check if user is blocked
    blocked_status = svc_check_if_user_blocked(user, get_client_ip(request))

    if blocked_status["blocked"]:
        log_login_logout(403, blocked_status["log_message"], user_agent, client_ip, user.id)
        if blocked_status["temporary_block"] is False:
            send_admin_blocked_email(user.name, user.email) 
        return jsonify(blocked_status["message"]), 401 #should be 403, but do not want to give clues
    
    # MFA: if enabled, handle the step the user is in now
    if user.mfa_enabled:
        if is_first_factor:
            svc_mark_mfa_first_factor_success(user,AuthMethods(method))
            db.session.commit()
            if method == AuthMethods.PASSWORD.value:
                msg = "Please confirm the OTP sent to your email address."
                log_txt = "Password validated."
                try:
                    otp = svc_generate_otp(user)
                    send_otp_email(user.name, otp, user.email)
                except Exception as e:
                    log_message = f"Failed to generate OTP and/or send it per email. Error: {str(e)}"
                    log_login_logout(500, log_message, user_agent, client_ip, user.id) 
                    return jsonify(error_response), 500
            else: 
                msg = "Please confirm your password."
                log_txt = "OTP validated."
            log_login_logout(202, log_txt, user_agent, client_ip, user.id) 
            res = {
                "message": f"First authentication factor accepted. {msg}",
                "response": "pending"
                }
            return jsonify(res), 202
        else:
            # confirm that first factor has indeed been used
            if user.first_factor_used is False:
                log_login_logout(422, "", user_agent, client_ip, user.id) 
                return jsonify({"response": "First MFA factor was not completed or the request is out of sequence."} ), 422
            second_factor_success = svc_check_mfa_second_factor(user, AuthMethods(method))
            if second_factor_success is False:
                # Likely the user failed to submit the second factor within a specific time frame
                log_login_logout(408, "", user_agent, client_ip, user.id) 
                return jsonify({"response": "Request Timeout (process abandoned) . Please re-start login process."}), 408
            
    # Reset login attempts counter upon successful login, set last seen, & create session
    try:
        svc_reset_failed_logins(user)
        user._last_seen = datetime.now(timezone.utc)
        # new_session = user.new_session()
        db.session.commit()
    except Exception as e:
        log_message = f"Login attempt counter could not be reset, function will continue. Error: {str(e)}"
        logging.error(log_message)
        log_login_logout(500, log_message, user_agent, client_ip, user.id) 

    # TODO: consider the bellow if user does not want to be remembered:
    # user.new_session() 
    # db.session.commit()

    # Use Flask-Login to log in the user
    flask_login_user(user)

    # event and system logs
    logging.info("A user logged in.")
    log_login_logout(200, "", user_agent, client_ip, user.id) 
    # logging.debug(f"Session after login: {session}") # Uncomment to debug session
    
    response_data ={
            "response":"success",
            "user": {
                "access": user.role.access_level,
                "name": user.name, 
                "email": user.email,
                "email_is_verified": user.email_is_verified,
                "mfa_enabled": user.mfa_enabled
                },
            "preferences":{
                "in_mailing_list": user.in_mailing_list,
                "night_mode_enabled": user.night_mode_enabled,
            } 
        }
    return jsonify(response_data)


####################################
#            LOG OUT               #
####################################

@session.route("/logout", methods=["POST"])
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
    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Current user saved for logging
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = 0

    svc_reset_user_session(current_user) # invalidate old auth sessions
    flask_logout_user() # classic flask-login log out
    session.clear() # to be safe, Flask-Session will: delete all session data in Redis for that session
    log_login_logout(204, "", "", client_ip, user_id) 

    #TODO: delete all old redis sessions
    #TODO: clean multi-session invalidation system needed for redis cleaup

    return jsonify({"response":"success"})

####################################
#   GET CURRENT USER FROM COOKIE   #
####################################

@session.route("/@me")
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
                    "email_is_verified": False,
                    "mfa_enabled": False,
                    }, 
                "preferences":{
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
                "access": user.role.access_level, 
                "name": user.name, 
                "email": user.email,
                "email_is_verified": user.email_is_verified,
                "mfa_enabled": user.mfa_enabled,
                },
            "preferences":{
                "in_mailing_list": user.in_mailing_list,
                "night_mode_enabled": user.night_mode_enabled,
            }
        }
    
    return jsonify(response_data)