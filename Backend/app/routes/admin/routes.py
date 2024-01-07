from flask import Blueprint, request, jsonify, session
import logging
import jsonschema
from sqlalchemy import desc, asc
from sqlalchemy_utils import escape_like
from app.extensions import flask_bcrypt, db
from app.routes.account.schemas import sign_up_schema, log_in_schema
from app.routes.admin.schemas import admin_users_table_schema
# from app.account.salt import generate_salt
from app.models.user import User
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper
from app.utils.detect_html.detect_html import check_for_html


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


