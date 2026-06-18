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

**Password reset flow:**
1. request_password_reset
   - takes email
   - always returns generic 200 on normal cases
   - sends 1 code per email if non-MFA
   - sends 2 codes per email if MFA (second code goes to recovery email)

2. reset_password
   - takes email, new_password, security_code, optional second_code
   - backend checks user.mfa_enabled
   A) If MFA user and second_code missing: will return 202 
        => FE shows second security code field
        => FE resubmits reset_password
        => BE validades both codes
   B) If not MFA user: returns 200 if ok

**Email change flow:**
1. request_email_change
    - takes new email and password 
    A) If non-MFA user and email not verified: sends code to new email
    B) If non-MFA user with verified email: sends code to email and new email
    C) If MFA user: sends code to email and new email

2. change_email
    - takes security code(s)
    - validates code(s)
    - sends out emails notifying the email has changed to both new and old emails
    - if MFA users: sends email notifying the email has changed to recovery email


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
from app.extensions.extensions import limiter


# Constants
# from app.constants.auth_password_change import PasswordChangeReason

# Utilities
# from app.common.bot_detection.bot_detection import bot_caught
# from app.common.constants.enum_class import TokenPurpose, modelBool, PasswordChangeReason
from app.common.custom_decorators.json_schema_validator import validate_schema
from app.common.detect_html.detect_html import check_for_html
from app.common.ip_utils.ip_address_validation import get_client_ip
from app.common.profanity_check.profanity_check import has_profanity
from app.common.token_utils.group_id_creation import get_group_id
# from app.common.token_utils.verification_urls import create_verification_url
from app.common.salt_and_pepper.helpers import get_pepper

# Services
from app.services.auth.user_block_service import svc_check_if_user_blocked
from app.services.auth.user_credential_change import (
    svc_change_user_password,
    svc_check_auth_change_block_status,
    svc_record_failed_auth_change_attempt,
    svc_reset_new_email,
    svc_save_new_email,
    svc_change_email
    )
from app.services.auth.user_otp_and_pw_service import svc_is_pw_or_otp_valid
from app.services.auth.user_security_code_service import (
    svc_generate_security_code, 
    svc_reset_security_codes,
    svc_validate_security_codes
    )
from app.services.user.user_service import svc_get_user_or_none
from app.services.auth.user_session_service import svc_reset_user_session
from app.services.bot.bot_service import svc_bot_caught


# from app.services.auth.token_service import svc_create_token, svc_validate_and_verify_signed_token


# Email services
from app.emails.auth.user_blocked_email import send_admin_blocked_email, send_temporarily_blocked_email
from app.emails.auth.credential_change import (
    send_pw_change_success_email,
    send_cred_change_block_email,
    send_pw_reset_request_email,
    send_email_reset_request_email,
    send_email_change_success_email
)

from app.routes.auth.credential_change.log import (
    log_password_change,
    log_request_reset_password,
    log_reset_password,
    log_request_change_email,
    log_change_email
)


from app.routes.auth.credential_change.schemas import (
    change_password_schema,
    request_password_reset_schema,
    reset_password_schema,
    request_change_email_schema,
    change_email_schema
)

# Blueprint
from . import credential_change


############# ROUTES ###############

####################################
#      CHANGE USER'S PASSWORD      #
####################################

