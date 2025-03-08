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
from app.utils.salt_and_pepper.helpers import get_pepper
from app.utils.custom_decorators.json_schema_validator import validate_schema

# Auth helpers (this file)
from app.routes.auth.safety.email import (
    send_acct_verification_sucess_email,
    send_email_mfa_set
)

from app.routes.auth.safety.schemas import (
    verify_account_schema,
    set_mfa_schema
)

# Blueprint
# safety = Blueprint('safety', __name__)
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

    #TODO: get user_agent and log it

    # Standard error response
    error_response = {
        "response": "Invalid or expired token.",
        "mail_sent": False,
        "acct_verified": False,
        }
    
    user = current_user
    
    try:
        # Check OTP
        if user.check_otp(otp) is False:
            logging.info(f"Invalid or expired token could not be validated. Account validation failed for {user.email}.")
            return jsonify(error_response), 400
        
        # Verify account
        is_verified = user.verify_account()
        db.session.commit()
        if is_verified:
            email_sent = send_acct_verification_sucess_email(user.name, user.email)
        else:
            email_sent = False

    except Exception as e:
        db.session.rollback()
        logging.error(f"Database error. Error: {e}")
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
    user_agent = json_data.get("user_agent", "") #TODO log this in event

    # Get the user from cookie 
    try:
        user = User.query.filter_by(email=current_user.email).first()
    except Exception as e:
        logging.error(f"Failed to get user. Error: {e}")
        return jsonify({"response": "A database error prevented user retrieval."}), 500
    
    #TODO: consider not allowing superadmin to disable mfa
    
    # Check password 
    salted_password = user.salt + password + get_pepper(user.created_at)
    if not flask_bcrypt.check_password_hash(user.password, salted_password):
        return jsonify({"response": "Password incorrect."} ), 401
    
    # Check OTP
    if enable_mfa is False:
        if user.check_otp(otp) is False:
            return jsonify({"response": "Provided OTP is wrong or expired."} ), 401
        
    try:
        user.set_mfa(enable_mfa)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"Failed to set MFA. Error: {e}")

        return jsonify({"response": "A database error prevented MFA to be set."}), 500
    
    try:
        send_email_mfa_set(user.name, user.email, enable_mfa)
    except Exception as e:
            logging.error(f"Error encountered while trying to send confirmation of setting mfa. Error: {e}")

        
    response_data ={
            "response":"MFA was successfully disabled!",
            "mfa_enabled": user.mfa_enabled.value,
        }
    return jsonify(response_data)

