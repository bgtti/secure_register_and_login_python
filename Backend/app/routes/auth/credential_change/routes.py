"""
**ABOUT THIS FILE**

auth/credential_change/routes.py contains routes responsible for authenticating a change of login credentials (ie: email and password).

Here you will find the following routes:
- **reset_password_token** route will send a token to the user email to reset the password
- **change_password** route will change the user's password
- **change_email** route will change the user account's email or initiate the change process
- **email_change_token_validation** route is the second step necessary to change the account's email for validated accounts

The format of data sent by the client is validated using Json Schema. 
Reoutes receiving client data are decorated with `@validate_schema(name_of_schema)` for this purpose. 

------------------------
## More information

Email and Password verification relies on token management. For more information about how tokens are used, please refer to the Token db model at app/models/token.py
"""
############# IMPORTS ##############

# Python/Flask libraries
import logging
import random
import time
from flask import  request, jsonify
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

# Utilities
from app.utils.bot_detection.bot_detection import bot_caught
from app.utils.constants.enum_class import TokenPurpose, modelBool, PasswordChangeReason
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.utils.detect_html.detect_html import check_for_html
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.profanity_check.profanity_check import has_profanity
from app.utils.token_utils.group_id_creation import get_group_id
from app.utils.token_utils.verification_urls import create_verification_url
from app.utils.salt_and_pepper.helpers import get_pepper

# Auth helpers
from app.routes.auth.helpers_auth import (
    anonymize_email,
    check_if_user_blocked, 
    get_hashed_pw, 
    get_user_or_none,
    reset_user_session)

from app.routes.auth.email_helpers import (
    send_email_admin_blocked,
    send_otp_email,
)

# Credential change helpers 
from app.routes.auth.credential_change.email import (
    send_pw_reset_email,
    send_pw_change_sucess_email,
    send_email_change_token_emails,
    send_email_change_sucess_emails
)

from app.routes.auth.credential_change.helpers import validate_and_verify_signed_token

from app.routes.auth.credential_change.log import (
    log_reset_password_token,
    log_password_change,
    log_email_change,
    log_email_token_validation
)


from app.routes.auth.credential_change.schemas import (
    reset_password_token_schema,
    change_password_schema,
    change_email_schema,
    change_email_token_validation_schema
)

# Blueprint
from . import credential_change


############# ROUTES ###############


####################################
#       RESET USER'S PASSWORD      #
####################################

@credential_change.route("/reset_password_token", methods=["POST"]) # TODO: proper logging
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
    user_agent = json_data.get("user_agent", "") 

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Standard response
    error_response = {"response": "There was an error resetting the user's password."}
    success_response = {"response": "Password reset request sent if email exists."}

    # Filter out bots
    if len(honeypot) > 0:
        log_reset_password_token(418, f"Email: {email}.", user_agent, client_ip, 0)
        bot_caught(request, "reset_password_token")
        return jsonify(error_response), 418
    
    # Check if user exists
    user = get_user_or_none(email, "reset_password_token")

    # Delay response in case user does not exist
    # Reason: mitigating timing attacks by introducing randomized delay
    if user is None:
        log_reset_password_token(404, f"Email: {email}.", user_agent, client_ip, 0)
        delay = random.uniform(1, 15)
        time.sleep(delay)
        return jsonify(success_response) # not sending error to create ambiguity
    
    # Check if user is blocked
    user_is_blocked = False

    blocked_status = check_if_user_blocked(user, client_ip)
    user_is_blocked = blocked_status["blocked"]

    if user_is_blocked:
        if blocked_status["temporary_block"] is False:
            log_reset_password_token(403, f"Temporary block.", user_agent,client_ip, user.id)
            send_email_admin_blocked(user.name, user.email)
        else:
            log_reset_password_token(403, f"Admin block.", user_agent,client_ip, user.id)
        return jsonify(success_response) # not sending error to create ambiguity
    
    try:
        token = Token(user_id=user.id, purpose=TokenPurpose.PW_RESET, ip_address=client_ip, user_agent=user_agent) 
        db.session.add(token)
        db.session.commit()

    except Exception as e:
        logging.error(f"Token creation failed. Error: {e}")
        log_reset_password_token(500, f"Token creation failed. {str(e)}", user_agent,client_ip, user.id)
        return jsonify(error_response), 500
    
    url_data = create_verification_url(token.token, TokenPurpose.PW_RESET)

    try:
        mail_sent = send_pw_reset_email(user.name, user.email, url_data["url"], url_data["token_url"], url_data["signed_token"] )
    except Exception as e:
        logging.error(f"Failed to send token email. Error: {e}")
        log_reset_password_token(500, f"{str(e)}", user_agent,client_ip, user.id)
        return jsonify(error_response), 500
    
    if not mail_sent:
        log_reset_password_token(500, f"Email could not be sent.", user_agent,client_ip, user.id)
        return jsonify(error_response), 500
    
    log_reset_password_token(200, "", user_agent,client_ip, user.id)
    return jsonify(success_response)