@credential_change.route("/change_password", methods=["POST"]) 
@login_required
@validate_schema(change_password_schema)
@limiter.limit("2/minute; 10/hour; 50/day")
def change_password(): 
    """
    change_password() -> JsonType
    ----------------------------------------------------------

    The password can only be changed if user is logged in.
    Else, user should choose the reset password route.

    If the logged in user decides to change the password, the user can do so either using the old password or an OTP. 
    If the user has MFA enabled, both are required: the front end should have sent an OTP to the 
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
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    new_password = json_data["new_password"]
    old_password = json_data.get("old_password", "")
    otp = json_data.get("otp", "")
    user_agent = json_data.get("user_agent", "")
    honeypot = json_data["honeypot"] #TODO: rename

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Standard response
    error_response = {"response": "There was an error changing the user's password."}

    # Filter out bots
    if len(honeypot) > 0:
        svc_bot_caught(request, "login")
        log_password_change(418, "Honeypot trigger", user_agent, client_ip, 0)
        return jsonify(error_response), 202 #TODO: ambiguity in response

    user = svc_get_user_or_none(current_user.email, "change_password")
    if not user:
        log_password_change(404, "User not found during password change.", user_agent, client_ip, 0)
        return jsonify(error_response), 404

    # Check if the user is blocked from changing credentials (too many failed attempts)
    if svc_check_auth_change_block_status(user):
        log_password_change(403, f"Blocked from changing credentials. Previous failed attempts: {user.auth_change_attempts}.", user_agent, client_ip, user.id)
        if user.auth_change_attempts == 5 or user.auth_change_attempts == 10:
            # Send email informing about the block
            send_cred_change_block_email(user.name, user.email, user.auth_change_attempts)
        return jsonify({"response": "Unauthorized: temporarily blocked from changing credentials due to too many failed attempts."}), 403

    # Check credentials

    def reject(log_message, res_message):
        svc_record_failed_auth_change_attempt(user)
        log_password_change(401, log_message, user_agent, client_ip, user.id)
        return jsonify({"response": res_message}), 401

    if not old_password and not otp:
        return reject("Neither password nor otp provided.", "Unauthorized: lacking credentials.")
    
    pw_ok = False
    otp_ok = False

    if old_password:
        pw_ok = svc_is_pw_or_otp_valid(user, old_password, "password")

    if otp:
        otp_ok = svc_is_pw_or_otp_valid(user, otp, "otp")

    if (old_password and otp) and (not pw_ok or not otp_ok):
        # non-MFA users shouldn't be sending both BUT if they do - treat like MFA
        # reject even if MFA not enabled: ambiguity = risk
        log_msg = f"Password valid = {pw_ok}, OTP valid = {otp_ok}, MFA enabled = {user.mfa_enabled}."
        return reject(log_msg, "Unauthorized: Password and/or OTP invalid.")
    
    if user.mfa_enabled and (not otp or not old_password):
        return reject("MFA enabled: one factor missing.", "Unauthorized: One authentication factor missing.")
    
    if not pw_ok and not otp_ok:
        return reject(
                f"Credential check failed. Password valid = {pw_ok}, OTP valid = {otp_ok}.",
                "Unauthorized: password or OTP invalid."
            )    
            
    # Check new password
    pw_change = svc_change_user_password(user, new_password)

    log_password_change(pw_change["log_code"], pw_change["log_text"], user_agent, client_ip, user.id)

    if pw_change["log_code"] == 500:
        return jsonify({"response": "Server error: password could not be changed."}), 500
    if pw_change["log_code"] == 400:
        svc_record_failed_auth_change_attempt(user)
        return jsonify({"response": "Password could not be changed: check new password input."}), 400
    
    # Invalidate other sessions and login the user again
    svc_reset_user_session(user)
    flask_logout_user()
    flask_login_user(user) 

    # Send email confirming password changed 
    send_pw_change_success_email(user.name, user.email)

    success_response = {"response": "Password changed successfully!"} 
    
    return jsonify(success_response)

########################################################################################

####################################
#      REQUEST PASSWORD RESET      #
####################################

@credential_change.route("/request_password_reset", methods=["POST"]) 
@validate_schema(request_password_reset_schema) 
@limiter.limit("2/minute; 10/hour; 50/day")
def request_password_reset(): 
    """
    request_password_reset() -> JsonType
    ----------------------------------------------------------

    Route creates a security code and sends it per email so that user can reset password.
    If user has MFA enabled, a second security code will be sent to recovery email as well. 
    
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
    user_agent = json_data.get("user_agent", "")
    honeypot = json_data["honeypot"] #TODO: rename 

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Standard response
    success_response = {"response": "Password reset request sent if email exists."}
    error_response = {"response": "There was an error resetting the user's password."}
    error_429 = {"response": "Too many failed attempts. Please try again later."}
    error_403 = {"response": "Unauthorized: please contact site admin for more information."}

    # Filter out bots
    if len(honeypot) > 0:
        # NOTE: consider a way to allow users to reset even if honey pot implemented
        log_request_reset_password(418, f"Bot caught in honeypot. Email: {email}.", user_agent, client_ip, 0)
        svc_bot_caught(request, "request_password_reset")
        return jsonify(error_response), 418 #TODO: honeypot breaks anbiguity of response
    
    # Check if user exists
    user = svc_get_user_or_none(email, "request_password_reset")

    # Delay response in case user does not exist
    # Reason: mitigating timing attacks by introducing randomized delay
    if user is None:
        log_request_reset_password(404, f"Email: {email}.", user_agent, client_ip, 0)
        delay = random.uniform(0.3, 1.5)
        time.sleep(delay)
        return jsonify(success_response) # not sending error to create ambiguity
    
    # Check if user is blocked from logging in
    block_status = svc_check_if_user_blocked(user)
    if block_status["blocked"]:
        log_request_reset_password(403, block_status["log_message"], user_agent, client_ip, user.id)
        if block_status["temporary_block"]:
            return jsonify(error_429),429
        return jsonify(error_403),403
    
    # Check if user is blocked from changing credentials
    if svc_check_auth_change_block_status(user):
        log_request_reset_password(403, f"Blocked from changing credentials. Previous failed attempts: {user.auth_change_attempts}.", user_agent, client_ip, user.id)
        if user.auth_change_attempts == 5 or user.auth_change_attempts == 10:
            send_cred_change_block_email(user.name, user.email, user.auth_change_attempts)
        return jsonify(error_429),429
    
    # In case of MFA, check if a recovery email exists:
    if user.mfa_enabled and not user.recovery_email:
        logging.critical(f"MFA enabled but no recovery email. user_id={user.id}")
        log_request_reset_password(501, "MFA is enabled, but no recovery email is available.", user_agent, client_ip, user.id)
        return jsonify(error_response), 500

    # Generate and send security codes
    codes = svc_generate_security_code(user, user.mfa_enabled)

    if not codes or not codes[0]:
        log_request_reset_password(500, "Failed to generate security codes.", user_agent, client_ip, user.id)
        return jsonify(error_response), 500
    
    if user.mfa_enabled and len(codes) != 2:
        log_request_reset_password(500, "Failed to generate 2nd security code (user has MFA enabled).", user_agent, client_ip, user.id)
        return jsonify(error_response), 500
    
    # Sending emails
    email_1_sent = send_pw_reset_request_email(user.name, user.email, codes[0])
    email_2_sent = False

    if user.mfa_enabled:
        time.sleep(2) # wait for 1st email to be properly sent (later: implement Celery)
        email_2_sent = send_pw_reset_request_email(user.name, user.recovery_email, codes[1])

    if not email_1_sent or (not email_2_sent and user.mfa_enabled):
        svc_reset_security_codes(user)
        msg = f"Failed to send security code email(s). Security codes were reset."
        logging.error(msg)
        log_request_reset_password(500, msg, user_agent,client_ip, user.id)
        return jsonify(error_response), 500 
    
    log_request_reset_password(200, "Successfully sent security codes.", user_agent,client_ip, user.id)

    return jsonify(success_response)


