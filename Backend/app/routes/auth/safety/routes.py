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
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.salt_and_pepper.helpers import get_pepper

# Safety helpers 
from app.routes.auth.safety.email import (
    send_acct_verification_sucess_email,
    send_email_mfa_set
)

from app.routes.auth.safety.log import (
    log_verify_account,
    log_set_mfa
)

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
def verify_account(): # TODO --> Add to logs so user actions can show in history, consider db rollbacks
    """
    **verify_account() -> JsonType**

    ----------------------------------------------------------
    Route receives the request to verify the user's email address
    and sends email with confirmation of verification if successfull. 
    
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

    # Standard error response
    error_response = {
        "response": "Invalid or expired token.",
        "mail_sent": False,
        "acct_verified": False,
        }

    # Get the user from cookie
    try:
        user = User.query.filter_by(email=current_user.email).first()
    except Exception as e:
        log_message = f"Database query failed: {str(e)}"
        logging.error(log_message)
        log_verify_account(500, log_message, user_agent, client_ip, 0)
        return jsonify({"response": "An error occurred while fetching the user."}), 500
    
    try:
        # Check OTP
        if user.check_otp(otp) is False:
            log_message = f"Invalid or expired token could not be validated. Account validation failed for {user.email}."
            logging.info(log_message)
            log_verify_account(401, log_message, user_agent, client_ip, user.id)
            return jsonify(error_response), 400
        
        # Verify account
        is_verified = user.verify_account()
        db.session.commit()
        if is_verified:
            email_sent = send_acct_verification_sucess_email(user.name, user.email)
            log_verify_account(200, "", user_agent, client_ip, user.id)
        else:
            email_sent = False

    except Exception as e:
        db.session.rollback()
        log_message = f"Database error. Error: {str(e)}"
        logging.error(log_message)
        log_verify_account(500, log_message, user_agent, client_ip, user.id)
        return jsonify(error_response), 500

        
    response_data ={
            "response":"success",
            "mail_sent": email_sent,
            "acct_verified": is_verified,
        }
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
    otp = json_data.get("otp", "")
    user_agent = json_data.get("user_agent", "") 

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Get the user from cookie 
    try:
        user = User.query.filter_by(email=current_user.email).first()
    except Exception as e:
        log_message = f"Failed to get user. Error: {str(e)}"
        logging.error(log_message)
        log_set_mfa(500, log_message, user_agent, client_ip, 0)
        return jsonify({"response": "A database error prevented user retrieval."}), 500
    
    #TODO: consider not allowing superadmin to disable mfa
    
    # Check password 
    salted_password = user.salt + password + get_pepper(user.created_at)
    if not flask_bcrypt.check_password_hash(user.password, salted_password):
        log_set_mfa(401, "Password incorrect.", user_agent, client_ip, user.id)
        return jsonify({"response": "Password incorrect."} ), 401
    
    # Check OTP
    if enable_mfa is False:
        if user.check_otp(otp) is False:
            log_set_mfa(401, "Provided OTP is wrong or expired.", user_agent, client_ip, user.id)
            return jsonify({"response": "Provided OTP is wrong or expired."} ), 401
        
    try:
        user.set_mfa(enable_mfa)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        log_message = f"Failed to set MFA. Error: {str(e)}"
        logging.error(f"Failed to set MFA. Error: {e}")
        log_set_mfa(500, log_message, user_agent, client_ip, user.id)
        return jsonify({"response": "A database error prevented MFA to be set."}), 500
    
    try:
        send_email_mfa_set(user.name, user.email, enable_mfa)
    except Exception as e:
        log_message = f"Error encountered while trying to send confirmation of setting mfa. Error: {str(e)}"
        logging.error(f"Error encountered while trying to send confirmation of setting mfa. Error: {e}")
        log_set_mfa(500, log_message, user_agent, client_ip, user.id)

    success_message = "MFA was successfully enabled!" if enable_mfa else "MFA was successfully disabled!"

    log_set_mfa(200, success_message, user_agent, client_ip, user.id)

    response_data ={
            "response":success_message,
            "mfa_enabled": user.mfa_enabled.value,
        }
    return jsonify(response_data)