####################################
#      CHANGE USER'S PASSWORD      #
####################################

@credential_change.route("/change_password", methods=["POST"]) # TODO: proper logging
@validate_schema(change_password_schema)
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
    signed_token = json_data.get("signed_token", "")
    honeypot = json_data["honeypot"]
    user_agent = json_data.get("user_agent", "") #TODO log this in event

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Standard response
    error_response = {"response": "There was an error changing the user's password."}

    # Filter out bots
    if len(honeypot) > 0:
        bot_caught(request, "login")
        log_password_change(418, "", user_agent, client_ip, 0)
        return jsonify(error_response), 418
    
    #TODO: make MFA required for admins to change password

    #TODO: break down this function is smaller and easier to digest helper functions
    
    # REASON: PW RESET
    if pw_change_reason == PasswordChangeReason.RESET.value:

        # validate token
        res = validate_and_verify_signed_token(signed_token, TokenPurpose.PW_RESET, "change_password", False)

        if res["status"] != 200:
            log_password_change(401, f"Token validation failed to reset password. Token validation status: {res["status"]}. Message: {res["message"]}", user_agent, client_ip, 0)
            return jsonify({"response": res["message"]}), res["status"]

        # Get user from token
        token = res["token"]
        user = token.user
    
    # REASON: PW CHANGE
    else:
        if pw_change_reason != PasswordChangeReason.CHANGE.value:
            logging.error("Error in change_password function: PasswordChangeReason not valid.")
            log_password_change(400, f"Invalid input: password change reason does not meet options. Received: {pw_change_reason}", user_agent, client_ip, 0)
            return jsonify(error_response), 400

        # Get the user
        if current_user.is_anonymous:
            log_password_change(401, "Current user is anonymous. Log-in required for password change.", user_agent, client_ip, 0)
            return jsonify({"response": "Unauthorized: log in to change password."}), 401
        user = get_user_or_none(current_user.email, "change_password")

        # Check that old password is correct
        salted_password = user.salt + old_password + get_pepper(user.created_at)
        if not flask_bcrypt.check_password_hash(user.password, salted_password):
            log_password_change(401, "Wrong password provided.", user_agent, client_ip, user.id)
            return jsonify({"response": "Unauthorized: incorrect credentials."}), 401
        
    # Check new password
    if is_first_factor:
        hashed_password = get_hashed_pw(new_password, user.created_at, user.salt) 
        if not hashed_password:
            log_password_change(400, "New password does not meet criteria.", user_agent, client_ip, user.id)
            return jsonify({"response": "New password does not meet criteria."}), 400
        try:
            user.new_password = hashed_password
            db.session.commit()
        except Exception as e:
            db.session.rollback() 
            logging.error(f"User password change failed. Error: {e}") 
            log_password_change(500, f"Error: {str(e)}", user_agent, client_ip, user.id)
            return jsonify(error_response), 500   

    # Check if user has mfa enabled
    mfa_enabled = user.mfa_enabled == modelBool.TRUE

    if mfa_enabled:
        # PW reset has two factors checked in separate requests when MFA is enabled
        if is_first_factor and pw_change_reason == PasswordChangeReason.RESET.value:
            # Send OTP to recovery email so user can proceed to second MFA step
            recovery_email = user.recovery_email
            if recovery_email is None:
                log_password_change(500, f"Error: {str(e)}", user_agent, client_ip, user.id)
                return jsonify({"response": "MFA enabled, but no recovery email on record. Contact support."}), 422
            try:
                    otp = user.generate_otp()
                    send_otp_email(user.name, otp, recovery_email)
            except Exception as e:
                log_password_change(500, f"OTP could not be generated. Error: {str(e)}", user_agent, client_ip, user.id)
                logging.warning(f"Failed to generate OTP and/or send it per email. Error: {e}") 
                return jsonify(error_response), 500
            log_password_change(202, f"OTP sent to recovery email: {anonymize_email(recovery_email)}.", user_agent, client_ip, user.id)
            return jsonify({"response": f"OTP sent to recovery email: {anonymize_email(recovery_email)}."}), 202
        # Both PW reset and PW change will check OTP as second MFA step
        else:
            if otp == "" or user.check_otp(otp) is False:
                log_password_change(401, "OTP invalid or expired.", user_agent, client_ip, user.id)
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
            log_password_change(500, f"Error: {str(e)}", user_agent, client_ip, user.id)
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

    log_password_change(200, "", user_agent, client_ip, user.id)

    success_response = {"response": "Password changed successfully!"} 
    
    return jsonify(success_response)