####################################
#       RESET USER'S PASSWORD      #
####################################

@credential_change.route("/reset_password", methods=["POST"]) 
@validate_schema(reset_password_schema) 
@limiter.limit("1/minute; 5/day")
def reset_password(): 
    """
    reset_password() -> JsonType
    ----------------------------------------------------------

    Route resets user password by validating a security code.
    If user has MFA enabled, route will ask for a second security code (sent to recovery email).
    
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
    new_password = json_data["new_password"]
    security_code_1 = json_data["security_code_1"]
    security_code_2 = json_data.get("security_code_2", "")
    user_agent = json_data.get("user_agent", "") 
    honeypot = json_data["honeypot"] #TODO: rename honeypot field

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Standard response
    success_response = {"response": "Password reset successful."}
    error_400 = {"response": "Check password input or add security code received in recovery email."}
    error_401 = {"response": "Authentication failed."}
    error_403 = {"response": "Unauthorized: please contact site admin for more information."}
    error_429 = {"response": "Too many failed attempts. Please try again later."}
    error_500 = {"response": "There was an error resetting the user's password."}

    # Filter out bots
    if len(honeypot) > 0:
        svc_bot_caught(request, "reset_password")
        log_reset_password(418, f"Honeypot trigger. Email: {email}", user_agent, client_ip, 0)
        return jsonify(error_400), 400 #TODO: revisit design choice
    
    # Check if user exists
    user = svc_get_user_or_none(email, "password_reset")

    # Delay response in case user does not exist
    # Reason: mitigating timing attacks by introducing randomized delay
    if user is None:
        log_reset_password(404, f"Email: {email}.", user_agent, client_ip, 0)
        delay = random.uniform(0.3, 1.5)
        time.sleep(delay)
        return jsonify(error_401), 401
    
    # Check if user is blocked from logging in
    block_status = svc_check_if_user_blocked(user)
    if block_status["blocked"]:
        log_reset_password(403, block_status["log_message"], user_agent, client_ip, user.id)
        if block_status["temporary_block"]:
            return jsonify(error_429),429
        return jsonify(error_403),403
    
    # Check if user is blocked from changing credentials
    if svc_check_auth_change_block_status(user):
        log_reset_password(403, f"Blocked from changing credentials. Previous failed attempts: {user.auth_change_attempts}.", user_agent, client_ip, user.id)
        if user.auth_change_attempts == 5 or user.auth_change_attempts == 10:
            send_cred_change_block_email(user.name, user.email, user.auth_change_attempts)
        return jsonify(error_429),429
    
    # If user has MFA enabled, check that there are 2 codes
    if user.mfa_enabled and not security_code_2:
        return jsonify(error_400), 400
    
    # Check security codes

    codes_are_valid = svc_validate_security_codes(user, security_code_1, security_code_2)

    if not codes_are_valid:
        svc_record_failed_auth_change_attempt(user)
        log_reset_password(401, f"MFA status: {user.mfa_enabled}.", user_agent, client_ip, user.id)
        return jsonify(error_401), 401

    # Check new password
    pw_change = svc_change_user_password(user, new_password)

    log_reset_password(pw_change["log_code"], pw_change["log_text"], user_agent, client_ip, user.id)

    if pw_change["log_code"] == 500:
        return jsonify(error_500), 500
    if pw_change["log_code"] == 400: #=> password check failed, probably means FE check bypassed
        svc_record_failed_auth_change_attempt(user)
        return jsonify(error_400), 400
    
    # Invalidate other sessions and log user out (if user was logged in)
    svc_reset_user_session(user)
    if current_user and current_user.is_authenticated:
        flask_logout_user()

    # Send email confirming password changed 
    send_pw_change_success_email(user.name, user.email)

    
    return jsonify(success_response)

####################################
#     REQUEST CHANGE EMAIL         #
####################################
@credential_change.route("/request_change_email", methods=["POST"]) 
@login_required
@validate_schema(request_change_email_schema) 
@limiter.limit("5/day")
def request_change_email():
    """
    request_change_email() -> JsonType
    ----------------------------------------------------------

    Validates user password and sends security code to new email address.
    If user has email verified, will also send a security code to old email address.

    A 200 response means user should continue flow in change_email route.
    
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
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    new_email = json_data["new_email"]
    password = json_data["password"]
    user_agent = json_data.get("user_agent", "") 

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Standard response
    success_response = {"response": "Successfully sent security code(s)."}
    error_400 = {"response": "Wrong password."}
    error_403 = {"response": "Unauthorized: temporarily blocked from changing credentials due to too many failed attempts."}
    error_440 = {"response": "Session expired. Please log in again."}
    error_500 = {"response": "An error occurred, please try again."}

    # Get user
    user = svc_get_user_or_none(current_user.email, "change_email")
    if user is None:
        log_request_change_email(500, "Session did not return current user.", user_agent, client_ip, 0)
        return jsonify(error_440), 440
    
    # Check if the user is blocked from changing credentials (too many failed attempts)
    if svc_check_auth_change_block_status(user):
        log_request_change_email(403, f"Blocked from changing credentials. Previous failed attempts: {user.auth_change_attempts}.", user_agent, client_ip, user.id)
        if user.auth_change_attempts == 5 or user.auth_change_attempts == 10:
            # Send email informing about the block
            send_cred_change_block_email(user.name, user.email, user.auth_change_attempts)
        return jsonify(error_403), 403
    
    # Check password
    pw_ok = svc_is_pw_or_otp_valid(user, password, "password")

    if not pw_ok:
        svc_record_failed_auth_change_attempt(user)
        log_request_change_email(400, f"Wrong password input.", user_agent, client_ip, user.id)
        return jsonify(error_400), 400
    
    # Check new email and save it to db
    email_ok = svc_save_new_email(user, new_email)

    if not email_ok["success"]:
        log_request_change_email(email_ok["log_code"], email_ok["log_text"], user_agent, client_ip, user.id)
        return jsonify({"response": email_ok["res_msg"]}), email_ok["res_code"]

    # Generate and send security codes
    codes = svc_generate_security_code(user, user.email_is_verified)

    if not codes or not codes[0]:
        log_request_change_email(500, "Failed to generate security codes.", user_agent, client_ip, user.id)
        return jsonify(error_500), 500
    
    if user.email_is_verified and len(codes) != 2:
        log_request_change_email(500, "Failed to generate 2nd security code (user email is verified).", user_agent, client_ip, user.id)
        return jsonify(error_500), 500
    
    # Sending emails
    email_1_sent = send_email_reset_request_email(user.name, new_email, codes[0])
    email_2_sent = False

    if user.email_is_verified:
        time.sleep(2) # wait for 1st email to be properly sent (later: implement Celery)
        email_2_sent = send_email_reset_request_email(user.name, user.email, codes[1])

    if not email_1_sent or (not email_2_sent and user.email_is_verified):
        svc_reset_security_codes(user)
        svc_reset_new_email(user)
        msg = f"Failed to send security code email(s). Security codes were reset."
        logging.error(msg)
        log_request_change_email(500, msg, user_agent,client_ip, user.id)
        return jsonify(error_500), 500 
    
    log_request_change_email(200, "Successfully sent security codes.", user_agent,client_ip, user.id)

    return jsonify(success_response)

