"""
**ABOUT THIS FILE**

auth/profile/routes.py contains routes responsible for profile management functionalities.

Here you will find the following routes:
- **change_user_name** route changes the user's name in the db

The format of data sent by the client is validated using Json Schema. 
Reoutes receiving client data are decorated with `@validate_schema(name_of_schema)` for this purpose. 

------------------------
## More information

In this simple app template, the Name feature functions more as a profile attribute than a core authentication feature. However, since users could potentially set their name to impersonate an administrator or another role, it has been placed in the auth section to maintain control and prevent misuse.
"""
############# IMPORTS ##############

# Python/Flask libraries
import logging
from flask import request, jsonify
from flask_login import (
    current_user,
    login_required,
)

# Extensions
from app.extensions.extensions import db, limiter

# Database models
from app.models.user import User

# Utilities
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.utils.detect_html.detect_html import check_for_html
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.profanity_check.profanity_check import has_profanity

# Auth helpers
from app.routes.auth.helpers_auth import user_name_is_valid

# Profile helpers
from app.routes.auth.profile.log import log_change_name

from app.routes.auth.profile.schemas import (
    change_name_schema
)

# Blueprint
from . import profile


############# ROUTES ###############


####################################
#         CHANGE USER'S NAME       #
####################################

@profile.route("/change_user_name", methods=["POST"])
@login_required
@validate_schema(change_name_schema)
@limiter.limit("10/day")
def change_user_name(): # TODO --> Add to logs so user actions can show in history
    """
    change_user_name() -> JsonType
    ----------------------------------------------------------

    Route changes the name associated with the user's account. 
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "user" value only included if response is "success".

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "user": {
                    "name": "John", 
                    "email": "john@email.com",
                    "access": "user",
                    "email_is_verified": True
                    }, 
            }
    ``` 
    """
    # Standard error response
    error_response = {"response": "There was an error changing user's name."}

    # Get the JSON data from the request body
    json_data = request.get_json()
    new_name = json_data["new_name"]
    user_agent = json_data.get("user_agent", "")

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Get the user from cookie 
    try:
        user = User.query.filter_by(email=current_user.email).first()
    except Exception as e:
        log_message = f"Failed to retrieve user from database. Error: {str(e)}"
        logging.error(log_message)
        log_change_name(500, log_message, user_agent, client_ip, 0)
        return jsonify(error_response), 500

    if user is None:
        log_change_name(500, "Session did not return current user.", user_agent, client_ip, 0)
        return jsonify({"response": "Error: user not found."}), 500 #500 instead of 401 because @login_required so current_user should exist

    new_name_is_valid = user_name_is_valid(new_name)

    if not new_name_is_valid:
        log_change_name(400, f"New name is not valid. New name: {new_name}", user_agent, client_ip, user.id)
        return jsonify(error_response), 400

    # the_user = User.query.filter_by(email=current_user.email).first()
    old_name = user.name

    try:
        user.name = new_name
        db.session.commit()
        log_message = f"User {current_user.email} name changed from {old_name} to {new_name}."
        logging.info(log_message)
        log_change_name(200, log_message, user_agent, client_ip, user.id)
        
    except Exception as e:
        db.session.rollback()
        log_message = f"User could not change name. Error: {str(e)}"
        logging.error(log_message)
        log_change_name(500, log_message, user_agent, client_ip, user.id)
        return jsonify(error_response), 500

    flag = False

    html_in_name = check_for_html(new_name, "auth - change_user_name", current_user.email)
    if html_in_name:
        flag = "YELLOW"
        user.flag_change(flag)
    else:
        profanity_in_name = has_profanity(new_name) 
        if profanity_in_name:
            flag = "PURPLE"
            user.flag_change(flag)
    
    if flag:
            user.flag_change(flag)
            db.session.commit()
            log_change_name(207, f"New name: {new_name}.", user_agent, client_ip, user.id)

    response_data ={
            "response":"success",
            "user": {
                "access": user.access_level.value, 
                "name": user.name, 
                "email": user.email,
                "email_is_verified": user.email_is_verified.value
                },
        }
    return jsonify(response_data)
