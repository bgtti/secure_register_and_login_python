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
from app.utils.profanity_check.profanity_check import has_profanity

# Auth helpers
from app.routes.auth.helpers_auth import user_name_is_valid

# Profile helpers
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
    #TODO: get the user_agent from json to log

    new_name_is_valid = user_name_is_valid(new_name)

    if not new_name_is_valid:
        return jsonify(error_response), 400

    the_user = User.query.filter_by(email=current_user.email).first()
    old_name = the_user.name

    try:
        the_user.name = new_name
        db.session.commit()
        logging.info(f"User {current_user.email} name changed from {old_name} to {new_name}.")
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"User could not change name. Error: {e}")
        return jsonify(error_response), 500

    flag = False

    html_in_name = check_for_html(new_name, "auth - change_user_name", current_user.email)
    if html_in_name:
        flag = "YELLOW"
        the_user.flag_change(flag)
    else:
        profanity_in_name = has_profanity(new_name) 
        if profanity_in_name:
            flag = "PURPLE"
            the_user.flag_change(flag)
    
    if flag:
            the_user.flag_change(flag)
            db.session.commit()

    response_data ={
            "response":"success",
            "user": {
                "access": the_user.access_level.value, 
                "name": the_user.name, 
                "email": the_user.email,
                "email_is_verified": the_user.email_is_verified.value
                },
        }
    return jsonify(response_data)
