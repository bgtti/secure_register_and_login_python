"""
**ABOUT THIS FILE**

auth/routes_credential_change.py contains routes responsible for authenticating a change of longin credentials.
Here you will find the following routes:
- **
- **reset_password** route will change the user's password
- **request_auth_change** route is the first step necessary to change the account's email or password #TODO: pw missing
- **request_token_validation** route is the second step necessary to change the account's email or password #TODO: pw missing

The format of data sent by the client is validated using Json Schema. 
Reoutes receiving client data are decorated with `@validate_schema(name_of_schema)` for this purpose. 

------------------------
## More information

Email verification relies on token management. For more information about how tokens are used, please refer to the Token db model at app/models/token.py
"""
############# IMPORTS ##############

# Python/Flask libraries
import logging
import random
import time
from flask import Blueprint, request, jsonify, session
from flask_login import (
    current_user,
    login_user as flask_login_user,
    login_required,
    logout_user as flask_logout_user,
)

# Extensions
from app.extensions.extensions import db, limiter, flask_bcrypt

# Database models
from app.models.token import Token
from app.models.user import User

# Utilities
from app.utils.bot_detection.bot_detection import bot_caught
from app.utils.constants.enum_class import TokenPurpose, modelBool, PasswordChangeReason, AuthMethods
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.utils.detect_html.detect_html import check_for_html
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.profanity_check.profanity_check import has_profanity
from app.utils.token_utils.group_id_creation import get_group_id
from app.utils.token_utils.sign_and_verify import verify_signed_token
from app.utils.token_utils.verification_urls import create_verification_url
from app.utils.salt_and_pepper.helpers import get_pepper

# Auth helpers
from app.routes.auth.auth_helpers import check_if_user_blocked, get_hashed_pw, reset_user_session, user_name_is_valid, get_user_or_none, reset_user_session, anonymize_email
from app.routes.auth.auth_helpers_credential_change import validate_and_verify_signed_token
from app.routes.auth.email_helpers import (
    send_email_admin_blocked,
    send_otp_email,
    send_email_change_emails,
    send_email_change_sucess_emails,
)
from app.routes.auth.email_helpers_credential_change import (
    send_pw_reset_email,
    # send_email_change_emails,
    # send_email_change_sucess_emails,
    # send_pw_change_email,
    send_pw_change_sucess_email,
)
from app.routes.auth.schemas import (
    reset_password_token_schema,
    change_name_schema,
    req_auth_change_schema,
    req_token_validation_schema,
)

# Blueprint
from . import auth


############# ROUTES ###############


####################################
#       RESET USER'S PASSWORD      #
####################################

