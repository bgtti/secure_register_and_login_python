# Python/Flask libraries
from flask import Blueprint, request, jsonify
import logging

# Extensions and configurations
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_required

from app.models.user import User
from app.models.stats import UserStats

# Common / Utils
# from app.utils.log_event_utils.log import log_event
from app.common.custom_decorators.admin_protected_route import admin_only
from app.common.custom_decorators.json_schema_validator import validate_schema
from app.common.ip_utils.ip_address_validation import get_client_ip
from app.common.log_utils.log_data_sanitation import safe_to_log

# Services
from app.services.user.user_flag_service import svc_user_flag_change
from app.services.user.user_service import svc_get_user_by_id, svc_delete_user
from app.services.user.user_role_service import (
    svc_make_user_admin,
    svc_make_user_role_user
)
from app.services.user.user_access_service import svc_set_user_blocked


# JSON Schema
from app.routes.admin.user_action.schemas import change_user_flag_schema,user_role_change_schema, block_and_unblock_user_schema, admin_delete_user_schema

# Logging
from app.routes.admin.user_action.routes import (
    log_admin_change_user_flag,
    log_user_role_change,
    log_user_block_status,
    log_user_deleted_by_admin
)



# Blueprint
from . import user_action

# In this file: routes that modify user-related information (to be accessed by admin users only) 
#   - change a user's flag colour, 
#   - change a user's access type (eg: give a user admin privileges), 
#   - block/unblock a user, 
#   - adelete a user 

# View functions in this file modify information in the db

# ----- ACTION: CHANGE USER FLAG -----
@user_action.route("/change_user_flag", methods=["POST"])
@login_required
@admin_only
@validate_schema(change_user_flag_schema)
def change_user_flag():
    """
    Route to change a user's flag by id.
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get JSON payload 
    user_id = json_data["user_id"]
    flag_colour = json_data["new_flag_colour"]

    # Get info from request
    user_agent = request.headers.get("User-Agent", "")
    client_ip = get_client_ip(request) or ""

    # Error messages
    error_404 = {"response": "Error: user not found."}
    error_500 = {"response": "System error: could not change flag."}

    user = svc_get_user_by_id(user_id)

    if not user:
        txt = f"User id={user_id} not found."
        log_admin_change_user_flag(404, txt, user_agent, client_ip, current_user.id)
        return jsonify(error_404), 404 
    
    # Save old flag
    old_flag = user.flagged

    # Change flag
    change_ok = svc_user_flag_change(user_id, flag_colour)

    if not change_ok:
        txt = f"User id={user_id} flag could not be changed from {old_flag} to {flag_colour}"
        log_admin_change_user_flag(500, txt, user_agent, client_ip, current_user.id)
        return jsonify(error_500), 500
    
    txt = f"User id={user_id} flag changed from {old_flag} to {flag_colour}"
    log_admin_change_user_flag(500, txt, user_agent, client_ip, current_user.id)
    
    return jsonify({"response": "success"}), 200


    
# ----- ACTION: CHANGE USER ACCESS TYPE -----
@user_action.route("/user_role_change", methods=["POST"])
@login_required
@admin_only
@validate_schema(user_role_change_schema)
def user_role_change():
    """
    Route to change a user's access type (role).
    Takes a JSON payload with the following parameters:
    - "user_id": id of the user whose role should be changed.
    - "new_role": Should be either "admin" or "user" (according to ROLES constant).
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get JSON payload 
    user_id = json_data["user_id"]
    new_role = json_data["new_role"]

    # Get info from request
    user_agent = request.headers.get("User-Agent", "")
    client_ip = get_client_ip(request) or ""

    # Responses
    success = {"response": "success."}
    error_403 = {"response": "Request denied."}
    error_404 = {"response": "User type (role) not found."}
    error_500 = {"response": "System error: could not change user's role."}

    if user_id == current_user.id:
        logging.warning(f"User={current_user.id} attempted to change own role to {new_role}.")
        txt = f"User attempted to change own role to {new_role}."
        log_user_role_change(403, txt, user_agent, client_ip, current_user.id)
        return jsonify(error_403), 403
    
    # PS: Currently only super_admin is able to promote/demote users
    if not current_user.is_super_admin:
        logging.warning(f"User={current_user.id} attempted to change role of user id= {user_id} to {new_role}.")
        txt = f"Non-super user attempted to change user id={user_id} role to {new_role}."
        log_user_role_change(403, txt, user_agent, client_ip, current_user.id)
        return jsonify(error_403), 403

    txt = f"Could not change user id={user_id} role to {new_role}."

    if new_role == "admin":
        if not svc_make_user_admin(user_id, True):
            log_user_role_change(500, txt, user_agent, client_ip, current_user.id)
            return jsonify(error_500), 500
        
    elif new_role == "user":
        if not svc_make_user_role_user(user_id, True):
            log_user_role_change(500, txt, user_agent, client_ip, current_user.id)
            return jsonify(error_500), 500
        
    elif new_role == "super_admin":
        txt = f"Attempt to change user id={user_id} role to {new_role}."
        logging.warning(txt)
        log_user_role_change(403, txt, user_agent, client_ip, current_user.id)
        return jsonify(error_403), 403
    
    else:
        log_user_role_change(404, txt, user_agent, client_ip, current_user.id)
        return jsonify(error_404), 404
    
    txt = f"Changed user id={user_id} role to {new_role}."
    log_user_role_change(200, txt, user_agent, client_ip, current_user.id)
    
    return jsonify(success), 200


