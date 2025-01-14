from flask import Blueprint, request, jsonify
import logging
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_required
from app.extensions.extensions import db
from app.routes.admin.user_action.schemas import admin_user_flag_change,admin_user_access_type_change, admin_block_and_unblock_user_schema, admin_delete_user_schema
from app.models.user import User
from app.models.stats import UserStats
from app.utils.constants.enum_class import UserAccessLevel, UserFlag
from app.utils.constants.enum_helpers import map_string_to_enum
from app.utils.log_event_utils.log import log_event
from app.utils.custom_decorators.admin_protected_route import admin_only
from app.utils.custom_decorators.json_schema_validator import validate_schema

user_action = Blueprint('user_action', __name__)

# In this file: routes that modify user-related information (to be accessed by admin users only) 
#   - change a user's flag colour, 
#   - change a user's access type (eg: give a user admin privileges), 
#   - block/unblock a user, 
#   - adelete a user 

# View functions in this file modify information in the db

# ----- ACTION: CHANGE USER FLAG -----
@user_action.route("/flag_change", methods=["POST"])
@login_required
@admin_only
@validate_schema(admin_user_flag_change)
def change_user_flag():
    """
    change_user_flag() -> JsonType
    ----------------------------------------------------------
    Route to change a user's flag by id.
    Takes a JSON payload with the following parameters:
    - "user_id": id of the user to block/unblock.
    - "new_flag_colour": Should be a value from UserFlag enum class in string form.

    Returns a JSON object with a "response" field:
    - If flag colour change is successful: {"response": "success"}
    - If the id is not found: {"response": "User not found"}
    - If an error occurs during the operation: {"response": "Error changing user flag", "error": "Details of the error"}

    ----------------------------------------------------------
    Request example:
    json_payload = {
        "user_id": 12345,
        "new_flag_colour": "red"
    }
    ----------------------------------------------------------
    Response examples:
    {"response": "success"}
    {"response": "User not found"}
    {"response": "Error changing user flag", "error": "Details of the error"}
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get JSON payload 
    user_id = json_data["user_id"]
    flag_colour = json_data["new_flag_colour"]

    # Make sure flag exists
    flag = map_string_to_enum(flag_colour, UserFlag)
    if flag == None:
        return jsonify({"response": "Flag colour not found"}), 404

    try:
        user = User.query.filter_by(id=user_id).first()

        if user:
            old_flag = user.flagged
            user.flag_change(flag_colour)
            db.session.commit()

            log_event("ADMIN_FLAG_USER","flag changed",user.id, f"Previous flag: {old_flag} New flag: {flag_colour}. Admin action from: {current_user.email}.") 
            return jsonify({"response": "success"})
        else:
            log_event("ADMIN_FLAG_USER","flag change problem",0, f"User id {user_id} lead to 404 not found.")
            logging.info(f"User id={user_id} could not be found, 404 not found.") 
            return jsonify({"response": "User not found"}), 404
        
    except IntegrityError as e:
        # Handle database integrity error (e.g., foreign key constraint)
        db.session.rollback()
        logging.error(f"DB integrity error prevented user flag change: {e}")
        try:
            log_event("ADMIN_FLAG_USER","flag change problem",0, f"User id {user_id}, integrity error raised.")
        except Exception as e:
            logging.error(f"Error prevented user flag change log to be saved: {e}")
        return jsonify({"response": "Error changing user flag - integrity error"}), 500
    
    except Exception as e:
        logging.error(f"Error prevented user flag change: {e}")
        try:
            log_event("ADMIN_FLAG_USER","flag change problem",0, f"User id {user_id}, error raised.")
        except Exception as e:
            logging.error(f"Error prevented user flag change log to be saved: {e}")
        return jsonify({"response": "Error changing user flag"}), 500
    
# ----- ACTION: CHANGE USER ACCESS TYPE -----
@user_action.route("/access_change", methods=["POST"])
@login_required
@admin_only
@validate_schema(admin_user_access_type_change)
def change_user_access():
    """
    change_user_access() -> JsonType
    ----------------------------------------------------------
    Route to change a user's access type by id.
    Takes a JSON payload with the following parameters:
    - "user_id": id of the user to block/unblock.
    - "new_type": Should be either "admin" or "user".

    Returns a JSON object with a "response" field:
    - If type change is successful: {"response": "success"}
    - If the id is not found: {"response": "User not found"}
    - If an error occurs during the operation: {"response": "Error changing user type", "error": "Details of the error"}

    ----------------------------------------------------------
    Request example:
    json_payload = {
        "user_id": 12345,
        "new_type": "admin"
    }
    ----------------------------------------------------------
    Response examples:
    {"response": "success"}
    {"response": "User not found"}
    {"response": "Error changing user type", "error": "Details of the error"}
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get JSON payload 
    user_id = json_data["user_id"]
    user_type = json_data["new_type"]

    try:
        user = User.query.filter_by(id=user_id).first()

        if user:
            current_type = user.access_level

            if user_type == "admin":

                if current_type == UserAccessLevel.ADMIN:
                    return jsonify({"response": "success"})
                else:
                    if current_user.access_level != UserAccessLevel.SUPER_ADMIN:
                        return jsonify({"response": "Users can only get admin permissions from the super admin."}), 403
                    else:
                        user.make_user_admin()
            else:
                user.make_user_regular_user()

            db.session.commit()

            log_event("ADMIN_USER_ACCESS_CHANGE","access changed",user.id, f"Previous access type: {current_type.value} New access type: {user_type.value}. Admin action from: {current_user.email}.")
            return jsonify({"response": "success"})
        else:
            log_event("ADMIN_USER_ACCESS_CHANGE","access change problem",0, f"User id {user_id} lead to 404 not found.")
            logging.info(f"User id={user_id} could not be found, 404 not found.") 
            return jsonify({"response": "User not found"}), 404
        
    except IntegrityError as e:
        # Handle database integrity error (e.g., foreign key constraint)
        db.session.rollback()
        logging.error(f"DB integrity error prevented user type change: {e}")
        try:
            log_event("ADMIN_USER_ACCESS_CHANGE","access change problem",0, f"User id {user_id}, integrity error raised.")
        except Exception as e:
            logging.error(f"Error prevented user access change log to be saved: {e}")
        return jsonify({"response": "Error deleting user"}), 500
    
    except Exception as e:
        logging.error(f"Error prevented user type change: {e}")
        try:
            log_event("ADMIN_USER_ACCESS_CHANGE","access change problem",0, f"User id {user_id}, error raised.")
        except Exception as e:
            logging.error(f"Error prevented user access change log to be saved: {e}")
        return jsonify({"response": "Error changing user type"}), 500


