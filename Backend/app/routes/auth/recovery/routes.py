"""
**ABOUT THIS FILE**

auth/recovery/routes.py contains routes responsible for a user's account recovery.

Here you will find the following routes:
- **set_recovery_email** sets second email in case user looses access to his/her registered email. Also used to change a recovery email.
- **get_recovery_status** sends information about whether the user has a recovery email set (and if so, the anonimyzed version of it).
- **get_recovery_email** sends the full recovery email when requested.
- **delete_recovery_email** deletes the recovery email stored.

A recovery email is especially important for users who have MFA set in their accounts. The reason is that if those users forget their passwords, the recovery email is the only way to reset their passwords. The front end suggests to the user to contact support otherwise.

TODO: make sure to implement the logic for when a user with MFA to regain access to their account using the recovery email when they lose access to their email address (ie: have no access to their OTP).

The format of data sent by the client is validated using Json Schema. 
Reoutes receiving client data are decorated with `@validate_schema(name_of_schema)` for this purpose. 

------------------------
## More information

NOTE: whomever uses this template should make sure to establish guidelines for the support team on how to proceed in case the user has MFA set up but no recovery email - and the user then looses access to their account.

------------------------
## Route testing

Status:
- **set_recovery_email** last test ran on XX December 2024 TODO: testing

"""
############# IMPORTS ##############

# Python/Flask libraries
import logging
from flask import Blueprint, request, jsonify

# Extensions and third-party libs
from flask_login import (
    current_user,
    login_required,
)
from app.extensions.extensions import db, flask_bcrypt, limiter

# Database models
from app.models.user import User

# Utilities
from app.common.custom_decorators.json_schema_validator import validate_schema
from app.common.ip_utils.ip_address_validation import get_client_ip
from app.common.anonymization.anonymize import anonymize_email

# Services
from app.services.auth.user_acct_recovery_service import (
    svc_reset_new_recovery_email,
    svc_save_new_recovery_email,
    svc_set_recovery_email,
    svc_delete_recovery_email
)
from app.services.auth.user_otp_and_pw_service import svc_is_pw_or_otp_valid
from app.services.auth.user_security_code_service import (
    svc_generate_security_code, 
    svc_reset_security_codes,
    svc_validate_security_codes
    )
from app.services.user.user_service import svc_get_user_or_none


# Email Services
from app.emails.auth.recovery_email import (
    send_recovery_email_req_set_email,
    send_recovery_email_changed_email,
    send_recovery_email_set_email,
    send_email_recovery_deletion
    )

# Log helpers
from app.routes.auth.recovery.log import (
    log_req_set_recovery_email,
    log_set_recovery_email,
    log_get_recovery_email,
    log_delete_recovery_email
)
# JSON Schema
from app.routes.auth.recovery.schemas import (
    req_set_recovery_email_schema,
    set_recovery_email_schema, 
    get_recovery_email_schema, 
    delete_recovery_email_schema)

# Blueprint
from . import recovery


############# ROUTES ###############

####################################
#    REQUEST SET RECOVERY EMAIL    #
####################################

@recovery.route("/request_set_recovery_email", methods=["POST"])
@login_required
@limiter.limit("5/minute;10/day")
@validate_schema(req_set_recovery_email_schema) 
def request_set_recovery_email(): 
    """
    request_set_recovery_email() -> JsonType
    ----------------------------------------------------------

    Step 1/2 to set user's recovery email address. Sends a security code to to a given recovery email as the first step to set a recovery email.
    
    Returns Json object containing strings:
    - "response" value is always included. 

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "recovery_email": "john@doe.com"
            }
    ``` 
    """
    # Get the JSON data from the request body 
    json_data = request.get_json()
    recovery_email = json_data["recovery_email"]
    password = json_data["password"]
    user_agent = json_data.get("user_agent", "") 

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Standard response
    success_response = {"response": "Successfully sent security code to recovery email."}
    error_401 = {"response": "Wrong password."}
    error_440 = {"response": "Session expired. Please log in again."}
    error_500 = {"response": "An error occurred, please try again."}

    # Get user
    user = svc_get_user_or_none(current_user.email, "change_email")
    if user is None:
        log_req_set_recovery_email(500, "Session did not return current user.", user_agent, client_ip, 0)
        return jsonify(error_440), 440
    
    # Check password
    pw_ok = svc_is_pw_or_otp_valid(user, password, "password")

    if not pw_ok:
        log_req_set_recovery_email(401, f"Wrong password input.", user_agent, client_ip, user.id)
        return jsonify(error_401), 401
    
    # Check recovery email and save it to db
    recovery_status = svc_save_new_recovery_email(user, recovery_email)

    log_req_set_recovery_email(recovery_status["log_code"], recovery_status["log_text"], user_agent, client_ip, user.id)

    if not recovery_status["success"]:
        jsonify({"response": recovery_status["res_msg"]}), recovery_status["res_code"]

    # Send security code to new recovery email
    code = svc_generate_security_code(user, False)

    if not code or not code[0]:
        log_req_set_recovery_email(500, "Failed to generate security codes.", user_agent, client_ip, user.id)
        return jsonify(error_500), 500
    
    email_sent = send_recovery_email_req_set_email(user.name, recovery_email, code[0])

    if not email_sent:
        svc_reset_security_codes(user)
        svc_reset_new_recovery_email(user)
        msg = f"Failed to send security code email. Security codes were reset."
        logging.error(msg)
        log_req_set_recovery_email(500, msg, user_agent,client_ip, user.id)
        return jsonify(error_500), 500
    
    log_req_set_recovery_email(200, "Successfully sent security code to recovery email.", user_agent,client_ip, user.id)

    return jsonify(success_response)

