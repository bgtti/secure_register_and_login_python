from flask import Blueprint, request, jsonify, session
import logging
import jsonschema
from sqlalchemy import desc, asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import escape_like
from app.extensions import flask_bcrypt, db
from app.routes.account.schemas import sign_up_schema, log_in_schema
from app.routes.admin.schemas import admin_users_table_schema, admin_user_logs_schema, admin_block_and_unblock_user_schema, admin_delete_user_schema
# from app.account.salt import generate_salt
from app.models.user import User
from app.models.log_event import LogEvent
from app.models.stats import UserStats
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper
from app.utils.detect_html.detect_html import check_for_html
from app.utils.log_event_utils.log import log_event


admin = Blueprint('admin', __name__)

# In this file: routes concerning admin 

# SIGN In
@admin.route("/restricted_login", methods=["POST"])
def admin_login():
    """
    login_user() -> JsonType
    ----------------------------------------------------------
    Route with no parameters.
    Sets a session cookie in response.
    Returns Json object containing strings.
    "response" value is always included.  
    "user" value only included if response is "success".
    ----------------------------------------------------------
    Response example:
    response_data = {
            "response":"success",
            "user": {
                "id": "16fd2706-8baf-433b-82eb-8c7fada847da", 
                "name": "John", 
                "email": "john@email.com"}, 
        } 
    """
    
    return jsonify({'response': 'You logged in!'})

# DASHBOARD
@admin.route("/restricted_area/dashboard", methods=["POST"])
def admin_dashboard():

    # users = User.query.order_by(_email=email).first()
    
    return jsonify({'response': 'You logged in!'})

