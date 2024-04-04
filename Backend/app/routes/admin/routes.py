from flask import Blueprint, request, jsonify, session
# from functools import wraps
# import pdb; pdb.set_trace()
import logging
# import jsonschema
from datetime import datetime, timezone, timedelta
from sqlalchemy import desc, asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import escape_like
from flask_login import current_user, login_required
from app.extensions import db, limiter
from app.routes.admin.schemas import admin_users_table_schema, admin_user_information, admin_user_logs_schema, admin_user_flag_change,admin_user_access_type_change, admin_block_and_unblock_user_schema, admin_delete_user_schema
from app.models.user import User
from app.models.log_event import LogEvent
from app.models.stats import UserStats
from app.utils.constants.enum_class import modelBool, UserAccessLevel, UserFlag
from app.utils.constants.enum_helpers import map_string_to_enum
from app.utils.detect_html.detect_html import check_for_html
from app.utils.log_event_utils.log import log_event
from app.utils.custom_decorators.admin_protected_route import admin_only
from app.utils.custom_decorators.json_schema_validator import validate_schema


admin = Blueprint('admin', __name__)

# In this file: routes concerning admin  

# DASHBOARD
@admin.route("/restricted_area/dashboard", methods=["POST"])
def admin_dashboard():
    # ...
    return jsonify({'response': '...'})

# USERS TABLE 
@admin.route("/restricted_area/users/users_table", methods=["POST"])
@limiter.limit("200/hour")
@login_required
@admin_only
@validate_schema(admin_users_table_schema)
def admin_users_table():
    """
    admin_users_table() -> JsonType
    ----------------------------------------------------------
    Route with no parameters.
    Sets a session cookie in response.
    Returns Json object containing strings.
    "response" value is always included.
    If response is "success", it will also be included the
    current_page, the total_pages, the original query, and the
    users array of dictionary.  
    ----------------------------------------------------------
    Response example:
    response_data = {
            "response":"success",
            "current_page": 1,
            "total_pages": 5,
            "query": {
                "filter_by": "none",
                "filter_by_flag": "blue",
                "filter_by_last_seen": "2024-01-01",
                "items_per_page": 25,
                "order_sort": "descending",
                "ordered_by": "last_seen",
                "page_nr": 1,
                "search_by": "email",
                "search_word": "frank",
            },
            "users": [
                {
                "id": 10
                "name": "Frank Torres",
                "email": "frank.torres@fakemail.com",
                "last_seen": "Thu, 25 Jan 2024 00:00:00 GMT",
                "access": "user",
                "flagged": "blue",
                "is_blocked": "false"
                }, 
                ...
            ]
        } 
    """
    # Get the JSON data from the request body 
    json_data = request.get_json()
    
    # Setting defaults to optional arguments:
    page_nr = json_data["page_nr"]
    items_per_page = json_data.get("items_per_page", 25)
    order_by = json_data.get("order_by", "last_seen")
    order_sort = json_data.get("order_sort", "descending")
    filter_by = json_data.get("filter_by", "none")
    filter_by_flag = json_data.get("filter_by_flag", "blue")
    filter_by_last_seen = json_data.get("filter_by_last_seen", "") 
    search_by = json_data.get("search_by", "none")
    search_word = json_data.get("search_word", "")

    # Check if search is valid
    if not search_word:
        search_by = "none"
    else:
        # Check for html in user input
        html_in_input = check_for_html(search_word, "admin_users_table - search_word field")
        if html_in_input:
            logging.warning(f"Admin input may include html. Possible vulnerability? Input in user search: {search_word}")

    # Determine the ordering based on user input
    ordering = User.__dict__.get(order_by, None)
    if ordering is None:
        return jsonify({"response": "Invalid order_by field."}), 400

    if order_sort == "descending":
        ordering = ordering.desc()
    else:
        ordering = ordering.asc()

    if filter_by != "none":
        filter_conditions_map = {
            "is_blocked": User.is_blocked == modelBool.TRUE,
            "is_unblocked": User.is_blocked == modelBool.FALSE,
            "flag": User.flagged == map_string_to_enum(filter_by_flag, UserFlag),
            "flag_not_blue": User.flagged != UserFlag.BLUE,
            "is_admin": User.access_level == UserAccessLevel.ADMIN,
            "is_user": User.access_level == UserAccessLevel.USER,
            "last_seen": User.last_seen >= filter_by_last_seen if filter_by_last_seen != "" else User.last_seen >= (datetime.now(timezone.utc) - timedelta(30)),
        }
    if search_by != "none":
        search_conditions_map = {
            "name":User.name.ilike(f"%{search_word}%"),
            "email": User.email.ilike(f"%{search_word}%")
        }
        
    filter_case = (filter_by == "none", search_by == "none")

    match filter_case:
        case (True, True):
            users = User.query.order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False)
        case (True, False):
            users = User.query.filter(search_conditions_map[search_by]).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False)
        case (False, True):
            users = User.query.filter(filter_conditions_map[filter_by]).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False)
        case (False, False):
            users = User.query.filter(filter_conditions_map[filter_by], search_conditions_map[search_by]).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False)
        case _:
            logging.error(f"User table could not be retrieved as criteria was not met.")
            return jsonify({"response": "Could not match search criteria"}), 404

    if not users.items:
        return jsonify({"response": "Requested page out of range"}), 404
    
    
    response_data ={
            "response":"success",
            "users": [user.serialize_user_table() for user in users.items if user.access_level != UserAccessLevel.SUPER_ADMIN],
            "total_pages": users.pages,
            "current_page": users.page,
            "query":{
                "page_nr": page_nr,
                "items_per_page": items_per_page,
                "ordered_by": order_by,
                "order_sort": order_sort,
                "filter_by": filter_by,
                "filter_by_flag": filter_by_flag,
                "filter_by_last_seen": filter_by_last_seen,
                "search_by": search_by,
                "search_word": search_word,
            }
        }
    
    return jsonify(response_data)

