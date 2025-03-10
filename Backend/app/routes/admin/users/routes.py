from flask import Blueprint, request, jsonify
from datetime import datetime, timezone, timedelta
from flask_login import login_required
import logging
from app.extensions.extensions import limiter
from app.models.user import User
from app.models.log_activity import LogActivity
# from app.models.log_event import LogEvent
from app.models.message import Message
from app.utils.constants.enum_class import modelBool, UserAccessLevel, UserFlag
from app.utils.constants.enum_helpers import map_string_to_enum
from app.utils.detect_html.detect_html import check_for_html
from app.utils.custom_decorators.admin_protected_route import admin_only
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.routes.admin.users.schemas import admin_users_table_schema, admin_user_information, admin_user_logs_schema, admin_user_messages_schema



# Blueprint
from . import users

# In this file: routes that provide user-related information (to be accessed by admin users only) 
#   - table with all users, 
#   - a particular user's information, 
#   - a particular user's logs, 
#   - a particular user's messages 

# View functions in this file provide but do not modify information in the db


# ----- USERS TABLE -----
@users.route("/table", methods=["POST"])
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

# ----- USER INFO -----
@users.route("/user_info", methods=["POST"])
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

# ----- USER LOGS -----
@users.route("/user_logs", methods=["POST"])
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
        user_logs = LogActivity.query.filter_by(user_id=user_id).order_by(LogActivity.created_at.desc()).paginate(page=page_nr, per_page=25, error_out=False)
        # user_logs = LogEvent.query.filter_by(user_id=user_id).order_by(LogEvent.created_at.desc()).paginate(page=page_nr, per_page=25, error_out=False)
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

# ----- USER MESSAGES -----
@users.route("/user_messages", methods=["POST"])
@login_required
@admin_only
@validate_schema(admin_user_messages_schema)
def admin_user_messages():
    """
    admin_user_messages() -> JsonType
    ----------------------------------------------------------
    Route to get a user's messages sent to the site.
    Takes a JSON payload with the following parameters:
    - "user_id": User's id to be queried.
    - "page_nr": int used for pagination.

    Returns a JSON object with a "response" field. messages and other information only sent if response is 200.
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
            "messages": {
                "id": 3,
                "date": "Thu, 25 Jan 2024 00:00:00 GMT",
                "sender_name": "John",
                "sender_email": "john@example.com",
                "message": "Hi, I have a problem logging in.",
                "flagged": "blue",
                "answer_needed": true,
                "was_answered": false,
                "answered_by": "",
                "answer_date": "",
                "answer": ""
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
        user_messages = Message.query.filter_by(user_id=user_id).order_by(Message.date.desc()).paginate(page=page_nr, per_page=25, error_out=False)
        if not user_messages.items:
            return jsonify({"response": "Requested page out of range"}), 404
    except Exception as e:
        logging.error(f"Error prevented Message to be queried: {e}")
        return jsonify({"response": "Error prevented messages from being queried"}), 500
    
    response_data ={
            "response":"success",
            "messages": [message.serialize_message_table() for message in user_messages.items],
            "total_pages": user_messages.pages,
            "current_page": user_messages.page,
            "query":{
                "page_nr": page_nr,
                "items_per_page": 25,
                "ordered_by": "date",
                "order_sort": "descending",
            }
        }
    
    print(response_data)
    
    return jsonify(response_data)