# ----- ACTION: BLOCK/UNBLOCK -----
@user_action.route("/block_unblock", methods=["POST"])
@login_required
@admin_only
@validate_schema(block_and_unblock_user_schema)
def block_unblock_user():
    """
    Route to block or unblock a user by id.
    Takes a JSON payload with the following parameters:
    - "user_id": id of the user to block/unblock.
    - "block_status": Set to true if the user should be blocked, false to unblock.
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get id and block status from JSON payload
    user_id = json_data["user_id"]
    block_status = json_data["block"]

    # Get info from request
    user_agent = request.headers.get("User-Agent", "")
    client_ip = get_client_ip(request) or ""

    # Responses
    success = {"response": "success."}
    error_403 = {"response": "Request denied."}
    error_404 = {"response": "User not found."}
    error_500 = {"response": "System error: could not change user's block status."}

    if user_id == current_user.id:
        txt = f"User={current_user.id} attempted to set self.is_blocked={block_status}."
        logging.warning(txt)
        log_user_block_status(403, txt, user_agent, client_ip, current_user.id)
        return jsonify(error_403), 403
    
    user = svc_get_user_by_id(user_id)

    if not user:
        txt = f"User={current_user.id} attempted to set is_blocked={block_status} to user id={user_id}, but user was not found."
        log_user_block_status(404, txt, user_agent, client_ip, current_user.id)
        return jsonify(error_404), 404
    
    status_ok =  svc_set_user_blocked(user=user, is_blocked=True, commit=True)

    if status_ok:
        txt = f"User={current_user.id} changed user={user_id} is_blocked to {block_status}."
        logging.info(txt)
        log_user_block_status(200, txt, user_agent, client_ip, current_user.id)
        return jsonify(success), 200
    
    txt = f"Error: user={current_user.id} did not change user={user_id} is_blocked to {block_status}."
    logging.info(txt)
    log_user_block_status(500, txt, user_agent, client_ip, current_user.id)
    return jsonify(error_500), 500

    

# ----- ACTION: DELETE USER -----
@user_action.route("/delete_user", methods=["POST"])
@login_required
@admin_only
@validate_schema(admin_delete_user_schema)
def admin_delete_user():
    """
    Route to delete a user by id.
    Takes a JSON payload with the following parameters:
    - "user_id": User's id to be deleted.
    - "reason": Reason given so that user is deleted.
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get id from JSON payload
    user_id = json_data["user_id"]
    reason = json_data["reason"]

    reason_sanitized = safe_to_log(reason)

    # Get info from request
    user_agent = request.headers.get("User-Agent", "")
    client_ip = get_client_ip(request) or ""

    # Responses
    success = {"response": "success."}
    error_403 = {"response": "Request denied."}
    error_404 = {"response": "User not found."}
    error_500 = {"response": "System error: could not delete user."}

    #NOTE: this will perform a hard delete! Consider soft-deletion!

    if user_id == current_user.id:
        txt = f"Error: wrong method to delete own account. Reason given for deletion: {reason_sanitized}"
        log_user_deleted_by_admin(405, txt, user_agent, client_ip, current_user.id)
        return jsonify(error_403), 403
    
    user = svc_get_user_by_id(user_id)

    if not user:
        txt = f"Error: user={user_id} not found. Reason given for deletion: {reason_sanitized}"
        log_user_deleted_by_admin(404, txt, user_agent, client_ip, current_user.id)
        return jsonify(error_404), 404
    
    # Super_admin cannot be deleted
    if user.is_super_admin:
        logging.warning(f"User={current_user.id} attempted to delete super_user.")
        txt = f"Error: super user cannot be deleted. Reason given for deletion: {reason_sanitized}"
        log_user_deleted_by_admin(403, txt, user_agent, client_ip, current_user.id)
        return jsonify(error_403), 403
    
    # If user is admin, can only be deleted by super_user
    if user.is_admin and not current_user.is_super_admin:
        logging.warning(f"User={current_user.id} attempted to delete admin id={user_id}.")
        txt = f"Error: only super admins may delete admins. User to be deleted: id={user_id}. Reason given for deletion: {reason_sanitized}"
        log_user_deleted_by_admin(403, txt, user_agent, client_ip, current_user.id)
        return jsonify(error_403), 403
    
    user_deleted = svc_delete_user(user, True)

    if user_deleted:
        logging.info(f"User={current_user.id} deleted user={user_id}. Given reason: {reason_sanitized}")
        txt = f"User deleted: id={user_id}. Reason given for deletion: {reason_sanitized}"
        log_user_deleted_by_admin(200, txt, user_agent, client_ip, current_user.id)
        return jsonify(success), 200
    
    txt = f"Error: could not delete user. User to be deleted: id={user_id}. Reason given for deletion: {reason_sanitized}"
    log_user_deleted_by_admin(500, txt, user_agent, client_ip, current_user.id)
    
    return jsonify(error_500), 500