@auth.route("/reset_password_token", methods=["POST"])
@validate_schema(reset_password_token_schema) 
@limiter.limit("1/minute; 5/day")
def reset_password_token(): 
    """
    reset_password_token() -> JsonType
    ----------------------------------------------------------

    Route creates a token and sends it per email so that user can reset password. 
    
    Returns Json object containing the response:
    - "response" value is always included.  

    ----------------------------------------------------------
    **Response example:**

    ```python
        "response": "Password reset request sent if email exists."
    ``` 

    ```python
        "response": "There was an error resetting the user's password."
    ``` 
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    email = json_data["email"]
    honeypot = json_data["honeypot"]
    user_agent = json_data.get("user_agent", "") #TODO log this in event

    # Standard response
    error_response = {"response": "There was an error resetting the user's password."}
    success_response = {"response": "Password reset request sent if email exists."}

    # Filter out bots
    if len(honeypot) > 0:
        bot_caught(request, "login")
        return jsonify(error_response), 418
    
    # Check if user exists
    user = get_user_or_none(email, "login")

    # Delay response in case user does not exist
    # Reason: mitigating timing attacks by introducing randomized delay
    if user is None:
        delay = random.uniform(1, 15)
        time.sleep(delay)
        return jsonify(success_response) # not sending error to create ambiguity
    
    # Get the request ip
    client_ip = get_client_ip(request)
    
    # Check if user is blocked
    user_is_blocked = False

    blocked_status = check_if_user_blocked(user, client_ip)
    user_is_blocked = blocked_status["blocked"]

    if user_is_blocked:
        if blocked_status["temporary_block"] is False:
            send_email_admin_blocked(user.name, user.email)
        return jsonify(success_response) # not sending error to create ambiguity
    
    try:
        token = Token(user_id=user.id, purpose=TokenPurpose.PW_RESET, ip_address=client_ip, user_agent=user_agent) 
        db.session.add(token)
        db.session.commit()

    except Exception as e:
        logging.error(f"Token creation failed. Error: {e}")
        return jsonify(error_response), 500
    
    url_data = create_verification_url(token.token, TokenPurpose.PW_RESET)

    try:
        mail_sent = send_pw_reset_email(user.name, user.email, url_data["url"], url_data["token_url"], url_data["signed_token"] )
    except Exception as e:
        logging.error(f"Failed to send token email. Error: {e}")
        return jsonify(error_response), 500
    
    if not mail_sent:
        return jsonify(error_response), 500
    
    return jsonify(success_response)

####################################
#      CHANGE USER'S PASSWORD      #
####################################

@auth.route("/change_password", methods=["POST"])
@validate_schema(reset_password_token_schema) #TODO: new schema necessary
@limiter.limit("1/minute; 5/day")
def change_password(): 
    """
    change_password() -> JsonType
    ----------------------------------------------------------

    The password can be changed in two settings:
    - The user requests a password reset due to forgotten password
    - The logged in user changes password

    The password reset change should validate a token. If the user has MFA enabled,
    then route shall return a 202 upon token validation, and a second request shall
    validate an OTP sent to the user's recovery email. Upon second factor validation,
    this OTP will be validated for the password to be changed.

    If the logged in user decides to change the password, the current (or "old") password
    shall be validated. If the user has MFA enabled, the front end should have sent an OTP to the 
    user's email address, and this OTP will be validated as the second step in a unique request. 
    
    Returns Json object containing the response:
    - "response" value is always included, containing the message detailing the result.  

    ----------------------------------------------------------
    **Response example:**

    An error may yield:
    ```python
        "response": "There was an error changing the user's password."
    ``` 

    A successful response may yield:

    ```python
        "response": "Password changed successfully!."
    ``` 

    or a 202

    ```python
        "response": "OTP sent to recovery email: c******@g****.com."
    ``` 
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    is_first_factor = json_data["is_first_factor"]
    new_password = json_data["new_password"]
    old_password = json_data.get("old_password", "")
    pw_change_reason = json_data["pw_change_reason"]
    otp = json_data.get("otp", "")
    signed_token = json_data.get("token", "")
    honeypot = json_data["honeypot"]
    user_agent = json_data.get("user_agent", "") #TODO log this in event

    # Standard response
    error_response = {"response": "There was an error changing the user's password."}

    # Filter out bots
    if len(honeypot) > 0:
        bot_caught(request, "login")
        return jsonify(error_response), 418
    
    #TODO: make MFA required for admins to change password

    #TODO: break down this function is smaller and easier to digest helper functions
    
    # REASON: PW RESET
    if pw_change_reason == PasswordChangeReason.RESET.value:

        # validate token
        res = validate_and_verify_signed_token(signed_token, PasswordChangeReason.RESET, "change_password", False)

        if res["status"] != 200:
            return jsonify({"response": res["message"]}), res["status"]

        # Get user from token
        token = res["token"]
        user = token.user
    
    # REASON: PW CHANGE
    else:
        if pw_change_reason != PasswordChangeReason.CHANGE.value:
            logging.error("Error in change_password function: PasswordChangeReason not valid.")
            return jsonify(error_response), 400

        # Get the user
        if current_user.is_anonymous:
            return jsonify({"response": "Unauthorized: log in to change password."}), 401
        user = get_user_or_none(current_user.email, "change_password")

        # Check that old password is correct
        salted_password = user.salt + old_password + get_pepper(user.created_at)
        if not flask_bcrypt.check_password_hash(user.password, salted_password):
            return jsonify({"response": "Unauthorized: incorrect credentials."}), 401
        
    # Check new password
    if is_first_factor:
        hashed_password = get_hashed_pw(new_password, user.created_at, user.salt) 
        if not hashed_password:
            return jsonify({"response": "New password does not meet criteria."}), 400
        try:
            user.new_password = new_password
            db.session.commit()
        except Exception as e:
            db.session.rollback() 
            logging.error(f"User password change failed. Error: {e}") 
            return jsonify(error_response), 500   

    # Check if user has mfa enabled
    mfa_enabled = user.mfa_enabled == modelBool.TRUE

    if mfa_enabled:
        # PW reset has two factors checked in separate requests when MFA is enabled
        if is_first_factor and pw_change_reason == PasswordChangeReason.RESET.value:
            # Send OTP to recovery email so user can proceed to second MFA step
            recovery_email = current_user.recovery_email
            if recovery_email is None:
                return jsonify({"response": "MFA enabled, but no recovery email on record. Contact support."}), 422
            try:
                    otp = user.generate_otp()
                    send_otp_email(user.name, otp, recovery_email)
            except Exception as e:
                logging.warning(f"Failed to generate OTP and/or send it per email. Error: {e}") 
                return jsonify(error_response), 500
            return jsonify({"response": f"OTP sent to recovery email: {anonymize_email(recovery_email)}."}), 202
        # Both PW reset and PW change will check OTP as second MFA step
        else:
            if otp == "" or user.check_otp(otp) is False:
                return jsonify({"response": "Unauthorized: OTP invalid or expired."}), 401

    try: 
        user.password = user.new_password
        user.new_password = None
        # PW reset: token needs to be deleted before proceeding
        if pw_change_reason == PasswordChangeReason.RESET.value:
            db.session.delete(token)
        db.session.commit() 
    except Exception as e:
            db.session.rollback() 
            logging.error(f"User password change failed. Error: {e}") 
            return jsonify(error_response), 500 

    # Send email confirming password changed 
    send_pw_change_sucess_email(user.name, user.email)
    
    # If user was logged in, log user out and login user in again
    if not current_user.is_anonymous:
        reset_user_session(user)
        flask_logout_user()
        flask_login_user(user)
    else:
        reset_user_session(user) 

    success_response = {"response": "Password changed successfully!"} 
    
    return jsonify(success_response)

    