####################################
#         SET RECOVERY EMAIL       #
####################################

@recovery.route("/set_recovery_email", methods=["POST"])
@login_required
@limiter.limit("5/minute;10/day")
@validate_schema(set_recovery_email_schema) 
def set_recovery_email(): 
    """
    set_recovery_email() -> JsonType
    ----------------------------------------------------------

    Step 2/2 of setting a recovery email.
    Receives a security code to validate, sets new recovery email, and confirms change to the user's email address(es).
    
    Returns Json object containing strings:
    - "response" value is always included. 

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "recovery_email": "john@doe.com"
            }
    ``` 
    """
    # Get the JSON data from the request body 
    json_data = request.get_json()
    security_code = json_data["security_code"]
    user_agent = json_data.get("user_agent", "") 

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Standard response
    error_400 = {"response": "Security code is missing, wrong, or expired."}
    error_422 = {"response": "New recovery email missing. Please Re-start the process."}
    error_440 = {"response": "Session expired. Please log in again."}
    error_500 = {"response": "An error occurred, please try again."}

    # Get user
    user = svc_get_user_or_none(current_user.email, "set_recovery_email")
    if user is None:
        log_set_recovery_email(500, "Session did not return current user.", user_agent, client_ip, 0)
        return jsonify(error_440), 440
    
    # Check whether a new recovery email exsts
    if not user.new_recovery_email:
        log_set_recovery_email(422, "No pending recovery email found.", user_agent, client_ip, user.id)
        return jsonify(error_422), 422

    # Check security code
    code_ok = svc_validate_security_codes(user, security_code)

    if not code_ok:
        log_set_recovery_email(400, "Security code wrong or expired.", user_agent, client_ip, user.id)
        return jsonify(error_400), 400
    
    # Save user's current settings
    old_recovery_email = user.recovery_email
    new_recovery_email = user.new_recovery_email

    recovery_change_ok = svc_set_recovery_email(user)

    if not recovery_change_ok:
        log_set_recovery_email(500, "Could not set recovery email due to DB error.", user_agent, client_ip, user.id)
        return jsonify(error_500), 500
    
    #NOTE: failure in sending emails are ignored at this time

    # Confirm per email to the newly set recovery email
    send_recovery_email_set_email(user.name, new_recovery_email, new_recovery_email)

    # Anonymize recovery email
    anonymized_recovery_email = anonymize_email(new_recovery_email)
    anonymized_old_recovery_email = anonymize_email(old_recovery_email)

    # Confirm change or setting of new recovery email to user
    if old_recovery_email:
        # Confirm change to user's email
        send_recovery_email_changed_email(user.name, user.email, new_recovery_email)
        # Confirm change to user's old recovery email
        send_recovery_email_changed_email(user.name, old_recovery_email, new_recovery_email)
        
        # Log change
        log_set_recovery_email(200, f"Old recovery: {anonymized_old_recovery_email}, new: {anonymized_recovery_email}", user_agent, client_ip, user.id)
    else:
        # Confirm change to user's email
        send_recovery_email_set_email(user.name, user.email, new_recovery_email)
        
        # Log set
        log_set_recovery_email(201, f"Recovery set to: {anonymized_recovery_email}", user_agent, client_ip, user.id)
    

    response_data = {
            "response":"Recovery email added successfully!",
            "recovery_email_added": True,
            "recovery_email_preview": anonymized_recovery_email
        }
    return jsonify(response_data)

####################################
#        GET RECOVERY STATUS       #
####################################

@recovery.route("/get_recovery_status")
@login_required
def get_recovery_status():
    """
    get_recovery_status() -> JsonType
    ----------------------------------------------------------

    Route sends user's recovery_email. 
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "recovery_email_preview" value only included if recovery_email_added is true.

    ----------------------------------------------------------
    **Response example:**

    # If recovery_email is "john@email.com", it's preview will be:

    ```python
        response_data = {
                "response":"success",
                "recovery_email_added": true,
                "recovery_email_preview": "j***@e***.com" 
            }
    ``` 
    """
    # Get the recovery email (it may be None or a string)
    recovery_email = current_user.recovery_email

    # Determine if a recovery email was added
    recovery_email_added = bool(recovery_email and recovery_email.strip())

    # Anonymize email if it's provided
    anonymized_recovery_email = anonymize_email(recovery_email) if recovery_email_added else ""

    response_data = {
            "response":"success",
            "recovery_email_added": recovery_email_added,
            "recovery_email_preview": anonymized_recovery_email
        }
    return jsonify(response_data)

