import logging
from app.extensions.extensions import  db
from app.models.log_activity import LogActivity

# CRED_CHANGE_FUNCTION_DIC = {
#     "reset_password_token": "password reset token request",
#     "change_password": "change password request"
# }

# TODO: other functions for logging

# Use for function: signup_user
def log_signup_user(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Function will log events from the route to the db.

    ---------------

    **Parameters**
    - http_code: the http error code (eg: 200)
    - text: extra information relevant to the log
    - user_agent: the user agent
    - user_ip: the user's ip address (not anonymous)
    - user_id: the user's id if available (0 if not available)

    """
    if http_code is None:
        logging.error("Logging activity error: http_code is None.")
        return
    
    activity = "signup"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    match http_code:
        case 200:
            message = "Successful signup."
        case 207:
            message = "Successful signup. Flag assigned." #indicates user was been flagged, but signup succeeded
            level = "SUSPICIOUS"
        case 400:
            message = "Signup failed: input does not meet criteria."
            level = "WARNING"
        case 409:
            message = "Signup failure: user exists."
        case 418:
            message = "Bot caught in honeypot."
            level = "BOT"
        case 500:
            message = "Signup failed: could not add user to db."
            level = "ERROR"
        case _:
            level = "NOTSET"
            logging.error("Logging activity error: unexpected HTTP code received.")
    
    try:
        new_log= LogActivity(
        level=level,
        activity=activity,
        message=message,
        more_info=text,
        ip=user_ip,
        user_agent=user_agent,
        user_id=user_id  
        )
        db.session.add(new_log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"LogActivity creation failed. Log activity: {activity}, http code: {http_code}  Error: {e}")
    return 

# Use for function: delete_user
def log_delete_user(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Function will log events from the route to the db.

    ---------------

    **Parameters**
    - http_code: the http error code (eg: 200)
    - text: extra information relevant to the log
    - user_agent: the user agent
    - user_ip: the user's ip address (not anonymous)
    - user_id: the user's id if available (0 if not available)

    """
    if http_code is None:
        logging.error("Logging activity error: http_code is None.")
        return
    
    activity = "account deletion"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    match http_code:
        case 200:
            message = "User successfully deleted account."
        case 400:
            message = "Signup failed: input does not meet criteria."
            level = "WARNING"
        case 401:
            message = "Deletion failed: wrong credentials."
        case 403: # to be used when trying to delete super admin account
            message = "Deletion forbidden: this account cannot be deleted." 
        case 404:
            message = "Deletion failed: user not found."
            level = "ERROR"
        case 418:
            message = "Bot caught in honeypot."
            level = "BOT"
        case 500:
            message = "Deletion failed: could not delete user from db."
            level = "ERROR"
        case _:
            level = "NOTSET"
            logging.error("Logging activity error: unexpected HTTP code received.")
    
    try:
        new_log= LogActivity(
        level=level,
        activity=activity,
        message=message,
        more_info=text,
        ip=user_ip,
        user_agent=user_agent,
        user_id=user_id  
        )
        db.session.add(new_log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"LogActivity creation failed. Log activity: {activity}, http code: {http_code}  Error: {e}")
    return 
