"""
**ABOUT THIS FILE**

auth/registration/routes.py contains routes responsible for the user account's existence.
Here you will find the following routes:
- **signup** route creates the user's account
- **delete_user_acct** deteles the user's account

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
import random
import time
from flask import request, jsonify, session
from flask_login import (
    current_user,
    login_user as flask_login_user,
    logout_user as flask_logout_user,
    login_required,
)

# Extensions
from app.extensions.extensions import db, limiter, flask_bcrypt

# Database models
from app.models.user import User

# Utilities: general
from app.common.detect_html.detect_html import check_for_html
from app.common.ip_utils.ip_address_validation import get_client_ip
from app.common.profanity_check.profanity_check import has_profanity
from app.common.salt_and_pepper.helpers import generate_salt, get_pepper
from app.common.custom_decorators.json_schema_validator import validate_schema

# Services
from app.services.auth.user_acct_deletion_service import svc_delete_user_account
from app.services.auth.user_acct_registration_service import svc_register_user
from app.services.bot.bot_service import svc_bot_caught
from app.services.user.user_service import svc_get_user_or_none

# Email services
from app.emails.auth.acct_registration_email import (
    send_email_acct_exists,
    send_email_acct_created
)
from app.emails.auth.acct_deletion_email import send_email_acct_deleted

# Log helpers
from app.routes.auth.registration.log import(
    log_signup_user,
    log_delete_user
)

# Json schemas
from app.routes.auth.registration.schemas import (
    signup_schema,
    delete_user_schema
)

# Blueprint
from . import registration


############# ROUTES ###############

####################################
#             SIGN UP              #
####################################

@registration.route("/signup", methods=["POST"])
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
                    "access": "user",
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
    honeypot = json_data["honeypot"] #TODO: change name!
    user_agent = json_data.get("user_agent", "") #TODO: FRONT END MUST SEND IT: check api call react
    client_ip = get_client_ip(request) or ""

    if len(honeypot) > 0:
        svc_bot_caught(request, "signup", "auth/registration/signup_user")
        log_signup_user(418, f"Email given: {email}", user_agent, client_ip, 0)
        #--> TODO front end adaptation: if screen readers fall in honeypot, 
        # Ideally: force email validation
        time.sleep(random.uniform(1, 7)) # Added delay before returning
        bot_res = {"response": "Complete next steps for account creation."}
        return jsonify(bot_res), 202
    
    # Try to register user
    reg_outcome = svc_register_user(name, email, password)

    user_created = reg_outcome["success"]
    user_id = reg_outcome["user_id"]
    log_code = reg_outcome["log_code"]
    log_text = reg_outcome["log_text"]

    # Log
    log_signup_user(log_code, log_text, user_agent, client_ip, user_id)

    # Registration successful
    if user_created:
        try:
            # Get newly created user
            user = db.session.get(User, user_id)
            if not user:
                raise ValueError(f"User {user_id} not found after registration")
            # Create session
            user.new_session() # an alternative id should be created to be used in session management
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            l_msg = f"User should have been created but could not be found by id or session could not be registered. Registration of {email} possibly failed or new_session() error."
            logging.error(f"{l_msg} Info: {e}")
            log_signup_user(500, l_msg, user_agent, client_ip, user_id)
            return jsonify(error_response), 500
        
        # Send account creation email
        send_email_acct_created(name, email)

        # Login user
        flask_login_user(user)

        # Return success
        response_data ={
                "response":"success",
                "user": {
                    "access": user.role.access_level, 
                    "name": user.name, 
                    "email": user.email,
                    "email_is_verified": False,
                    "mfa_enabled": False,
                    },
                "preferences":{
                    "in_mailing_list": False,
                    "night_mode_enabled": True,
                }
            }
        # Note we are not encoding user input when sending to FE because the FE is built with React with JSX
        # JSX auto-escapes the data before putting it into the page, so deemed escaping to be unecessary.
        return jsonify(response_data)
    
    # Registration failed

    # If there was a DB failure, send a 500
    if log_code == 500:
        return jsonify(error_response), 500

    # If user already exists, send email 
    if reg_outcome["user_already_exists"]:
        send_email_acct_exists(reg_outcome["user_name"], email)
    
    # Add delay before returning a failure. The reason is to diminish the response time discrepancy between a successfully created user and a failed response. The difference in response time can be used by bad actors to deduce whether an account exists or not in the system.
    time.sleep(random.uniform(1, 6)) # Added delay

    # Any client failure is treated the same and this is on purpose: we do not want to give much information about whether accounts may exists or not. --> give information on the frontend about pw and name requirements that may lead to failure. All client failures will yield a 400.

    return jsonify(error_response), 400




####################################
#       DELETE USER ACCOUNT        #
####################################
# NOTE: consider placing account in quarantene (in case user did not want a deletion)

@registration.route("/delete_user", methods=["POST"])
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
    # Get the JSON data from the request body 
    json_data = request.get_json()
    password = json_data["password"]
    otp = json_data.get("otp", "")
    user_agent = json_data.get("user_agent", "")

    # Standard error response
    error_response = {"response": "An error prevented account from being deleted."} 
    
    # Check if user exists
    user = svc_get_user_or_none(current_user.email, "delete_user")
    client_ip = get_client_ip(request) or ""

    # Delay response in case of wrong credentials to mitigate attacks by introducing randomized delay
    def delay_response():
        delay = random.uniform(1, 10)
        time.sleep(delay)

    if user is None:
        log_delete_user(404, "User could not be found from current_user although login_required is present.", user_agent, client_ip, 0)
        logging.warning("User deletion route failed to find current_user even though login_required decorator present. Investigation necessary.")
        delay_response()
        return jsonify(error_response), 500
        
    # Check password
    salted_password = user.salt + password + get_pepper(user.created_at)
    if not flask_bcrypt.check_password_hash(user.password, salted_password):
        log_delete_user(401, "Wrong password.", user_agent, client_ip, user.id)
        delay_response()
        return jsonify({"response": "Wrong credentials: password incorrect."} ), 401
    
    # Check OTP only if user has mfa set
    if user.mfa_enabled:
        if user.check_otp(otp) is False:
            log_delete_user(401, "Incorrect OTP.", user_agent, client_ip, user.id)
            delay_response()
            return jsonify({"response": "Wrong credentials: OTP incorrect or expired."}), 401
    
    # Temporarily save some user details for later:
    user_id = user.id
    name=user.name
    email=user.email

    # Credentials correct: delete user
    del_outcome = svc_delete_user_account(user)

    user_deleted = del_outcome["success"]
    log_code = del_outcome["log_code"]
    log_text = del_outcome["log_text"] 

    log_delete_user(log_code, log_text, user_agent, client_ip, user_id)

    if user_deleted:
        send_email_acct_deleted(name, email)
        flask_logout_user() # classic flask-login log out
        session.clear() # Flask-Session to clear session data in Redis 
        return jsonify({"response": "User deleted successfully!"}), 200
    else:
        return jsonify(error_response), 500