####################################
#          CHANGE EMAIL            #
####################################

@credential_change.route("/change_email", methods=["POST"])  
@login_required
@validate_schema(change_email_schema) 
@limiter.limit("5/day")
def change_email():
    """
    change_email() -> JsonType
    ----------------------------------------------------------

    This is the second step of a 2-step email change process.
    Will validate the security code sent to new email address.
    If the user had a validated email address, will also validate a second security code.

    If email is successfully changed, a confirmation email will be sent to the old and new email addresses. In case the user has MFA enabled, a confirmation will also be sent to the recovery email.
    
    Note:

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
        "response": "An error occurred, please try again."
    ``` 

    A successful response may yield:

    ```python
        "response": "Email changed successfully!."
    ``` 

    ``` 
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    security_code_1 = json_data["security_code_1"]
    security_code_2 = json_data.get("security_code_2", "")
    user_agent = json_data.get("user_agent", "") 

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Standard response
    success_response = {"response": "Email changed successfully."}
    error_400 = {"response": "Security code is missing, wrong, or expired."}
    error_403 = {"response": "Unauthorized: temporarily blocked from changing credentials due to too many failed attempts."}
    error_440 = {"response": "Session expired. Please log in again."}
    error_500 = {"response": "An error occurred, please try again."}

    # Get user
    user = svc_get_user_or_none(current_user.email, "change_email")
    if user is None:
        log_change_email(500, "Session did not return current user.", user_agent, client_ip, 0)
        return jsonify(error_440), 440
    
    # Check if the user is blocked from changing credentials (too many failed attempts)
    if svc_check_auth_change_block_status(user):
        log_change_email(403, f"Blocked from changing credentials. Previous failed attempts: {user.auth_change_attempts}.", user_agent, client_ip, user.id)
        if user.auth_change_attempts == 5 or user.auth_change_attempts == 10:
            # Send email informing about the block
            send_cred_change_block_email(user.name, user.email, user.auth_change_attempts)
        return jsonify(error_403), 403
    
    # Check security code(s)
    codes_ok = False

    # Case the user has email verified or is MFA
    if user.email_is_verified:
        if not security_code_1 or not security_code_2:
            log_change_email(400, "Security code missing.", user_agent, client_ip, user.id)
            return jsonify(error_400), 400
        codes_ok = svc_validate_security_codes(user, security_code_1, security_code_2)
    else:
        codes_ok = svc_validate_security_codes(user, security_code_1)
    
    if not codes_ok:
        svc_record_failed_auth_change_attempt(user)
        log_change_email(400, "Security code wrong or expired.", user_agent, client_ip, user.id)
        return jsonify(error_400), 400
    
    # Save user current settings
    old_email = user.email
    new_email = user.new_email
    
    # Change email
    email_change_ok = svc_change_email(user)

    if not email_change_ok:
        log_change_email(500, "Could not change email due to DB error.", user_agent, client_ip, user.id)
        return jsonify(error_500), 500
    
    # Confirm email change to the new email
    send_email_change_success_email(user.name, new_email, old_email, new_email)

    # Confirm email change to the old email
    send_email_change_success_email(user.name, old_email, old_email, new_email)

    # If user has MFA, send confirmation to recovery email address
    if user.mfa_enabled:
        send_email_change_success_email(user.name, user.recovery_email, old_email, new_email)

    # Invalidate other sessions and login the user again
    svc_reset_user_session(user)
    flask_logout_user()
    flask_login_user(user) 

    # Log success
    log_change_email(200, f"Old email: {old_email}, new email: {new_email}", user_agent, client_ip, user.id)

    # Return success
    return jsonify(success_response), 200

####################################
#  VALIDATE TOKEN FOR EMAIL CHANGE #
####################################

# @credential_change.route('/email_change_token_validation', methods=['POST']) # TODO: proper logging
# @limiter.limit("5/day")
# @validate_schema(change_email_token_validation_schema)
# def email_change_token_validation():
#     """
#     email_change_token_validation() -> JsonType 

