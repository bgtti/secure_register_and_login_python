# Python and Flask
from flask import Blueprint, request, jsonify
from datetime import datetime, timezone, timedelta
import logging

# Extensions
from app.extensions.extensions import limiter
from flask_login import (
    current_user,
    login_required,
)

# DB Models
from app.models.user import User
from app.models.role import Role
from app.models.log_activity import LogActivity
# from app.models.log_event import LogEvent
from app.models.message import Message

# Constants
from app.constants.flags import Flag
# from app.common.constants.enum_class import modelBool, UserAccessLevel, UserFlag
# from app.common.constants.enum_helpers import map_string_to_enum

# Common Utils
from app.common.enum_helpers.map_string_to_enum import map_string_to_enum
from app.common.detect_html.detect_html import check_for_html
from app.common.custom_decorators.admin_protected_route import admin_only
from app.common.custom_decorators.json_schema_validator import validate_schema

# Services
from app.services.admin.users_table_service import svc_get_users_table
from app.services.user.user_service import svc_get_user_by_id, svc_serialize_user_table
from app.services.logging.security_log_services import svc_user_security_log_table
from app.services.logging.activity_log_services import svc_user_activity_log_table
from Backend.app.services.message.search_service import svc_search_user_message_threads

# Json Schema
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
    order_by = json_data.get("order_by", "last_seen") # ["last_seen", "name", "email", "created_at"]
    order_sort = json_data.get("order_sort", "descending")
    filter_by = json_data.get("filter_by", "none")
    filter_by_flag = json_data.get("filter_by_flag", "blue")
    filter_by_last_seen = json_data.get("filter_by_last_seen", "") 
    search_by = json_data.get("search_by", "none")
    search_word = json_data.get("search_word", "")

    table_res = svc_get_users_table(
        page_nr=page_nr,
        items_per_page=items_per_page,
        order_by=order_by,
        order_sort=order_sort,
        filter_by=filter_by,
        filter_by_flag=filter_by_flag,
        filter_by_last_seen=filter_by_last_seen,
        search_by=search_by,
        search_word=search_word,
    )

    # prepare response
    res_data ={
            "response":"success",
            "users": [],
            "total_pages": 1,
            "current_page": 1,
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
    
    if table_res is not None:
        res_data["users"] = table_res["users"]
        res_data["total_pages"] = table_res["total_pages"]
        res_data["current_page"] = table_res["current_page"]

    
    return jsonify(res_data), 200

    # # Check if search is valid
    # if not search_word:
    #     search_by = "none"
    # else:
    #     search_word = search_word.strip()
    #     # Check for html in user input
    #     html_in_input = check_for_html(search_word, "admin_users_table - search_word field")
    #     if html_in_input:
    #         logging.warning(f"Admin input may include html. Possible vulnerability? Input in user search: {search_word}")#TODO: sanitize???

    # # Determine the ordering based on order_by input
    # ordering = User.__dict__.get(order_by, None) 
    # if ordering is None:
    #     return jsonify({"response": "Invalid order_by field."}), 400

    # if order_sort == "descending":
    #     ordering = ordering.desc()
    # else:
    #     ordering = ordering.asc()
    
    # # Base query: exclude super admins before filtering/pagination TODO: really necessary????
    # query = User.query.join(Role).filter(
    #     Role.access_level != "super_admin"
    # )

    # # Filtering
    # if filter_by != "none":

    #     flag_enum = map_string_to_enum(filter_by_flag, Flag)

    #     filter_conditions_map = {
    #         "is_blocked": User.is_blocked.is_(True), #User.is_blocked == True,
    #         "is_unblocked": User.is_blocked.is_(False), #User.is_blocked == False,
    #         "flag": User.flagged == flag_enum, # User.flagged == map_string_to_enum(filter_by_flag, UserFlag),
    #         "flag_not_blue": User.flagged != UserFlag.BLUE, 
    #         "is_admin": Role.access_level == "admin", #User.access_level == UserAccessLevel.ADMIN,#TODO fix new logic
    #         "is_user": Role.access_level == "user", #User.access_level == UserAccessLevel.USER,#TODO fix new logic
    #         "last_seen": User.last_seen >= filter_by_last_seen if filter_by_last_seen != "" else User.last_seen >= (datetime.now(timezone.utc) - timedelta(30)),
    #     }

    # if search_by != "none":
    #     search_conditions_map = {
    #         "name":User.name.ilike(f"%{search_word}%"),
    #         "email": User.email.ilike(f"%{search_word}%")
    #     }
        
    # filter_case = (filter_by == "none", search_by == "none")

    # match filter_case:
    #     case (True, True):
    #         users = User.query.order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False)
    #     case (True, False):
    #         users = User.query.filter(search_conditions_map[search_by]).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False)
    #     case (False, True):
    #         users = User.query.filter(filter_conditions_map[filter_by]).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False)
    #     case (False, False):
    #         users = User.query.filter(filter_conditions_map[filter_by], search_conditions_map[search_by]).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False)
    #     case _:
    #         logging.error(f"User table could not be retrieved as criteria was not met.")
    #         return jsonify({"response": "Could not match search criteria"}), 404

    # if not users.items:
    #     return jsonify({"response": "Requested page out of range"}), 404
    
    
    # response_data ={
    #         "response":"success",
    #         "users": [user.serialize_user_table() for user in users.items if user.access_level != UserAccessLevel.SUPER_ADMIN],
    #         "total_pages": users.pages,
    #         "current_page": users.page,
    #         "query":{
    #             "page_nr": page_nr,
    #             "items_per_page": items_per_page,
    #             "ordered_by": order_by,
    #             "order_sort": order_sort,
    #             "filter_by": filter_by,
    #             "filter_by_flag": filter_by_flag,
    #             "filter_by_last_seen": filter_by_last_seen,
    #             "search_by": search_by,
    #             "search_word": search_word,
    #         }
    #     }
    
    # return jsonify(response_data)

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

    # Get user
    user = svc_get_user_by_id(user_id)

    if not user:
        return jsonify({"response": "Error prevented user from being queried."}), 500
    
    user_dict = svc_serialize_user_table(user)

    response_data ={
            "response":"success",
            "user": user_dict,
        }
    
    return jsonify(response_data), 200

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

    Returns a JSON object with a "response" field. Logs and other information only sent if response is 200.
    ----------------------------------------------------------
    Request example:
    json_payload = {
        "user_id": 12345,
        "log_type": "both",
        "page_nr": 1,
        "items_per_page": 25
    }
    ----------------------------------------------------------
    Response examples:

    {"response": "Requested page out of range"}

    {"response":"success",
            "security_logs": {
                "total_pages": 2,
                "current_page": 1,
                "logs": [{
                    "id": 10,
                    "created_at": "Thu, 25 Jan 2024 00:00:00 GMT",
                    "message": "Successful login.",
                    "level": "INFO",
                    "level_id": 10,
                    "event": "login",
                    "activity": "login",
                    "ip_address": "192.168.1.1",
                    "geo_location": "USA, New York",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    },
                    #...
                ]
            },
            "activity_logs": {
                "total_pages": 2,
                "current_page": 1,
                "logs": [{
                    "id": 10,
                    "created_at": "Thu, 25 Jan 2024 00:00:00 GMT",
                    "message": "Successful login.",
                    "level": "INFO",
                    "level_id": 10,
                    "event": "login",
                    "activity": "login",
                    "ip_address": "192.168.1.o",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    },
                    #...
                ]
            }
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
    log_type = json_data["log_type"] # one of ["security", "activity", "both"]
    page_nr = json_data.get("page_nr", 1)
    items_per_page = json_data.get("items_per_page", 25)

    if log_type == "both":
        page_nr = 1
        items_per_page = 25
    
    # Log request
    logging.info(f"Admin {current_user.id} requested {log_type} logs for user {user_id}.")

    # prepare success response
    res_data ={
            "response":"success",
            "security_logs": [],
            "activity_logs": [],
            "query":{
                "page_nr": page_nr,
                "items_per_page": items_per_page,
                "ordered_by": "created_at",
                "order_sort": "descending",
            }
        }

    if log_type == "both" or log_type == "security":
        sec_logs_data = svc_user_security_log_table(user_id, page_nr, items_per_page, True)
        res_data["security_logs"] = sec_logs_data if sec_logs_data else None
    
    if log_type == "both" or log_type == "activity":
        act_logs_data = svc_user_activity_log_table(user_id, page_nr, items_per_page, True)
        res_data["activity_logs"] = act_logs_data if act_logs_data else None
    
    if not res_data["security_logs"] and not res_data["activity_logs"]:
        return jsonify({"response": "Requested page out of range"}), 404
    
    return jsonify(res_data), 200

# ----- USER MESSAGES -----
@users.route("/user_messages", methods=["POST"])
@login_required
@admin_only
@validate_schema(admin_user_messages_schema)
def admin_user_messages():
    """
    admin_user_messages() -> JsonType
    ----------------------------------------------------------
    Route to get a user's message threads sent to the site.
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

    {"response":"success",
            "message_threads": [
                {
                "id": 10,
                "reference": "REF-A7X92Q98",
                "created_at": "Thu, 25 Jan 2024 00:00:00 GMT",
                "last_message_at": "Thu, 25 Jan 2024 00:00:00 GMT",
                "subject": "Problems logging into account.",
                "status": "new",
                "priority": "normal", 
                "flagged": "blue", 
                "is_spam": False, 
                "is_deleted": False, 
                "deleted_at": None, 
                "purge_date": "Fri, 25 Jan 2025 00:00:00 GMT", 
                "originator_id": 105, 
                "originator_email": "john@example.com", 
                "originator_name": "John", 
                "assigned_to_admin_id": None, 
                }, 
                #...
            ]
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

    # Get message threads
    thread_data = svc_search_user_message_threads(
    user_id=user_id,
    page_nr=page_nr,
    items_per_page=25,
    marked_spam=False,
    marked_deleted=False,
    internal_use=True,
    )

    # Prepare response
    res_data ={
            "response":"success",
            "message_threads": [],
            "total_pages": 1,
            "current_page": 1,
            "query":{
                "page_nr": page_nr,
                "items_per_page": 25,
                "ordered_by": "date", #last_message_at
                "order_sort": "descending",
            }
        }

    if thread_data:
        res_data["message_threads"] = thread_data["threads"]
        res_data["total_pages"] = thread_data["total_pages"]
        res_data["current_page"] = thread_data["current_page"]
    
    # Log request
    logging.info(f"Admin {current_user.id} requested message threads for user {user_id}.")
    
    return jsonify(res_data), 200