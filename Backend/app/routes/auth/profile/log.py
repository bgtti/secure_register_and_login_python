# Python/Flask libraries
import logging

# Constants
from app.constants.log_events_security import SecurityEvent

# Services
from app.services.logging.security_log_services import svc_add_log_security

# Use for function: reset_password_token
def log_change_name(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
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
    
    activity = "change name"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    match http_code:
        case 200:
            message = "Name changed successfully."
            event = SecurityEvent.USER_NAME_CHANGE_SUCCESS
        case 207:
            message = "Name changed successfully." # User was flagged
            event = SecurityEvent.USER_NAME_CHANGE_SUCCESS
        case 400:
            message = "Name change failed: malformed client request." #likely impersonation, possible abuse
            level = "SUSPICIOUS"
            event = SecurityEvent.USER_NAME_CHANGE_FAILURE
        case 440:
            message = "Name change failed: user not found." 
            event = SecurityEvent.USER_NAME_CHANGE_FAILURE
        case 500:
            message = "Name change failed: system error."
            level = "WARNING"
            event = SecurityEvent.USER_NAME_CHANGE_FAILURE
        case _:
            level = "NOTSET"
            message = "Event not set."
            event = SecurityEvent.UNKNOWN_EVENT
            logging.error("Logging security error: unexpected HTTP code received.")
    
    svc_add_log_security(
        level,
        event,
        activity,
        message,
        text,
        user_ip,
        user_agent,
        user_id
        )
    
    return  