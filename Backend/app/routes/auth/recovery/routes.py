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
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.utils.detect_html.detect_html import check_for_html
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.profanity_check.profanity_check import has_profanity
from app.utils.salt_and_pepper.helpers import get_pepper

# Auth helpers
from app.routes.auth.helpers_auth import anonymize_email

# Recovery helpers 
from app.routes.auth.recovery.email import (
    send_email_recovery_set, 
    send_email_recovery_deletion, 
    send_email_change_and_set_recovery
    )

from app.routes.auth.recovery.log import (
    log_set_recovery_email,
    log_get_recovery_email,
    log_delete_recovery_email
)

from app.routes.auth.recovery.schemas import set_recovery_email_schema, get_recovery_email_schema, delete_recovery_email_schema

# Blueprint
from . import recovery


############# ROUTES ###############

####################################
#         SET RECOVERY EMAIL       #
####################################

@recovery.route("/set_recovery_email", methods=["POST"])
@login_required
@limiter.limit("5/minute;6/day")
@validate_schema(set_recovery_email_schema) 
def set_recovery_email(): 
    """
    get_otp() -> JsonType
    ----------------------------------------------------------

    Sets a recovery email to the user's account.
    
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
    # Standard error response
    error_response = {"response": "There was an error saving recovery email."} 

    # Get the JSON data from the request body 
    json_data = request.get_json()
    recovery_email = json_data["recovery_email"]
    password = json_data["password"]
    otp = json_data["otp"]
    user_agent = json_data.get("user_agent", "") 

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Get the user from cookie 
    try:
        user = User.query.filter_by(email=current_user.email).first()
    except Exception as e:
        log_message = f"Failed to retrieve user from database. Error: {str(e)}"
        logging.error(log_message)
        log_set_recovery_email(500, log_message, user_agent, client_ip, 0)
        return jsonify(error_response), 500
    
    # Recovery email should not be the same as email
    if user.email == recovery_email:
        user.otp_reset()
        db.session.commit()
        log_set_recovery_email(400, "", user_agent, client_ip, user.id)
        return jsonify({"response": "Recovery must be different than account email."} ), 400

    # Check password and OTP
    if user.check_otp(otp) is False:
        log_set_recovery_email(401, "Provided OTP is wrong or expired.", user_agent, client_ip, user.id)
        return jsonify({"response": "Provided OTP is wrong or expired."} ), 401
    
    salted_password = user.salt + password + get_pepper(user.created_at)
    if not flask_bcrypt.check_password_hash(user.password, salted_password):
        log_set_recovery_email(401, "Incorrect password.", user_agent, client_ip, user.id)
        return jsonify({"response": "Password incorrect."} ), 401

    try:
        if check_for_html(recovery_email, "set recovery email", recovery_email):
            user.flag = "YELLOW"
            log_set_recovery_email(207, f"Recovery set to: {recovery_email}", user_agent, client_ip, user.id)
        old_recovery_email = user.recovery_email
        user.recovery_email = recovery_email
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        log_message = f"Failed to save recovery email. Error: {str(e)}"
        logging.error(log_message)
        log_set_recovery_email(500, log_message, user_agent, client_ip, user.id)
        return jsonify(error_response), 500
    
    # Send confirmation emails that new recovery has been added 
    if old_recovery_email:
        #TODO: SSL issue not resolved
        send_email_change_and_set_recovery(user.name, user.email, old_recovery_email, recovery_email)
        log_set_recovery_email(204, f"Previous recovery email: {old_recovery_email}", user_agent, client_ip, user.id)
    else:
        send_email_recovery_set(user.name, user.email, recovery_email)

    # Log
    log_set_recovery_email(200, "", user_agent, client_ip, user.id)

    # Anonymize recovery email
    anonymized_recovery_email = anonymize_email(recovery_email)

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
    recovery_email_added = recovery_email is not None and recovery_email.strip() != ""

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
                "recovery_email": john@email.com" 
            }
    ``` 
    """
    # Get the JSON data from the request body 
    json_data = request.get_json()
    password = json_data["password"]
    user_agent = json_data.get("user_agent", "") 
    
    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Get the user from cookie
    try:
        user = User.query.filter_by(email=current_user.email).first()
    except Exception as e:
        log_message = f"Database query failed: {str(e)}"
        logging.error(log_message)
        log_get_recovery_email(500, log_message, user_agent, client_ip, 0)
        return jsonify({"response": "An error occurred while fetching the user."}), 500

    # Check password     
    salted_password = user.salt + password + get_pepper(user.created_at)
    if not flask_bcrypt.check_password_hash(user.password, salted_password):
        log_get_recovery_email(500, "Wrong password input.", user_agent, client_ip, user.id)
        return jsonify({"response": "Password incorrect."} ), 401

    # Get the recovery email (it may be None or a string)
    recovery_email = user.recovery_email

    if not recovery_email:
        log_get_recovery_email(404, "", user_agent, client_ip, user.id)
        return jsonify({"response": "No recovery email found."} ), 404
    
    log_get_recovery_email(100, "", user_agent, client_ip, user.id)

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

    # Get the user from cookie 
    try:
        user = User.query.filter_by(email=current_user.email).first()
    except Exception as e:
        log_message = f"Database query failed: {str(e)}"
        logging.error(log_message)
        log_delete_recovery_email(500, log_message, user_agent, client_ip, 0)
        return jsonify({"response": "An error occurred while fetching the user."}), 500

    # Check password     
    salted_password = user.salt + password + get_pepper(user.created_at)
    if not flask_bcrypt.check_password_hash(user.password, salted_password):
        log_delete_recovery_email(500, "Incorrect password input.", user_agent, client_ip, user.id)
        return jsonify({"response": "Password incorrect."} ), 401

    # Delete the recovery email
    try:
        old_recovery_email = user.recovery_email
        user.recovery_email = None
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        log_message = f"Failed to delete recovery email: {str(e)}"
        logging.error(log_message)
        log_delete_recovery_email(500, log_message, user_agent, client_ip, user.id)
        return {"response": "Failed to delete recovery email."}, 500
    
    # Send confirmation emails that recovery has been removed
    send_email_recovery_deletion(user.name, user.email, old_recovery_email)
    # try:
    #     mail_sent = send_email_recovery_deletion(user.name, user.email, old_recovery_email)
    #     if not mail_sent:
    #         logging.error(f"Failed to send confirmation emails of set account recovery email.")
    # except Exception as e:
    #     logging.error(f"Error encountered while trying to send confirmation of setting recovery email. Error: {e}")

    log_delete_recovery_email(200, "", user_agent, client_ip, user.id)

    response_data = {
            "response":"Recovery email deleted sucessfully!",
            "recovery_email_added": False,
            "recovery_email_preview": ""
        }
    return jsonify(response_data)

