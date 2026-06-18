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
from app.common.custom_decorators.json_schema_validator import validate_schema
from app.common.detect_html.detect_html import check_for_html
from app.common.ip_utils.ip_address_validation import get_client_ip
from app.common.profanity_check.profanity_check import has_profanity

# Services
from app.services.auth.user_profile_service import svc_change_user_name
from app.services.user.user_service import svc_get_user_or_none

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
def change_user_name(): 
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
    
    # Get the JSON data from the request body
    json_data = request.get_json()
    new_name = json_data["new_name"]
    user_agent = json_data.get("user_agent", "")

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # Error messages
    error_400 = {"response": "Error: name could not be changed."}
    error_440 = {"response": "Session expired. Please log in again."}
    error_500 = {"response": "System error: could not change name."}


    # Check if user exists
    user = svc_get_user_or_none(current_user.email, "change_user_name")

    if user is None:
        log_change_name(440, "Session did not return current user.", user_agent, client_ip, 0)
        return jsonify(error_440), 440 
    
    change_name_res = svc_change_user_name(user, new_name)

    log_change_name(change_name_res["log_code"], change_name_res["log_text"], user_agent, client_ip, user.id)

    if not change_name_res["success"]:
        if change_name_res["log_code"] == 500:
            return jsonify(error_500), 500
        else:
            return jsonify(error_400), 400

    response_data ={
            "response":"success",
            "user": {
                "access": user.role.access_level, 
                "name": user.name, 
                "email": user.email,
                "email_is_verified": user.email_is_verified
                },
        }
    return jsonify(response_data)