# ----- ACTION: BLOCK/UNBLOCK -----
@user_action.route("/block_unblock", methods=["POST"])
@login_required
@admin_only
@validate_schema(admin_block_and_unblock_user_schema)
def block_unblock_user():
    """
    block_unblock_user() -> JsonType
    ----------------------------------------------------------
    Route to block or unblock a user by id.
    Takes a JSON payload with the following parameters:
    - "user_id": id of the user to block/unblock.
    - "block": Set to true if the user should be blocked, false to unblock.

    Returns a JSON object with a "response" field:
    - If blocking/unblocking is successful: {"response": "success"}
    - If the id is not found: {"response": "User not found"}
    - If an error occurs during the operation: {"response": "Error blocking/unblocking user", "error": "Details of the error"}

    ----------------------------------------------------------
    Request example:
    json_payload = {
        "user_id": 12345,
        "block": true
    }
    ----------------------------------------------------------
    Response examples:
    {"response": "success"}
    {"response": "User not found"}
    {"response": "Error blocking/unblocking user", "error": "Details of the error"}
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get id and block status from JSON payload
    user_id = json_data["user_id"]
    block_status = json_data["block"]

    try:
        user = User.query.filter_by(id=user_id).first()

        if user:

            if block_status:
                user.block_access()
                log_event("ADMIN_BLOCK_USER","block user",user.id)
            else:
                user.unblock_access()
                log_event("ADMIN_BLOCK_USER","unblock user",user.id, f"Admin action from: {current_user.email}." )

            db.session.commit()
            logging.info(f"User successfully set to blocked={block_status} by admin.") 
            return jsonify({"response": "success"})
        else:
            logging.info(f"User could not be set to blocked={block_status}, 404 not found.") 
            return jsonify({"response": "User not found"}), 404
        
    except IntegrityError as e:
        # Handle database integrity error (e.g., foreign key constraint)
        db.session.rollback()
        logging.error(f"DB integrity error prevented user block/unblock: {e}")
        if block_status:
            log_event("ADMIN_BLOCK_USER","block problem",user.id)
        else:
            log_event("ADMIN_BLOCK_USER","unblock problem",user.id)
        return jsonify({"response": "Error deleting user", "error": "An internal error has occurred."}), 500
    
    except Exception as e:
        logging.error(f"Error prevented user block/unblock: {e}")
        if block_status:
            log_event("ADMIN_BLOCK_USER","block problem",user.id)
        else:
            log_event("ADMIN_BLOCK_USER","unblock problem",user.id)
        return jsonify({"response": "Error blocking/unblocking user", "error": "An internal error has occurred."}), 500
    

# ----- ACTION: DELETE USER -----
@user_action.route("/delete_user", methods=["POST"])
@login_required
@admin_only
@validate_schema(admin_delete_user_schema)
def admin_delete_user():
    """
    admin_delete_user() -> JsonType
    ----------------------------------------------------------
    Route to delete a user by id.
    Takes a JSON payload with the following parameters:
    - "user_id": User's id to be deleted.

    Returns a JSON object with a "response" field:
    - If deletion is successful: {"response": "success"}
    - If the id is not found: {"response": "User not found"}
    - If an error occurs during deletion: {"response": "Error deleting user", "error": "Details of the error"}

    ----------------------------------------------------------
    Request example:
    json_payload = {
        "user_id": 12345
    }
    ----------------------------------------------------------
    Response examples:
    {"response": "success"}
    {"response": "User not found"}
    {"response": "Error deleting user", "error": "Details of the error"}
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get id from JSON payload
    user_id = json_data["user_id"]

    try:
        user = User.query.filter_by(id=user_id).first()

        if user:
            # Super Admin user should not be deleted
            if user.access_level == UserAccessLevel.SUPER_ADMIN:
                logging.warning(f"Blocked attempt to delete admin user.")
                return jsonify({"response": "Action forbidden to all users. Check the request parameters."}), 403
            # Admin user can only be deleted by the super admin
            elif user.access_level == UserAccessLevel.ADMIN:
                if current_user.access_level != UserAccessLevel.SUPER_ADMIN:
                    return jsonify({"response": "Admin users can only be deleted by the super admin."}), 403
        
            db.session.delete(user)
            db.session.commit()
            logging.info("User deleted successfully by admin.")
            log_event("ADMIN_DELETE_USER","deletion successful",user.id, f"Admin action from: {current_user.email}.")

            try:
                new_user_stats = UserStats(new_user=-1,country="")
                db.session.add(new_user_stats)
                db.session.commit()
            except Exception as e:
                logging.error(f"Admin deleted user but error prevented UserStats entry: {e}")

            # returns success even if stats could not be registered
            return jsonify({"response": "success"})
        else:
            return jsonify({"response": "User not found"}), 404

    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"DB integrity error prevented user deletion: {e}")
        log_event("ADMIN_DELETE_USER","deletion problem",user.id)
        return jsonify({"response": "Error deleting user"}), 500

    except Exception as e:
        logging.error(f"Error prevented user deletion: {e}")
        log_event("ADMIN_DELETE_USER","deletion problem",user.id)
        return jsonify({"response": "Error deleting user"}), 500