####################################
#        GET RECOVERY EMAIL        #
####################################

@recovery.route("/get_recovery_email", methods=["POST"])
@login_required
@limiter.limit("5/minute;10/day")
@validate_schema(get_recovery_email_schema) 
def get_recovery_email():
    """
    get_recovery_email() -> JsonType
    ----------------------------------------------------------

    Route sends user's recovery_email. 
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "recovery_email" value only included if response is "success".

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "recovery_email": "john@email.com" 
            }
    ``` 
    """
    # Get the JSON data from the request body 
    json_data = request.get_json()
    password = json_data["password"]
    user_agent = json_data.get("user_agent", "") 
    
    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Standard response
    error_401 = {"response": "Wrong password."}
    error_422 = {"response": "No recovery email found."}
    error_440 = {"response": "Session expired. Please log in again."}

    # Get user
    user = svc_get_user_or_none(current_user.email, "get_recovery_email")
    if user is None:
        log_get_recovery_email(440, "Session did not return current user.", user_agent, client_ip, 0)
        return jsonify(error_440), 440

    # Check password     
    pw_ok = svc_is_pw_or_otp_valid(user, password, "password")
    if not pw_ok:
        log_get_recovery_email(401, "Wrong password input.", user_agent, client_ip, user.id)
        return jsonify(error_401 ), 401

    # Get the recovery email (it may be None or a string)
    recovery_email = user.recovery_email

    if not recovery_email:
        log_get_recovery_email(422, "", user_agent, client_ip, user.id)
        return jsonify(error_422 ), 422
    
    log_get_recovery_email(200, "", user_agent, client_ip, user.id)

    response_data = {
            "response":"success",
            "recovery_email": recovery_email
        }
    return jsonify(response_data)

####################################
#      DELETE RECOVERY EMAIL       #
####################################

@recovery.route("/delete_recovery_email", methods=["POST"])
@login_required
@limiter.limit("5/minute;10/day")
@validate_schema(delete_recovery_email_schema) 
def delete_recovery_email():
    """
    delete_recovery_email() -> JsonType
    ----------------------------------------------------------

    Route deletes the user's recovery_email. 
    PS: FE should make sure user is aware that this action will disable MFA.
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "recovery_email_added" value only included if response is 200. 
    - "recovery_email_preview" value only included if response is 200.

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"Recovery email deleted sucessfully!",
                "recovery_email_added": false,
                "recovery_email_preview": "" 
            }
    ```
    """
    # Get the JSON data from the request body 
    json_data = request.get_json()
    password = json_data["password"]
    user_agent = json_data.get("user_agent", "") 
    
    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Standard response
    error_401 = {"response": "Wrong password."}
    error_422 = {"response": "No recovery email found."}
    error_440 = {"response": "Session expired. Please log in again."}
    error_500 = {"response": "An error occurred, please try again."}

    # Get user
    user = svc_get_user_or_none(current_user.email, "delete_recovery_email")
    if user is None:
        log_delete_recovery_email(440, "Session did not return current user.", user_agent, client_ip, 0)
        return jsonify(error_440), 440
    
    # Check password     
    pw_ok = svc_is_pw_or_otp_valid(user, password, "password")
    if not pw_ok:
        log_delete_recovery_email(401, "Wrong password input.", user_agent, client_ip, user.id)
        return jsonify(error_401 ), 401
    
    # Check whether recovery email exists
    if not user.recovery_email:
        log_delete_recovery_email(422, "No recovery email found.", user_agent, client_ip, user.id)
        return jsonify(error_422 ), 422
    
    # Save current user data:
    mfa_was_enabled = user.mfa_enabled
    old_recovery_email = user.recovery_email

    # Delete the recovery email
    recovery_deleted = svc_delete_recovery_email(user)
    if not recovery_deleted:
        log_delete_recovery_email(500, "Could not delete recovery email: DB failure or incorrect user.", user_agent, client_ip, user.id)
        return jsonify(error_500), 500
    
    # Send confirmation emails that recovery has been removed to main email and old recovery email
    send_email_recovery_deletion(user.name, user.email, old_recovery_email)
    
    # Log
    if mfa_was_enabled:
        log_delete_recovery_email(201, "", user_agent, client_ip, user.id)
    else:
        log_delete_recovery_email(200, "", user_agent, client_ip, user.id)

    #TODO: check if FE requires new MFA data

    response_data = {
            "response":"Recovery email deleted successfully!",
            "recovery_email_added": False,
            "recovery_email_preview": ""
        }
    return jsonify(response_data)