#     ----------------------------------------------------------
#     Validates a token to change the user's email or password.
#     This route is used as the second step of the email change process
#     when a user has a validated account.

#     Two tokens should be validated for an email change to be successfull:
#     - the token sent to the current email address
#     - the token sent to the new email address

#     When only one token is validated, route will return a 202.
#     When both tokens have been validated, route will return a 200 response.
    
#     Returns Json object containing the response:
#     - "response" value is always included, containing the message detailing the result.

#     ----------------------------------------------------------
#     **Response example:**

#     An error may yield:
#     ```python
#         "response": "Invalid or expired token."
#     ``` 

#     A successful response may yield:

#     ```python
#         "response": "Email changed successfully!"
#     ``` 

#     or a 202

#     ```python
#         "response": "Token validated. One token validation missing."
#     ```  
#     """
#     # Get the JSON data from the request body
#     json_data = request.get_json()
#     signed_token = json_data["signed_token"]
#     purpose = json_data["purpose"]
#     user_agent = json_data.get("user_agent", "") 

#     # Get the request ip
#     client_ip = get_client_ip(request) or ""

#     # Standard error response
#     error_response = { "response": "Invalid or expired token." }
    
#     token_purpose = TokenPurpose(purpose) 
    
#     # validate token
#     res = validate_and_verify_signed_token(signed_token, token_purpose, "email_change_token_validation", True) 

