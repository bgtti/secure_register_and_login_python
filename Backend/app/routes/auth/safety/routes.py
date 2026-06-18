"""
**ABOUT THIS FILE**

auth/safety/routes.py contains routes responsible for the user account's safety and verification.
Here you will find the following routes:
- **verify_acct_email** route is the second step in the email verification process
- **set_mfa** route enables or disables multi factor authentication

The format of data sent by the client is validated using Json Schema. 
Reoutes receiving client data are decorated with `@validate_schema(name_of_schema)` for this purpose. 

------------------------
## More information

Setting MFA does not require the user to have a recovery email address. If the user looses access to their email or password that user will be locked out. The user is informed of this per email. Consider making MFA status dependent on having a recovery method. Alternatively, instruct support on how to verify the user and allow access to the account.

"""
############# IMPORTS ##############

# Python/Flask libraries
import logging
from flask import request, jsonify
from flask_login import (
    current_user,
    login_required,
)

# Extensions
from app.extensions.extensions import db, limiter, flask_bcrypt, limiter

# Database models
from app.models.user import User

# Utilities
from app.common.custom_decorators.json_schema_validator import validate_schema
from app.common.ip_utils.ip_address_validation import get_client_ip
from app.common.salt_and_pepper.helpers import get_pepper

# Services
from app.services.auth.user_otp_and_pw_service import svc_generate_otp, svc_is_pw_or_otp_valid
from app.services.user.user_service import svc_get_user_or_none
from app.services.auth.user_acct_verification_service import svc_verify_user_acct_email
from app.services.auth.user_mfa_service import svc_set_MFA

# Email services
from app.emails.auth.acct_verification_email import send_acct_verification_success_email
from app.emails.auth.mfa_status_email import send_email_mfa_set

# Log helpers
from app.routes.auth.safety.log import (
    log_verify_account,
    log_set_mfa
)

# JSON Schemas
from app.routes.auth.safety.schemas import (
    verify_account_schema,
    set_mfa_schema
)

# Blueprint
from . import safety


############# ROUTES ###############


####################################
#            VERIFY ACCT           #
####################################

