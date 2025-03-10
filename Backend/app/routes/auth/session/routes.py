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
from flask import request, jsonify

# Extensions
from flask_login import (
    current_user,
    login_user as flask_login_user,
    login_required,
    logout_user as flask_logout_user,
)
from app.extensions.extensions import db, flask_bcrypt, limiter

# Utilities
from app.utils.bot_detection.bot_detection import bot_caught
from app.utils.constants.enum_class import AuthMethods,modelBool
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.salt_and_pepper.helpers import get_pepper

# Auth helpers
from app.routes.auth.helpers_auth import (
    check_if_user_blocked, 
    get_user_or_none, 
    reset_user_session)
from app.routes.auth.email_helpers import send_email_admin_blocked, send_otp_email

# Session helpers
from app.routes.auth.session.log import (
    log_get_otp,
    log_login
)
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
    # Standard error response
    error_response = {"response": "There was an error generating OTP."} 
    success_response = {"response": "success"}

    # Get the JSON data from the request body 
    json_data = request.get_json()
    email = json_data["email"]
    honeypot = json_data["honeypot"]
    user_agent = json_data.get("user_agent", "") 

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Filter out bots
    if len(honeypot) > 0:
        bot_caught(request, "login")
        log_get_otp(418, f"Email given: {email}", user_agent, client_ip, 0)
        return jsonify(error_response), 418

    # Check if user exists
    if current_user.is_anonymous:
        user = get_user_or_none(email, "get_otp")
    else:
        user = get_user_or_none(current_user.email, "get_otp")

    # Return success even if user does not exist (to avoid information leakage)
    if user is None:
        log_get_otp(404, f"Email given: {email}", user_agent, client_ip, 0)
        return jsonify(success_response)

    # Create OTP
    try:
        otp = user.generate_otp()
        send_otp_email(user.name, otp, email) # not using user.email because otp can be used to confirm recovery email address
    except Exception as e:
        log_message = f"Failed to generate OTP and/or send it per email. Error: {str(e)}"
        logging.warning(log_message) 
        log_get_otp(500, log_message, user_agent, client_ip, user.id)
        return jsonify(error_response), 500
    
    log_get_otp(200, "", user_agent, client_ip, user.id)

    # Return success response
    return jsonify(error_response)



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
    # Standard error response
    error_response = {"response": "There was an error logging in user."} 

    # Get the JSON data from the request body 
    json_data = request.get_json()
    email = json_data["email"]
    password = json_data["password"]
    method =json_data["method"] # login method can be "otp" or "password"
    honeypot = json_data["honeypot"]
    is_first_factor = json_data["is_first_factor"]
    user_agent = json_data.get("user_agent", "") 
    
    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Filter out bots
    if len(honeypot) > 0:
        bot_caught(request, "login")
        log_login(418, f"Email given: {email}", user_agent, client_ip, 0)
        return jsonify(error_response), 418
    
    # Check if user exists

    user = get_user_or_none(email, "login")

    # Delay response in case user does not exist
    # Reason: mitigating timing attacks by introducing randomized delay
    if user is None:
        log_login(404, f"Email given: {email}", user_agent, client_ip, 0)
        delay = random.uniform(1, 6)
        time.sleep(delay)
        return jsonify(error_response), 401

    # Set control variables
    invalid_pw = False
    user_is_blocked = False

    # Check password or otp accordingly
    
    if method == AuthMethods.PASSWORD.value:
        salted_password = user.salt + password + get_pepper(user.created_at)
        if not flask_bcrypt.check_password_hash(user.password, salted_password):
            invalid_pw = True
    elif method == AuthMethods.OTP.value:
        if user.check_otp(password) is False:
            invalid_pw = True
    else:
        logging.error("Invalid AuthMethods value passed to login function")
        invalid_pw = True

    if invalid_pw:
        # Increment login attempts and block if necessary
        try:
            user.increment_login_attempts()
            db.session.commit()
        except Exception as e:
            log_message = f"Login attempt counter could not be incremented, function will continue. Error: {str(e)}"
            logging.error(log_message)
            log_login(500, log_message, user_agent, client_ip, user.id)

    blocked_status = check_if_user_blocked(user, get_client_ip(request))
    user_is_blocked = blocked_status["blocked"]

    if user_is_blocked:
        if blocked_status["temporary_block"] is False:
            send_email_admin_blocked(user.name, user.email)
        log_login(403, "", user_agent, client_ip, user.id)
        return jsonify(blocked_status["message"]), 401 #should be 403, but do not want to give clues

    # If pw/otp is invalid, return
    if invalid_pw:
        log_login(401, f"Wrong password.", user_agent, client_ip, user.id)
        return jsonify(error_response), 401
    
    # MFA: if enabled, handle the step the user is in now
    mfa_enabled = user.mfa_enabled == modelBool.TRUE

    if mfa_enabled:
        if is_first_factor:
            user.mfa_first_factor_used(AuthMethods(method).name)
            db.session.commit()
            if method == AuthMethods.PASSWORD.value:
                msg = "Please confirm the OTP sent to your email address."
                try:
                    otp = user.generate_otp()
                    send_otp_email(user.name, otp, user.email)
                except Exception as e:
                    log_message = f"Failed to generate OTP and/or send it per email. Error: {str(e)}"
                    logging.warning(log_message)
                    log_login(500, log_message, user_agent, client_ip, user.id) 
                    return jsonify(error_response), 500
            else: 
                msg = "Please confirm your password."

            log_login(202, "", user_agent, client_ip, user.id) 
            res = {
                "message": f"First authentication factor accepted. {msg}",
                "response": "pending"
                }
            return jsonify(res), 202
        else:
            # confirm that first factor has indeed been used
            is_really_first = user.first_factor_used == modelBool.TRUE
            if is_really_first is False:
                log_login(422, "", user_agent, client_ip, user.id) 
                return jsonify({"response": "First MFA factor was not completed or the request is out of sequence."} ), 422
            second_factor_success = user.mfa_second_factor_check(AuthMethods(method).name)
            if second_factor_success is False:
                # Likely the user failed to submit the second factor within a specific time frame
                log_login(408, "", user_agent, client_ip, user.id) 
                res = {"response": "Request Timeout (process abandoned) . Please re-start login process."}
                return jsonify(error_response), 408
            
    # Reset login attempts counter upon successful login, set last seen, & create session
    try:
        user.reset_login_attempts()
        user._last_seen = datetime.now(timezone.utc)
        # new_session = user.new_session()
        db.session.commit()
    except Exception as e:
        log_message = f"Login attempt counter could not be reset, function will continue. Error: {str(e)}"
        logging.error(log_message)
        log_login(500, log_message, user_agent, client_ip, user.id) 

    # TODO: consider the bellow if user does not want to be remembered:
    # user.new_session() 
    # db.session.commit()

    # Use Flask-Login to log in the user
    flask_login_user(user)

    # event and system logs
    logging.info("A user logged in.")
    log_login(200, "", user_agent, client_ip, user.id) 
    # logging.debug(f"Session after login: {session}") # Uncomment to debug session
    
    response_data ={
            "response":"success",
            "user": {
                "access": user.access_level.value,
                "name": user.name, 
                "email": user.email,
                "email_is_verified": user.email_is_verified.value,
                "mfa_enabled": user.mfa_enabled.value
                },
            "preferences":{
                "in_mailing_list": user.in_mailing_list.value,
                "night_mode_enabled": user.night_mode_enabled.value,
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

    reset_user_session(current_user) # invalidate old auth sessions
    flask_logout_user() # classic flask-login log out
    logging.info(f"Successful logout") 
    log_login(204, "", "N/A", client_ip, user_id) 

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
                "access": user.access_level.value, 
                "name": user.name, 
                "email": user.email,
                "email_is_verified": user.email_is_verified.value,
                "mfa_enabled": user.mfa_enabled.value,
                },
            "preferences":{
                "in_mailing_list": user.in_mailing_list.value,
                "night_mode_enabled": user.night_mode_enabled.value,
            }
        }
    
    return jsonify(response_data)