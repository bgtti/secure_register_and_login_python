from flask import Blueprint, request, jsonify, session
# from functools import wraps
# import pdb; pdb.set_trace()
import logging
import jsonschema
from sqlalchemy import desc, asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import escape_like
from flask_login import current_user, login_required
from app.extensions import flask_bcrypt, db
from app.routes.admin.schemas import admin_users_table_schema, admin_user_logs_schema, admin_block_and_unblock_user_schema, admin_delete_user_schema
from app.models.user import User
from app.models.log_event import LogEvent
from app.models.stats import UserStats
from app.utils.constants.enum_class import modelBool, UserAccessLevel, UserFlag
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
@admin.route("/restricted_area/users", methods=["POST"])
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
                "items_per_page": 25,
                "order_sort": "descending",
                "ordered_by": "_last_seen",
                "page_nr": 1,
                "search_by": "email",
                "search_word": "frank",
            },
            "users": [
                {
                "email": "frank.torres@fakemail.com",
                "is_blocked": "false",
                "last_seen": "Thu, 25 Jan 2024 00:00:00 GMT",
                "name": "Frank Torres",
                "uuid": "3f61108854cd4b5886401080d681dd96"
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

    # Dynamic filtering conditions - possible values for (filter_by, search_by)
    filter_conditions = {
        ("none","none"): User.query.order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False),
        ("none", "email"): User.query.filter(User.email.ilike(f"%{search_word}%")).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False),
        ("none","name",): User.query.filter(User.name.ilike(f"%{search_word}%")).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False),
        ("is_blocked","none"): User.query.filter_by(is_blocked=modelBool.TRUE).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False),
        ("is_blocked", "email"): User.query.filter(User.is_blocked == modelBool.TRUE, User.email.ilike(f"%{search_word}%")).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False),
        ("is_blocked", "name"): User.query.filter(User.is_blocked == modelBool.TRUE, User.name.ilike(f"%{search_word}%")).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False),
    }

    try:
        users = filter_conditions.get((filter_by, search_by), ("none","none"))
    except Exception as e:
        logging.error(f"User table could not be retrieved. Error: {e}")

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
                "search_by": search_by,
                "search_word": search_word,
            }
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

    # Get Uuuid and block status from JSON payload
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
            # Admin user should not be deleted
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
    