#     if res["status"] != 200:
#         log_email_token_validation(500, f"{res["message"]}", user_agent, client_ip, 0)
#         return jsonify({"response": res["message"]}), res["status"]
    
#     # Token validated, now take appropriate action

#     # Get user from token
#     token = res["token"]
#     user = token.user
        
#     # Two tokens are issued for an email change: one to verify the old and another to verify the new email   
#     related_tokens = Token.query.filter_by(group_id=token.group_id).all()

#     if len(related_tokens) != 2:
#         log_message = f"Invalid number of related tokens for group_id: {token.group_id}. 2 are required for email changes"
#         logging.error(log_message)
#         log_email_token_validation(500, log_message, user_agent, client_ip, user.id)
#         return jsonify(error_response), 500
        
#     # Check to see if the other token has already been validated
#     second_token = next((t for t in related_tokens if t != token), None)
#     if not second_token:
#         log_message = f"Second token not found for group_id: {token.group_id}."
#         logging.error(log_message)
#         log_email_token_validation(500, log_message, user_agent, client_ip, user.id)
#         return jsonify(error_response), 500
    
#     if second_token.token_verified == modelBool.TRUE:
#         # User has validated both required tokens and may now change emails
#         try: 
#             new_email = user.new_email
#             old_email = user.email
#             email_was_changed = user.change_email() 
#             if email_was_changed:
#                 # Delete tokens after email change
#                 db.session.delete(token)
#                 db.session.delete(second_token)
#                 db.session.commit()
#                 # Send emails confirming email change
#                 try:
#                     send_email_change_success_emails(user.name, old_email, new_email)
#                 except Exception as e:
#                     logging.warning(f"Failed to send email change success notification. Error: {e}") 
#             else:
#                 log_message = f"Failed to change email possibly because no new email was found in the database."
#                 logging.error(log_message)
#                 log_email_token_validation(500, log_message, user_agent, client_ip, user.id)
#                 return jsonify(error_response), 500
#         except Exception as e:
#             db.session.rollback()
#             log_message = f"Failed to change email. Error: {str(e)}"
#             logging.error(log_message)
#             log_email_token_validation(500, log_message, user_agent, client_ip, user.id)
#             return jsonify(error_response), 500
#     else:
#         log_email_token_validation(202, "", user_agent, client_ip, user.id)
#         return jsonify({"response": "Token validated. One token validation missing."}), 202
    
#     # Reset user sessions and if user is logged in, log out
#     reset_user_session(user)
#     if not current_user.is_anonymous:
#         flask_logout_user()

#     # Log
#     log_email_token_validation(200, f"Previous email: {old_email}. New email: {new_email}", user_agent, client_ip, user.id)

#     response_data ={ "response":"Email was changed successfully!" }
#     return jsonify(response_data), 200
