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

# Utilities
from app.utils.custom_decorators.json_schema_validator import validate_schema

# Auth helpers
from app.routes.user_settings.schemas import (
    set_mailing_list_schema,
    set_night_mode_schema
)

# Blueprint
user_settings = Blueprint("user_settings", __name__)


############# ROUTES ###############


####################################
#    SET MAILING LIST PREFERENCE   #
####################################

@user_settings.route("/set_mailing_list", methods=["POST"])
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
    - "in_mailing_list" value only included if response is successfull.

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
    mailing_list = json_data["mailing_list"]
    user_agent = json_data.get("user_agent", "") #TODO log this in event

    # Get the user from cookie 
    try:
        user = User.query.filter_by(email=current_user.email).first()
    except Exception as e:
        logging.error(f"Failed to get user. Error: {e}")
        return jsonify({"response": "A database error prevented user retrieval."}), 500
    
    # Set mailing list preferences
    try:
        user.set_mailing_list(mailing_list)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"Failed to set mailing list. Error: {e}")
        return jsonify({"response": "A database error prevented setting mailing list preferences."}), 500
    
    response_data ={
            "response":"Mailing list set successfully!",
            "in_mailing_list": user.in_mailing_list.value
        }
    return jsonify(response_data)

####################################
#     SET NIGHT MODE PREFERENCE    #
####################################

@user_settings.route("/set_night_mode", methods=["POST"])
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
    - "night_mode_enabled" value only included if response is successfull.

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
    user_agent = json_data.get("user_agent", "") #TODO log this in event

    # Get the user from cookie 
    try:
        user = User.query.filter_by(email=current_user.email).first()
    except Exception as e:
        logging.error(f"Failed to get user. Error: {e}")
        return jsonify({"response": "A database error prevented user retrieval."}), 500
    
    # Set mailing list preferences
    try:
        user.set_night_mode(night_mode)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"Failed to set night mode. Error: {e}")
        return jsonify({"response": "A database error prevented setting night mode preferences."}), 500
    
    response_data ={
            "response":"Night mode set successfully!",
            "night_mode_enabled": user.night_mode_enabled.value
        }
    return jsonify(response_data)