@safety.route("/verify_account", methods=["POST"]) 
@login_required
@validate_schema(verify_account_schema)
@limiter.limit("5/day")
def verify_account(): 
    """
    **verify_account() -> JsonType**

    ----------------------------------------------------------
    Route receives the request to verify the user's email address
    and sends email with confirmation of verification if successful. 
    Note: FE should have sent request to OTP route before calling this function.
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "mail_sent" boolean value indicates whether the user received a success email.
    - "acct_verified" boolean value indicates whether the user's account email has been verified'.

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "mail_sent": True, 
                "acct_verified": True,
            }
    ``` 
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    otp = json_data["otp"]
    user_agent = json_data.get("user_agent", "") 

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Standard response
    response_data = {
        "response": "",
        "mail_sent": False,
        "acct_verified": False,
        }
    
    # Get user
    user = svc_get_user_or_none(current_user.email, "verify_account")
    if user is None:
        response_data["response"] = "Session expired. Please log in again."
        log_verify_account(404, "Session did not return current user.", user_agent, client_ip, 0)
        return jsonify(response_data), 440
    
    # Check if account is already verified
    if user.email_is_verified:
        response_data["response"] = "success"
        response_data["acct_verified"] = True
        log_verify_account(200, "Account email already verified.", user_agent, client_ip, user.id)
    
    # Check OTP
    password_is_valid = svc_is_pw_or_otp_valid(user, otp, "otp")
    if not password_is_valid:
        response_data["response"] = "Invalid or expired OTP."
        log_verify_account(401, "Invalid or expired OTP.", user_agent, client_ip, user.id)
        return jsonify(response_data), 401
    
    # Verify account
    verification_ok = svc_verify_user_acct_email(user)
    if not verification_ok:
        response_data["response"] = "System error: please try again later."
        log_verify_account(500, "Could not verify account due to DB error.", user_agent, client_ip, user.id)
        return jsonify(response_data), 500
    
    # Prepare success response
    response_data["response"] = "success"
    response_data["acct_verified"] = True
    
    # Confirm verification per email
    email_sent = send_acct_verification_success_email(user.name, user.email)

    if email_sent:
        response_data["mail_sent"] = True
        log_verify_account(200, "", user_agent, client_ip, user.id)
    else:
        log_verify_account(206, "Account verified but confirmation email failed.", user_agent, client_ip, user.id)


    return jsonify(response_data)

####################################
#             SET MFA              #
####################################

@safety.route("/set_mfa", methods=["POST"]) 
@login_required
@validate_schema(set_mfa_schema)
@limiter.limit("5/day")
def set_mfa(): 
    """
    **set_mfa() -> JsonType**

    ----------------------------------------------------------
    Route receives the request to enable or disable mfa
    and sends email with confirmation of action. 
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "mfa_enabled" boolean value indicates whether mfa is enabled.

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"MFA was successfully set!",
                "mfa_enabled": False
            }
    ``` 
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    enable_mfa = json_data["enable_mfa"]
    password = json_data["password"]
    user_agent = json_data.get("user_agent", "") 

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Prepare response
    response_data ={
            "response":"",
            "mfa_enabled": False,
        }

    # Get user
    user = svc_get_user_or_none(current_user.email, "set_mfa")
    if user is None:
        response_data["response"] = "Session expired. Please log in again."
        log_set_mfa(404, "Session did not return current user.", user_agent, client_ip, 0)
        return jsonify(response_data), 440
    
    # Check if MFA is already set
    if user.mfa_enabled == enable_mfa:
        response_data["response"] = "MFA was successfully enabled!" if enable_mfa else "MFA was successfully disabled!"
        response_data["mfa_enabled"] = user.mfa_enabled
        log_txt = "MFA was already enabled." if enable_mfa else "MFA was already disabled."
        log_code = 201 if enable_mfa else 200
        log_set_mfa(log_code, log_txt, user_agent, client_ip, user.id)
        return jsonify(response_data), 200
    
    # Check Password
    password_is_valid = svc_is_pw_or_otp_valid(user, password, "password")
    if not password_is_valid:
        response_data["response"] = "Invalid password."
        log_set_mfa(401, "Invalid password.", user_agent, client_ip, user.id)
        return jsonify(response_data), 401
    
    # Only verified accounts can enable MFA
    if enable_mfa and not user.email_is_verified:
        response_data["response"] = "Please verify your account email before enabling MFA."
        log_set_mfa(403, "Account email not verified.", user_agent, client_ip, user.id)
        return jsonify(response_data), 403
    
    # Must have recovery email address
    if enable_mfa and not user.recovery_email:
        response_data["response"] = "Please add a recovery email before enabling MFA."
        log_set_mfa(403, "No recovery email address.", user_agent, client_ip, user.id)
        return jsonify(response_data), 403
    
    # Set MFA status
    mfa_status_ok = svc_set_MFA(user, enable_mfa)

    if not mfa_status_ok:
        response_data["response"] = "System error: please try again later."
        log_set_mfa(500, "DB error prevented change of MFA status.", user_agent, client_ip, user.id)
        return jsonify(response_data), 500
    
    # Prepare success response
    response_data["response"] = "MFA was successfully enabled!" if enable_mfa else "MFA was successfully disabled!"
    response_data["mfa_enabled"] = user.mfa_enabled
    
    # Send confirmation email
    email_sent = send_email_mfa_set(user.name, user.email, enable_mfa)

    # Log success
    if enable_mfa:
        log_code = 201 if email_sent else 206
        log_text = "MFA enabled." if email_sent else "MFA enabled. Email informing of MFA status change failed."
    else:
        log_code = 200 if email_sent else 207
        log_text = "MFA disabled." if email_sent else "MFA disabled. Email informing of MFA status change failed."

    log_set_mfa(log_code, log_text, user_agent, client_ip, user.id)
    
    return jsonify(response_data)

