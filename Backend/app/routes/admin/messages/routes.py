from flask import Blueprint, request, jsonify
from datetime import datetime, timezone, timedelta
from flask_login import login_required
from app.extensions.extensions import limiter
import logging
from app.models.user import User
# from app.models.log_event import LogEvent
from app.models.message import Message
from app.utils.constants.enum_class import modelBool, UserAccessLevel, UserFlag
from app.utils.constants.enum_helpers import map_string_to_enum
from app.utils.detect_html.detect_html import check_for_html
from app.utils.custom_decorators.admin_protected_route import admin_only
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.routes.admin.messages.schemas import admin_messages_table_schema



# Blueprint
from . import messages

# In this file: routes that provide message-related information (to be accessed by admin users only) 
#   - table with all messages, 
#   - message actions

# View functions in this file provide and/or modify information in the db

# ----- MESSAGES TABLE -----
@messages.route("/table", methods=["POST"])
@login_required
@admin_only
@validate_schema(admin_messages_table_schema)
def admin_messages_table():
    """
    admin_messages_table() -> JsonType
    ----------------------------------------------------------
    Route to get a table of messages sent to the site.
    Takes a JSON payload with the following required parameters:
    - "items_per_page": int greater than 0, smaller than or equal to 50, multiple of 5.
    - "page_nr": int used for pagination.
    Optional parameters:
    - "filter_by": one of ["answer_needed", "answer_not_needed", "all"]
    - "order_sort": one of ["order_sort", "descending"]
    - "include_spam": boolean

    Returns a JSON object with a "response" field. messages and other information only sent if response is 200.
    ----------------------------------------------------------
    Request example:
    json_payload = {
        "page_nr": 1,
        "items_per_page": 25,
        "filter_by": "answer_needed",
        "order_sort": "descending",
        "include_spam": false
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
                "sender_is_user": true,
                "subject": "Login issue",
                "message": "Hi, I have a problem logging in.",
                "flagged": "blue",
                "is_spam": false,
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
                "filter_by": "answer_needed",
                "order_sort": "descending",
                "include_spam": "false",
            }
    }
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get info from JSON payload
    page_nr = json_data["page_nr"] # > 0
    items_per_page = json_data["items_per_page"] # >= 5 and <=50, multiple of 5
    order_sort = json_data["order_sort"] # one of: ["descending", "ascending"]
    filter_by = json_data["filter_by"] # one of: ["answer_needed", "answer_not_needed", "all"]
    include_spam = json_data["include_spam"] # boolean

    # Determine the ordering based on user input
    ordering = Message.__dict__.get("date", None)

    if order_sort == "descending":
        ordering = ordering.desc()
    else:
        ordering = ordering.asc()

    if include_spam:
        spam_included = modelBool.TRUE
    else:
        spam_included = modelBool.FALSE

    match filter_by:
        case "all":
            messages = Message.query.filter_by(is_spam=spam_included).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False)
        case "answer_needed":
            messages = Message.query.filter(Message.is_spam == spam_included, Message.answer_needed == modelBool.TRUE).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False)
        case "answer_not_needed":
            messages = Message.query.filter(Message.is_spam == spam_included, Message.answer_needed == modelBool.FALSE).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False)
        case _:
            logging.error(f"Message table could not be retrieved as criteria was not met.")
            return jsonify({"response": "Could not match search criteria"}), 404
        
    
        
    if not messages.items:
        return jsonify({"response": "Requested page out of range"}), 404
    
    response_data ={
            "response":"success",
            "messages": [message.serialize_message_table() for message in messages.items],
            "total_pages": messages.pages,
            "current_page": messages.page,
            "query":{
                "page_nr": page_nr,
                "items_per_page": items_per_page,
                "order_sort": order_sort,
                "filter_by": filter_by,
                "include_spam": include_spam,
            }
        }
    
    return jsonify(response_data)