# USERS TABLE INFO 
@admin.route("/restricted_area/users/user_information", methods=["POST"])
@login_required
@admin_only
@validate_schema(admin_user_information)
def admin_user_information():
    """
    admin_user_information() -> JsonType
    ----------------------------------------------------------
    Route to get a user's base information.
    Takes a JSON payload with the following parameter:
    - "user_id": User's id to be queried.

    Returns a JSON object with a "response" field. User information only sent if response is 200.
    ----------------------------------------------------------
    Request example:
    json_payload = {
        "user_id": 12345
    }
    ----------------------------------------------------------
    Response examples:

    {"response": "Requested page out of range"}

    {
        "response":"success",
        "user":      {
                "id": 12345
                "name": "Frank Torres",
                "email": "frank.torres@fakemail.com",
                "last_seen": "Thu, 25 Jan 2024 00:00:00 GMT",
                "access": "user",
                "flagged": "blue",
                "is_blocked": "false"
                }, 
    }
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get info from JSON payload
    user_id = json_data["user_id"]

    # Get user info
    try:
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return jsonify({"response": "User not found."}), 404
    except Exception as e:
        logging.error(f"Failed to access db. Error: {e}")
        return jsonify({"response": "Error prevented user from being queried"}), 500
    
    response_data ={
            "response":"success",
            "user": user.serialize_user_table(),
        }
    
    return jsonify(response_data)

# USERS TABLE LOGS 
@admin.route("/restricted_area/users/user_logs", methods=["POST"])
@login_required
@admin_only
@validate_schema(admin_user_logs_schema)
def admin_user_logs():
    """
    admin_user_logs() -> JsonType
    ----------------------------------------------------------
    Route to get a user's logs.
    Takes a JSON payload with the following parameters:
    - "user_id": User's id to be queried.
    - "page_nr": int used for pagination.

    Returns a JSON object with a "response" field. Logs and other information only sent if response is 200.
    ----------------------------------------------------------
    Request example:
    json_payload = {
        "user_id": 12345,
        "page_nr": 1
    }
    ----------------------------------------------------------
    Response examples:

    {"response": "Requested page out of range"}

    {"response":"success",
            "logs": {
                "user_id": 12345,
                "created_at": "Thu, 25 Jan 2024 00:00:00 GMT",
                "type": "INFO",
                "activity": "login",
                "message": "login rejected: user is blocked."
                },
                ...
            "total_pages": 2,
            "current_page": 1,
            "query":{
                "page_nr": 1,
                "items_per_page": 25,
                "ordered_by": "created_at",
                "order_sort": "descending",
            }
    }
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get info from JSON payload
    user_id = json_data["user_id"]
    page_nr = json_data["page_nr"]

    try:
        user_logs = LogEvent.query.filter_by(user_id=user_id).order_by(LogEvent.created_at.desc()).paginate(page=page_nr, per_page=25, error_out=False)
        if not user_logs.items:
            return jsonify({"response": "Requested page out of range"}), 404
    except Exception as e:
        logging.error(f"Error prevented eventLogs to be queried: {e}")
        return jsonify({"response": "Error prevented logs from being queried"}), 500
    
    response_data ={
            "response":"success",
            "logs": [log.serialize_user_logs() for log in user_logs.items],
            "total_pages": user_logs.pages,
            "current_page": user_logs.page,
            "query":{
                "page_nr": page_nr,
                "items_per_page": 25,
                "ordered_by": "created_at",
                "order_sort": "descending",
            }
        }
    
    return jsonify(response_data)

