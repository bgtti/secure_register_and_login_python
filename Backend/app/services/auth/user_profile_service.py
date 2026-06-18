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

# Utils
from app.common.user_credential_helpers.name_validation import user_name_is_valid
from app.common.detect_html.detect_html import check_for_html
from app.common.profanity_check.profanity_check import has_profanity

# Services
from app.services.user.user_flag_service import svc_user_flag_change

def svc_change_user_name(user: User, new_name: str) -> dict:
    """
    Checks the new name against a list of reserved names, html, and profanity, then changes the name in the DB and commits if appropriate. 

    :param user (User): Member of the User db model class.
    :param new_name (str): The new name.

    Returns dictionary containing:
     - success (bool): True if new name saved to db, False otherwise.
     - flagged (bool): True if the user was flagged in the process, False otherwise.
     - log_code (int): an http-like code to be used for internal logging
     - log_text (str): a log message to be used internally.

    """
    res = {
        "success": False,
        "flagged": False,
        "log_text": "",
        "log_code":0
    }

    if not user or not new_name:
        log_msg = "Name change rejected: missing user or new name parameter to svc_change_user_name."
        res["log_code"] = 400
        res["log_text"] = log_msg
        logging.error(log_msg)
        return res

    name_is_ok = user_name_is_valid(new_name)

    if not name_is_ok: 
        res["log_code"] = 400
        res["log_text"] = f"Name change rejected: in list of reserved names. New name = {new_name}."
        logging.info(f"Change of name rejected for id={user.id}. New name likely in list of reserved names: {new_name}.")
        return res
    
    # Checking for html and profanity
    html_in_name = check_for_html(new_name, "auth - change_user_name", user.email)
    if html_in_name:
        res["flagged"] = True
        res["log_code"] = 207
        res["log_text"] = "Name changed, but user flagged: HTML detected in new name."
        svc_user_flag_change(user, "YELLOW")
    
    if not html_in_name:
        profanity_in_name = has_profanity(new_name) 
        if profanity_in_name:
            res["flagged"] = True
            res["log_code"] = 207
            res["log_text"] = "Name changed, but user flagged: profanity detected in new name."
            svc_user_flag_change(user, "PURPLE")

    old_name = user.name
    
    try:
        user.name = new_name
        db.session.commit()

        res["success"] = True

        if not res["flagged"]:
            res["log_code"] = 200
            res["log_text"] = f"Name changed successfully. Old name: {old_name}, new name: {new_name}"
    except Exception as e:
        db.session.rollback()
        log_message = f"User id={user.id} could not change name due to db error. Error: {str(e)}"
        logging.error(log_message)
        res["log_code"] = 500
        res["log_text"] = log_message
    
    return res
