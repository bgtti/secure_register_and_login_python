"""
**ABOUT THIS FILE**

auth/routes_registration.py contains routes responsible for the user account's existence.
Here you will find the following routes:
- **signup** route creates the user's account
- **delete_user_acct** route #=> TODO

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
import random
import time
# from flask import Blueprint, request, jsonify, session
from flask import request, jsonify
from flask_login import (
    login_user as flask_login_user,
    logout_user as flask_logout_user,
    current_user,
    login_required,
)

# Extensions
from app.extensions.extensions import db, limiter, flask_bcrypt

# Database models
from app.models.user import User
from app.models.token import Token

# Utilities
from app.utils.bot_detection.bot_detection import bot_caught
from app.utils.constants.enum_class import TokenPurpose, modelBool
from app.utils.detect_html.detect_html import check_for_html
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.log_event_utils.log import log_event
from app.utils.profanity_check.profanity_check import has_profanity
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper
from app.utils.token_utils.sign_and_verify import verify_signed_token
from app.utils.token_utils.verification_urls import create_verification_url
from app.utils.custom_decorators.json_schema_validator import validate_schema

# Auth helpers (this file)
from app.routes.auth.auth_helpers import get_hashed_pw, get_user_or_none, user_name_is_valid, reset_user_session
from app.routes.auth.email_helpers_registration import (
    send_email_acct_exists,
    send_email_acct_created,
    send_email_acct_deleted

)
from app.routes.auth.schemas import (
    signup_schema,
    delete_user_schema
)

# Blueprint
from . import auth


############# ROUTES ###############

####################################
#             SIGN UP              #
####################################

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
    - "user" and "preferences" values only included if response is "success".

    ----------------------------------------------------------
    **Response example:**
    ```python
        response_data = {
                "response":"success",
                "user": {
                    "access": "user"
                    "name": "John", 
                    "email": "john@email.com",
                    "email_is_verified": False # will always be false after signup,
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
        user_if_exists = get_user_or_none(email, "signup")
        user_exists = user_if_exists is not None 
    except Exception as e:
        logging.error(f"Could not check if user exists in db: {e}")

    if user_exists:
        try:
            send_email_acct_exists(user_if_exists.name, user_if_exists.email)
            logging.info(f"User already in db (error 409 in reality): {email}")
            log_event("ACCOUNT_SIGNUP", "user exists", user_if_exists.id)
        except Exception as e:
            logging.error(f"Could not log event in signup: {e}")
    
    # Check if password meets safe password criteria, salt and pepper password, then hash it
    date = datetime.now(timezone.utc) # date is required to get apropriate Pepper value
    salt = generate_salt()
    hashed_password = get_hashed_pw(password, date, salt) # will be null if password does not meet criteria
    
    # Determine if the new user should be flagged on the base of possible html or profanity in input (so admin could check). Flag colours described in enum in user's model page.
    flag = False

    name_is_valid = user_name_is_valid(name)

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
    
    if user_exists or not hashed_password or name_is_valid is False:
        return jsonify({"response": "There was an error registering user."}), 400 

    # Create user
    try:
        new_user = User(name=name, email=email, password=hashed_password, salt=salt, created_at=date) # passing on the creation date to make sure it is the same used for pepper
        db.session.add(new_user)
        if flag:
            new_user.flag_change(flag)
        new_user.new_session() # an alternative id should be created to be used in session management
        db.session.commit()

        send_email_acct_created(new_user.name, new_user.email)

    except Exception as e:
        db.session.rollback() 
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

    response_data ={
            "response":"success",
            "user": {
                "access": new_user.access_level.value, 
                "name": new_user.name, 
                "email": new_user.email,
                "email_is_verified": False,
                "mfa_enabled": False,
                },
            "preferences":{
                "in_mailing_list": False,
                "night_mode_enabled": True,
            }
        }
    return jsonify(response_data)



####################################
#       DELETE USER ACCOUNT        #
####################################

@auth.route("/delete_user", methods=["POST"])
@login_required
@limiter.limit("2/minute; 10/day")
@validate_schema(delete_user_schema)
def delete_user():
    """
    delete_user() -> JsonType
    ----------------------------------------------------------

    Route deletes the user's account.
    
    Requires json data from the client. 
    Sets a session cookie in response.
    Returns Json object containing strings:
    - "response" value is always included.  

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"User deleted successfully!"
            }
    ``` 
    """
    # NOTE: consider placing account in quarantene (in case user did not want a deletion)

    # Standard error response
    error_response = {"response": "An error prevented account from being deleted."} 

    # Get the JSON data from the request body 
    json_data = request.get_json()
    password = json_data["password"]
    otp = json_data.get("otp", "")
    user_agent = json_data.get("user_agent", "") #TODO log this in event
    
    # Check if user exists

    user = get_user_or_none(current_user.email, "delete_user")

    print(current_user)

    # Delay response in case of wrong credentials to mitigate attacks by introducing randomized delay
    def delay_response():
        delay = random.uniform(1, 10)
        time.sleep(delay)

    if user is None:
        delay_response()
        return jsonify(error_response), 404
    
    # Wrong credentials response
    wrong_creds_res = {"response": "Wrong credentials: password/OTP expired or incorrect."} 

    # Check password
    salted_password = user.salt + password + get_pepper(user.created_at)
    if not flask_bcrypt.check_password_hash(user.password, salted_password):
        delay_response()
        return jsonify({"response": "Wrong credentials: password incorrect."} ), 401
    
    # Check OTP only if user has mfa set
    mfa_enabled = user.mfa_enabled == modelBool.TRUE
    if mfa_enabled:
        if user.check_otp(otp) is False:
            delay_response()
            return jsonify({"response": "Wrong credentials: OTP incorrect or expired."}), 401
        
    # Credentials correct: delete user
    try:
        name=user.name
        email=user.email
        db.session.delete(user)
        db.session.commit()
        send_email_acct_deleted(name, email)
        logging.info("User deleted account.")

        #logout user
        reset_user_session(current_user) # invalidate old auth sessions
        flask_logout_user() # classic flask-login log out

        return jsonify({"message": "User deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback() 
        logging.error(f"Failed to delete user. Details: {str(e)}")
        return jsonify(error_response), 500
