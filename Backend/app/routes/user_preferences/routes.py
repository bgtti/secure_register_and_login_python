"""
**ABOUT THIS FILE**

user_settings/routes.py contains routes responsible for non-auth related user setting functionalities.

Here you will find the following routes:
- **set_mailing_list** route changes the user's mailing list preferences in the db
- **set_night_mode** route changes the user's night mode preferences in the db

The format of data sent by the client is validated using Json Schema. 
Reoutes receiving client data are decorated with `@validate_schema(name_of_schema)` for this purpose. 

------------------------
## More information

In this simple app template, the Name feature functions more as a profile attribute than a core authentication feature. However, since users could potentially set their name to impersonate an administrator or another role, it has been placed in the auth section to maintain control and prevent misuse.
"""
############# IMPORTS ##############

# Python/Flask libraries
import logging
from flask import Blueprint, request, jsonify, session
from flask_login import (
    current_user,
    login_required,
)

# Extensions
from app.extensions.extensions import db, limiter

# Database models
from app.models.user import User

# Services
from app.services.user.user_service import svc_get_user_or_none
from app.services.user.user_preference_service import svc_set_mailing_list, svc_set_night_mode

# Utilities
from app.common.custom_decorators.json_schema_validator import validate_schema
from app.common.ip_utils.ip_address_validation import get_client_ip

# Logging
from app.routes.user_preferences.log import log_set_mailing_list, log_set_night_mode

# Json Schemas
from app.routes.user_preferences.schemas import (
    set_mailing_list_schema,
    set_night_mode_schema
)

# Blueprint
user_preferences = Blueprint("user_preferences", __name__)


############# ROUTES ###############


####################################
#    SET MAILING LIST PREFERENCE   #
####################################

@user_preferences.route("/set_mailing_list", methods=["POST"])
@login_required
@validate_schema(set_mailing_list_schema)
@limiter.limit("2/minute;10/day")
def set_mailing_list():
    """
    set_mailing_list() -> JsonType
    ----------------------------------------------------------

    Route sets whether user would like or not to be in the app's mailing list. 
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "in_mailing_list" value only included if response is successful.

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"Mailing list set successfully!",
                "in_mailing_list": True # or False
            }
    ``` 
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    join_mailing_list = json_data["mailing_list"]
    user_agent = json_data.get("user_agent", "")

    # Get the request ip
    client_ip = get_client_ip(request) or ""
    
    # Set mailing list preferences
    pref_ok = svc_set_mailing_list(current_user, join_mailing_list)

    if not pref_ok:
        log_set_mailing_list(500, "System error prevented preference change", user_agent, client_ip, current_user.id)
        return jsonify({"response": "An error occurred: please try again later."}), 500
    
    log_set_mailing_list(200, f"User in mailing list set to {join_mailing_list}.", user_agent, client_ip, current_user.id)
    
    response_data ={
            "response":"Mailing list set successfully!",
            "in_mailing_list": current_user.in_mailing_list
        }
    return jsonify(response_data), 200

####################################
#     SET NIGHT MODE PREFERENCE    #
####################################

@user_preferences.route("/set_night_mode", methods=["POST"])
@login_required
@validate_schema(set_night_mode_schema)
@limiter.limit("2/minute;10/day")
def set_night_mode():
    """
    set_night_mode() -> JsonType
    ----------------------------------------------------------

    Route defines whether user prefers night nightmode enabled or not. 
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "night_mode_enabled" value only included if response is successful.

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"Night mode set successfully!",
                "night_mode_enabled": True # or False
            }
    ``` 
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    night_mode = json_data["night_mode"]
    user_agent = json_data.get("user_agent", "") 

    # Get the request ip
    client_ip = get_client_ip(request) or ""
    
    # Set mailing list preferences
    pref_ok = svc_set_night_mode(current_user, night_mode)

    if not pref_ok:
        log_set_night_mode(500, "System error prevented preference change.", user_agent, client_ip, current_user.id)
        return jsonify({"response": "An error occurred: please try again later."}), 500
    
    log_set_night_mode(200, f"Night mode set to {night_mode}.", user_agent, client_ip, current_user.id)
    
    response_data ={
            "response":"Night mode set successfully!",
            "night_mode_enabled": current_user.night_mode_enabled
        }
    return jsonify(response_data), 200