# USERS TABLE ----------- SET COOKIE
@admin.route("/restricted_area/users", methods=["POST"])
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

    # validate Json against the schema
    try:
        jsonschema.validate(instance=json_data, schema=admin_users_table_schema)
    except jsonschema.exceptions.ValidationError as e:
        logging.info(f"Jsonschema validation error. Input page_nr: {json_data["page_nr"]}, items_per_page: {json_data["items_per_page"]}, order_by: {json_data["order_by"]}, order_sort: {json_data["order_sort"]}, filter_by: {json_data["filter_by"]}, search_by: {json_data["search_by"]}, search_word: {json_data["search_word"]}")
        return jsonify({"response": "Invalid JSON data.", "error": str(e)}), 400
    
    # setting defaults to optional arguments:
    page_nr = json_data["page_nr"]
    items_per_page = json_data.get("items_per_page", 25)
    order_by = json_data.get("order_by", "last_seen")
    order_sort = json_data.get("order_sort", "descending")
    filter_by = json_data.get("filter_by", "none")
    search_by = json_data.get("search_by", "none")
    search_word = json_data.get("search_word", "")

    order_by = "_" + order_by

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
        ("none", "email"): User.query.filter(User._email.ilike(f"%{search_word}%")).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False),
        ("none","name",): User.query.filter(User._name.ilike(f"%{search_word}%")).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False),
        ("is_blocked","none"): User.query.filter_by(_is_blocked="true").order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False),
        ("is_blocked", "email"): User.query.filter(User._is_blocked == "true", User._email.ilike(f"%{search_word}%")).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False),
        ("is_blocked", "name"): User.query.filter(User._is_blocked == "true", User._name.ilike(f"%{search_word}%")).order_by(ordering).paginate(page=page_nr, per_page=items_per_page, error_out=False),
    }

    try:
        users = filter_conditions.get((filter_by, search_by), ("none","none"))
    except Exception as e:
        logging.error(f"User table could not be retrieved. Error: {e}")

    if not users.items:
        return jsonify({"response": "Requested page out of range"}), 404
    
    response_data ={
            "response":"success",
            "users": [user.serialize_user_table() for user in users.items],
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


# USERS TABLE LOGS ----------- SET COOKIE 
@admin.route("/restricted_area/users/user_logs", methods=["POST"])
def admin_user_logs():
    """
    admin_user_logs() -> JsonType
    ----------------------------------------------------------
    Route to get a user's logs.
    Takes a JSON payload with the following parameters:
    - "user_uuid": User's uuid to be queried.
    - "page_nr": int used for pagination.

    Returns a JSON object with a "response" field. Logs and other information only sent if response is 200.
    ----------------------------------------------------------
    Request example:
    json_payload = {
        "user_uuid": "3f61108854cd4b5886401080d681dd96",
        "page_nr": 1
    }
    ----------------------------------------------------------
    Response examples:

    {"response": "Requested page out of range"}

    {"response":"success",
            "logs": {
                "user_uuid": "3f61108854cd4b5886401080d681dd96",
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

    # validate Json against the schema
    try:
        jsonschema.validate(instance=json_data, schema=admin_user_logs_schema)
    except jsonschema.exceptions.ValidationError as e:
        logging.info(f"Jsonschema validation error. Input uuid: {json_data["user_uuid"]}")
        return jsonify({"response": "Invalid JSON data.", "error": str(e)}), 400

    # Get info from JSON payload
    user_uuid = json_data["user_uuid"]
    page_nr = json_data["page_nr"]

    try:
        user_logs = LogEvent.query.filter_by(_user_uuid=user_uuid).order_by(LogEvent._created_at.desc()).paginate(page=page_nr, per_page=25, error_out=False)
        if not user_logs.items:
            return jsonify({"response": "Requested page out of range"}), 404
        # print(user_logs)
        # random_log = db.session.query(LogEvent).get(1)
        # print(random_log.user_uuid)
    except Exception as e:
        # Handle other exceptions
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
    # return jsonify({"success":"200"})


# USERS TABLE BLOCK/UNBLOCK ----------- SET COOKIE
@admin.route("/restricted_area/users/block_unblock", methods=["POST"])
def block_unblock_user():
    """
    block_unblock_user() -> JsonType
    ----------------------------------------------------------
    Route to block or unblock a user by UUID.
    Takes a JSON payload with the following parameters:
    - "user_uuid": Uuid of the user to block/unblock.
    - "block": Set to true if the user should be blocked, false to unblock.

    Returns a JSON object with a "response" field:
    - If blocking/unblocking is successful: {"response": "success"}
    - If the UUID is not found: {"response": "User not found"}
    - If an error occurs during the operation: {"response": "Error blocking/unblocking user", "error": "Details of the error"}

    ----------------------------------------------------------
    Request example:
    json_payload = {
        "user_uuid": "3f61108854cd4b5886401080d681dd96",
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

    # Validate Json against the schema
    try:
        jsonschema.validate(instance=json_data, schema=admin_block_and_unblock_user_schema)
    except jsonschema.exceptions.ValidationError as e:
        logging.info(f"Jsonschema validation error. Input uuid: {json_data["user_uuid"]}. Input clock: {json_data["block"]}.")
        return jsonify({"response": "Invalid JSON data.", "error": str(e)}), 400

    # Get Uuuid and block status from JSON payload
    user_uuid = json_data["user_uuid"]
    block_status = json_data["block"]

    try:
        user = User.query.filter_by(_uuid=user_uuid).first()

        if user:

            if block_status:
                user.block_access()
                log_event("LOG_EVENT_BLOCK","LEB_01",user_uuid)
            else:
                user.unblock_access()
                log_event("LOG_EVENT_UNBLOCK","LEU_01",user_uuid)

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
            log_event("LOG_EVENT_BLOCK","LEB_02",user_uuid)
        else:
            log_event("LOG_EVENT_UNBLOCK","LEU_02",user_uuid)
        return jsonify({"response": "Error deleting user", "error": str(e)}), 500
    
    except Exception as e:
        logging.error(f"Error prevented user block/unblock: {e}")
        if block_status:
            log_event("LOG_EVENT_BLOCK","LEB_02",user_uuid)
        else:
            log_event("LOG_EVENT_UNBLOCK","LEU_02",user_uuid)
        return jsonify({"response": "Error blocking/unblocking user", "error": str(e)}), 500
    

# USERS TABLE DELETE ----------- SET COOKIE 
@admin.route("/restricted_area/users/delete", methods=["POST"])
def admin_delete_user():
    """
    admin_delete_user() -> JsonType
    ----------------------------------------------------------
    Route to delete a user by UUID.
    Takes a JSON payload with the following parameters:
    - "user_uuid": User's UUID to be deleted.

    Returns a JSON object with a "response" field:
    - If deletion is successful: {"response": "success"}
    - If the UUID is not found: {"response": "User not found"}
    - If an error occurs during deletion: {"response": "Error deleting user", "error": "Details of the error"}

    ----------------------------------------------------------
    Request example:
    json_payload = {
        "uuid": "3f61108854cd4b5886401080d681dd96"
    }
    ----------------------------------------------------------
    Response examples:
    {"response": "success"}
    {"response": "User not found"}
    {"response": "Error deleting user", "error": "Details of the error"}
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # validate Json against the schema
    try:
        jsonschema.validate(instance=json_data, schema=admin_delete_user_schema)
    except jsonschema.exceptions.ValidationError as e:
        logging.info(f"Jsonschema validation error. Input uuid: {json_data["user_uuid"]}")
        return jsonify({"response": "Invalid JSON data.", "error": str(e)}), 400

    # Get UUID from JSON payload
    user_uuid = json_data["user_uuid"]

    try:
        user = User.query.filter_by(_uuid=user_uuid).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            logging.info("User deleted successfully by admin.")
            log_event("LOG_EVENT_DELETE_USER","LEDU_01",user_uuid)

            try:
                new_user_stats = UserStats(new_user=-1,country="")
                db.session.add(new_user_stats)
                db.session.commit()
            except Exception as e:
                logging.error(f"Admin deleted user but error prevented UserStats entry: {e}")

            # returns success even if stats could not be registered
            return jsonify({"response": "success"})
        else:
            # User not found
            return jsonify({"response": "User not found"}), 404

    except IntegrityError as e:
        # Handle database integrity error (e.g., foreign key constraint)
        db.session.rollback()
        logging.error(f"DB integrity error prevented user deletion: {e}")
        log_event("LOG_EVENT_DELETE_USER","LEDU_02",user_uuid)
        return jsonify({"response": "Error deleting user", "error": str(e)}), 500

    except Exception as e:
        # Handle other exceptions
        logging.error(f"Error prevented user deletion: {e}")
        log_event("LOG_EVENT_DELETE_USER","LEDU_02",user_uuid)
        return jsonify({"response": "Error deleting user", "error": str(e)}), 500
    