# USERS TABLE CHANGE USER FLAG
@admin.route("/restricted_area/users/flag_change", methods=["POST"])
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

            log_event("ADMIN_FLAG_USER","flag changed",user.id, f"Previous flag: {old_flag} New flag: {flag_colour}.")
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
        return jsonify({"response": "Error deleting user", "error": str(e)}), 500
    
    except Exception as e:
        logging.error(f"Error prevented user flag change: {e}")
        try:
            log_event("ADMIN_FLAG_USER","flag change problem",0, f"User id {user_id}, error raised.")
        except Exception as e:
            logging.error(f"Error prevented user flag change log to be saved: {e}")
        return jsonify({"response": "Error changing user flag", "error": str(e)}), 500
    
# USERS TABLE CHANGE USER ACCESS TYPE
@admin.route("/restricted_area/users/access_change", methods=["POST"])
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
            log_event("ADMIN_USER_ACCESS_CHANGE","access changed",user.id, f"Previous access type: {current_type} New: {user_type}.")
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
        return jsonify({"response": "Error deleting user", "error": str(e)}), 500
    
    except Exception as e:
        logging.error(f"Error prevented user type change: {e}")
        try:
            log_event("ADMIN_USER_ACCESS_CHANGE","access change problem",0, f"User id {user_id}, error raised.")
        except Exception as e:
            logging.error(f"Error prevented user access change log to be saved: {e}")
        return jsonify({"response": "Error changing user type", "error": str(e)}), 500


# USERS TABLE BLOCK/UNBLOCK
@admin.route("/restricted_area/users/block_unblock", methods=["POST"])
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
                log_event("ADMIN_BLOCK_USER","unblock user",user.id)

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
        return jsonify({"response": "Error deleting user", "error": str(e)}), 500
    
    except Exception as e:
        logging.error(f"Error prevented user block/unblock: {e}")
        if block_status:
            log_event("ADMIN_BLOCK_USER","block problem",user.id)
        else:
            log_event("ADMIN_BLOCK_USER","unblock problem",user.id)
        return jsonify({"response": "Error blocking/unblocking user", "error": str(e)}), 500
    

# USERS TABLE DELETE 
@admin.route("/restricted_area/users/delete", methods=["POST"])
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
            log_event("ADMIN_DELETE_USER","deletion successful",user.id)

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
        return jsonify({"response": "Error deleting user", "error": str(e)}), 500

    except Exception as e:
        logging.error(f"Error prevented user deletion: {e}")
        log_event("ADMIN_DELETE_USER","deletion problem",user.id)
        return jsonify({"response": "Error deleting user", "error": str(e)}), 500
    