####################################
#      CHANGE EMAIL/PW (STEP 1)    #
####################################

@auth.route("/request_auth_change", methods=["POST"]) # TODO: TEST
@login_required
@validate_schema(req_auth_change_schema)
@limiter.limit("5/day")
def request_auth_change(): # TODO --> Add to logs so user actions can show in history, consider db rollbacks
    """
    **request_auth_change() -> JsonType**

    ----------------------------------------------------------
    Route receives the request to change a user's login credential (email or password)
    and sends email(s) with verification url(s) to the user. 
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "mail_sent" boolean value only included if response is "success".

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

    if change_request_type == "password":
        try:
            token = Token(user_id=user.id, purpose=TokenPurpose.PW_CHANGE, ip_address=client_ip, user_agent=user_agent) 
            db.session.add(token)
            db.session.commit()

        except Exception as e:
            logging.error(f"Token creation failed. Error: {e}")
            return jsonify(error_response), 500
        
        link = create_verification_url(token.token, TokenPurpose.PW_CHANGE)
        # mail_sent = send_pw_change_email(user.name, link, user.email)
    
    elif change_request_type == "email":
        new_email = json_data["new_email"]
        if new_email is None:
            return jsonify({"response": "New email is required."}), 400
        try:
            user.new_email = new_email
            token_group = get_group_id(user.id)
            # logging.debug(f"Creating token for EMAIL_CHANGE_OLD_EMAIL with purpose: {TokenPurpose.EMAIL_CHANGE_OLD_EMAIL}")
            token_old_email = Token(user_id=user.id, group_id=token_group, purpose=TokenPurpose.EMAIL_CHANGE_OLD_EMAIL, ip_address=client_ip, user_agent=user_agent) 
            # logging.debug(f"Creating token for EMAIL_CHANGE_NEW_EMAIL with purpose: {TokenPurpose.EMAIL_CHANGE_NEW_EMAIL}")
            token_new_email = Token(user_id=user.id, group_id=token_group, purpose=TokenPurpose.EMAIL_CHANGE_NEW_EMAIL, ip_address=client_ip, user_agent=user_agent) 
            db.session.add(token_old_email)
            db.session.add(token_new_email)
            db.session.commit()
        except Exception as e:
            logging.error(f"New email/Token could not be added to user. Error: {e}")
            return jsonify(error_response), 500
        link_old_email = create_verification_url(token_old_email.token, TokenPurpose.EMAIL_CHANGE_OLD_EMAIL)
        link_new_email = create_verification_url(token_new_email.token, TokenPurpose.EMAIL_CHANGE_NEW_EMAIL)
        mail_sent = send_email_change_emails(user.name, link_old_email, link_new_email, user.email, new_email)
    else:
        return jsonify(error_response), 400
    
    response_data ={
            "response":"success",
            "mail_sent": mail_sent,
        }
    return jsonify(response_data)

####################################
#      CHANGE EMAIL/PW (STEP 2)    #
####################################

@auth.route('/request_token_validation', methods=['POST']) # TODO: improve + logging
@limiter.limit("5/day")
@validate_schema(req_token_validation_schema)
def request_token_validation():
    """
    request_token_validation() -> JsonType 

    ----------------------------------------------------------
    Validate a token to change the user's email or password.
    
    Returns:
        JsonType: Response JSON containing:
            - "response": String status of the operation ("success" or error message).
            - "cred_changed": Boolean indicating if auth credentials were changed.
            - "signed_token": String echo of the input token.
            - "purpose": String echo purpose of the token. One of: TokenPurpose.value
            - "email_sent": Boolean whether a success email was sent to user or not

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "cred_changed": True, 
                "signed_token": "knslsknskns27t21o....", 
                "purpose": "pw_change",
                "email_sent": True
            }
    ``` 
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    signed_token = json_data["signed_token"]
    purpose = json_data["purpose"]

    # Standard error response
    error_response = {
        "response": "Invalid or expired token.",
        "cred_changed": False,
        "signed_token": signed_token,
        "purpose": purpose,
        "email_sent": False #=> TODO: whether emails are sent or not, the front end is not handling this data
        }

    # Verify token signature and timestamp
    token = verify_signed_token(signed_token, purpose)

    if not token:
        logging.info(f"Invalid or expired token could not be validated.")
        return jsonify(error_response), 400 
    
    # Fetch the token from the database
    try:
        the_token =Token.query.filter_by(token=token).first()
    except Exception as e:
        logging.error(f"Database error while fetching token. Error: {e}")
        return jsonify(error_response), 500

    if not the_token:
        logging.info(f"Verified token not found in the database.")
        return jsonify(error_response), 400 
    
    # Validate token
    try:
        if the_token.validate_token():
            db.session.commit()
        else:
            logging.info(f"Token validation failed.")
            return jsonify(error_response), 400 
    except Exception as e:
        db.session.rollback()
        logging.error(f"Database error while validating token. Error: {e}")
        return jsonify(error_response), 500
    
    # Token validated, now take appropriate action
    credentials_changed = False
    email_sent = False

    token_purpose = TokenPurpose(purpose) 

    # Case: password change
    if token_purpose == TokenPurpose.PW_CHANGE:
        new_pw = json_data["new_password"]
        if not new_pw:
            logging.error(f"No new password provided in request. Failed to change password.")
            return jsonify(error_response), 400  
        
        try: 
            user = the_token.user
            new_pw_hashed = get_hashed_pw(new_pw, user.created_at, user.salt)
            if not new_pw_hashed:
                logging.error(f"Password in request does not meet standards.")
                return jsonify(error_response), 400
            
            user.password = new_pw_hashed
            db.session.delete(the_token)
            db.session.commit()
            credentials_changed = True
            email_sent = send_pw_change_sucess_email(user.name, user.email)
        except Exception as e:
            db.session.rollback()
            logging.error(f"Failed to change password. Error: {e}")
            return jsonify(error_response), 500
        
    # Case: email change    
    else:
        related_tokens = Token.query.filter_by(group_id=the_token.group_id).all()
        if len(related_tokens) != 2:
            logging.error(f"Invalid number of related tokens for group_id: {the_token.group_id}. 2 are required for email changes")
            return jsonify(error_response), 500
        
        second_token = next((t for t in related_tokens if t != the_token), None)
        if not second_token:
            logging.error(f"Second token not found for group_id: {the_token.group_id}.")
            return jsonify(error_response), 500
        
        if second_token.token_verified == modelBool.TRUE:
            # User has validated both required tokens and may now change emails
            try: 
                user = the_token.user
                new_email = user.new_email
                old_email = user.email
                email_was_changed = user.change_email() 

                if email_was_changed:
                    db.session.delete(the_token)
                    db.session.delete(second_token)
                    db.session.commit()
                    credentials_changed = True
                    # If success emails fail to be sent, no error should be returned 
                    try:
                        email_sent = send_email_change_sucess_emails(user.name, old_email, new_email)
                    except Exception as e:
                        logging.warning(f"Failed to send email change success notification. Error: {e}") 
                else:
                    logging.error(f"Email change failed. Possible reason: no new_email stored in User.")
                    return jsonify(error_response), 500
            except Exception as e:
                db.session.rollback()
                logging.error(f"Failed to change email. Error: {e}")
                return jsonify(error_response), 500

    # Log out user from any open session in case the credentials have changed.
    if credentials_changed:
        reset_user_session(user)

    response_data ={
                "response":"success",
                "cred_changed": credentials_changed,
                "signed_token": signed_token,
                "purpose": purpose,
                "email_sent": email_sent
            }
    return jsonify(response_data), 200