####################################
#          CHANGE EMAIL            #
####################################

@credential_change.route("/change_email", methods=["POST"])  # TODO: proper logging
@login_required
@validate_schema(change_email_schema) 
@limiter.limit("5/day")
def change_email():
    """
    change_email() -> JsonType
    ----------------------------------------------------------

    If the user's account is not validated, the email change
    will be accepted in this function (should the request be valid).
    In this case, a successful response will return 200.

    If the user's account has been validated, the email change process 
    begins with this function, which will store the new email,
    issue validation tokens, and send those tokens per email.
    A successfull response in this case will be 202.
    Another route must be used to validate the email change tokens so that
    the email change does in fact take place.

    The process is independent of MFA, but rather based on the account
    email being validated. The reason for this is that if the account
    has not been validated before, the user's email may be invalid or
    incorrect (which means the user may not receive confirmation emails).
    
    Returns Json object containing the response:
    - "response" value is always included, containing the message detailing the result.  

    ----------------------------------------------------------
    **Response example:**

    An error may yield:
    ```python
        "response": "There was an error changing email. Please contact support."
    ``` 

    A successful response may yield:

    ```python
        "response": "Email changed successfully!."
    ``` 

    or a 202

    ```python
        "response": "Check your email to complete email change process!"
    ``` 
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    password = json_data["password"]
    new_email = json_data["new_email"]
    user_agent = json_data.get("user_agent", "") 

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Get user
    user = get_user_or_none(current_user.email, "change_email")
    if user is None:
        log_email_change(500, "Session did not return current user.", user_agent, client_ip, 0)
        return jsonify({"response": "Error: user not found."}), 500 #500 instead of 401 because @login_required so current_user should exist
    
    # Check password
    salted_password = user.salt + password + get_pepper(user.created_at)
    if not flask_bcrypt.check_password_hash(user.password, salted_password):
        log_email_change(401, "Incorrect password.", user_agent, client_ip, user.id)
        return jsonify({"response": "Unauthorized: incorrect password."}), 401
    
    # Check new email to see if its like the recovery email or current email
    if new_email == user.email:
        log_email_change(400, f"New email must be different to current email. New email: {new_email}", user_agent, client_ip, user.id)
        return jsonify({"response": "Error: new email is the same as current email."}), 400
    if new_email == user.recovery_email:
        log_email_change(400, "New email must be different to recovery email.", user_agent, client_ip, user.id)
        return jsonify({"response": "Error: new email cannot be the same as the recovery email."}), 400
    
    # Check that new email is not already in DB
    user_exists = get_user_or_none(new_email, "change_email")
    if user_exists is not None:
        log_email_change(409, f"New email already exists in server. New email: {new_email}", user_agent, client_ip, user.id)
        # Reason for rejection should not be obvious in this case for security reasons
        return jsonify({"response": "There was an error changing email. Please contact support."}), 400 
    
    # Check new email for html and profanity
    flag = False
    html_in_email = check_for_html(new_email, "email_change - new_email field", new_email)

    if html_in_email:
        flag = "YELLOW"
        log_email_change(207, "HMTL detected in new email.", user_agent, client_ip, user.id)
    else:
        profanity_in_email = has_profanity(new_email)
        if profanity_in_email:
            flag = "PURPLE"
            log_email_change(207, "Profanity detected in new email.", user_agent, client_ip, user.id)
    
    # General error response
    error_response = {"response": "There was an error changing email. Please try again."}
    
    # Save the new email to the user's new_email field
    try:
        user.new_email = new_email
        if flag:
            user.flag_change(flag)
        db.session.commit()
    except Exception as e:
        db.session.rollback() 
        logging.error(f"User email change failed. Error: {e}")
        log_email_change(500, f"Failure in attempt to flag user. {str(e)}", user_agent, client_ip, user.id)
        return jsonify(error_response), 500

    # Define the emails
    new_email = user.new_email
    old_email = user.email
    
    # If the user is not verified, proceed to change email
    if user.check_if_account_is_verified() is False:
        try: 
            email_was_changed = user.change_email() 

            if email_was_changed:
                db.session.commit()
                # If success emails fail to be sent, no error shall be returned 
                try:
                    send_email_change_sucess_emails(user.name, old_email, new_email)
                except Exception as e:
                    logging.warning(f"Failed to send email change success notification. Error: {e}") 
                
                # Log user out of old sessions and start a new one
                reset_user_session(user)
                flask_logout_user()
                flask_login_user(user)

                # Log change
                log_email_change(200, f"Email changed from {old_email} to {new_email}.", user_agent, client_ip, user.id)

                # Return
                return jsonify({"response": "Email changed successfully!"}), 200
            else:
                logging.error(f"Email change failed. Possible reason: no new_email stored in User.")
                log_email_change(500, "Failure possibly attributed to the 'new email' missing in the database.", user_agent, client_ip, user.id)
                return jsonify(error_response), 500
        except Exception as e:
                db.session.rollback()
                logging.error(f"Failed to change email. Error: {e}")
                log_email_change(500, f"Error: {str(e)}", user_agent, client_ip, user.id)
                return jsonify(error_response), 500

    # If user is verified, issue a token to start the verification process
    try:
        token_group = get_group_id(user.id)
        token_old_email = Token(user_id=user.id, group_id=token_group, purpose=TokenPurpose.EMAIL_CHANGE_OLD_EMAIL, ip_address=client_ip, user_agent=user_agent) 
        token_new_email = Token(user_id=user.id, group_id=token_group, purpose=TokenPurpose.EMAIL_CHANGE_NEW_EMAIL, ip_address=client_ip, user_agent=user_agent) 
        db.session.add(token_old_email)
        db.session.add(token_new_email)
        db.session.commit()
    except Exception as e:
        logging.error(f"New email/Token could not be added to user. Error: {e}")
        log_email_change(500, f"New email/Token could not be added to user. Error: {str(e)}", user_agent, client_ip, user.id)
        return jsonify(error_response), 500
    
    # Send tokens per email
    url_data_old = create_verification_url(token_old_email.token, TokenPurpose.EMAIL_CHANGE_OLD_EMAIL)
    url_data_new = create_verification_url(token_new_email.token, TokenPurpose.EMAIL_CHANGE_NEW_EMAIL)

    send_email_change_token_emails(
        user.name,
        old_email,
        new_email,
        url_data_old["url"],
        url_data_new["url"],
        url_data_old["token_url"],
        url_data_new["token_url"],
        url_data_old["signed_token"],
        url_data_new["signed_token"]
        )
    
    # Log
    log_email_change(202, f"Tokens sent to current email ({old_email}) and desired new email ({new_email})", user_agent, client_ip, user.id)

    
    # Return 202: user will have to verify the tokens to complete email change
    return jsonify({"response": "Check your email to complete email change process!"}), 202

####################################
#  VALIDATE TOKEN FOR EMAIL CHANGE #
####################################

@credential_change.route('/email_change_token_validation', methods=['POST']) # TODO: proper logging
@limiter.limit("5/day")
@validate_schema(change_email_token_validation_schema)
def email_change_token_validation():
    """
    email_change_token_validation() -> JsonType 

    ----------------------------------------------------------
    Validates a token to change the user's email or password.
    This route is used as the second step of the email change process
    when a user has a validated account.

    Two tokens should be validated for an email change to be successfull:
    - the token sent to the current email address
    - the token sent to the new email address

    When only one token is validated, route will return a 202.
    When both tokens have been validated, route will return a 200 response.
    
    Returns Json object containing the response:
    - "response" value is always included, containing the message detailing the result.

    ----------------------------------------------------------
    **Response example:**

    An error may yield:
    ```python
        "response": "Invalid or expired token."
    ``` 

    A successful response may yield:

    ```python
        "response": "Email changed successfully!"
    ``` 

    or a 202

    ```python
        "response": "Token validated. One token validation missing."
    ```  
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    signed_token = json_data["signed_token"]
    purpose = json_data["purpose"]
    user_agent = json_data.get("user_agent", "") 

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Standard error response
    error_response = { "response": "Invalid or expired token." }
    
    token_purpose = TokenPurpose(purpose) 
    
    # validate token
    res = validate_and_verify_signed_token(signed_token, token_purpose, "email_change_token_validation", True) 

    if res["status"] != 200:
        log_email_token_validation(500, f"{res["message"]}", user_agent, client_ip, 0)
        return jsonify({"response": res["message"]}), res["status"]
    
    # Token validated, now take appropriate action

    # Get user from token
    token = res["token"]
    user = token.user
        
    # Two tokens are issued for an email change: one to verify the old and another to verify the new email   
    related_tokens = Token.query.filter_by(group_id=token.group_id).all()

    if len(related_tokens) != 2:
        log_message = f"Invalid number of related tokens for group_id: {token.group_id}. 2 are required for email changes"
        logging.error(log_message)
        log_email_token_validation(500, log_message, user_agent, client_ip, user.id)
        return jsonify(error_response), 500
        
    # Check to see if the other token has already been validated
    second_token = next((t for t in related_tokens if t != token), None)
    if not second_token:
        log_message = f"Second token not found for group_id: {token.group_id}."
        logging.error(log_message)
        log_email_token_validation(500, log_message, user_agent, client_ip, user.id)
        return jsonify(error_response), 500
    
    if second_token.token_verified == modelBool.TRUE:
        # User has validated both required tokens and may now change emails
        try: 
            new_email = user.new_email
            old_email = user.email
            email_was_changed = user.change_email() 
            if email_was_changed:
                # Delete tokens after email change
                db.session.delete(token)
                db.session.delete(second_token)
                db.session.commit()
                # Send emails confirming email change
                try:
                    send_email_change_sucess_emails(user.name, old_email, new_email)
                except Exception as e:
                    logging.warning(f"Failed to send email change success notification. Error: {e}") 
            else:
                log_message = f"Failed to change email possibly because no new email was found in the database."
                logging.error(log_message)
                log_email_token_validation(500, log_message, user_agent, client_ip, user.id)
                return jsonify(error_response), 500
        except Exception as e:
            db.session.rollback()
            log_message = f"Failed to change email. Error: {str(e)}"
            logging.error(log_message)
            log_email_token_validation(500, log_message, user_agent, client_ip, user.id)
            return jsonify(error_response), 500
    else:
        log_email_token_validation(202, "", user_agent, client_ip, user.id)
        return jsonify({"response": "Token validated. One token validation missing."}), 202
    
    # Reset user sessions and if user is logged in, log out
    reset_user_session(user)
    if not current_user.is_anonymous:
        flask_logout_user()

    # Log
    log_email_token_validation(200, f"Previous email: {old_email}. New email: {new_email}", user_agent, client_ip, user.id)

    response_data ={ "response":"Email was changed successfully!" }
    return jsonify(response_data), 200
