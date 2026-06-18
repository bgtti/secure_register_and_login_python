# Python/Flask libraries
import logging

# Constants
from app.constants.log_events_security import SecurityEvent

# Services
from app.services.logging.security_log_services import svc_add_log_security


def log_req_set_recovery_email(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Helper function for request_set_recovery_email route.
    Function will call `svc_add_log_security` to add a security log to the DB.

    ---------------

    :param http_code: the http-based case code (eg: 200)
    :param text: extra information relevant to the log (free text)
    :param user_agent: the user agent
    :param user_ip: the user's ip address (not anonymous)
    :param user_id: the user's id if available (0 if not available)

    """
    if http_code is None:
        logging.error("Logging activity error: http_code is None.")
        return
    
    activity = "request to set recovery email"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    match http_code:
        case 200:
            message = "Security code sent to set recovery email."
            event = SecurityEvent.RECOVERY_EMAIL_SET_REQUEST
        case 400:
            message = "Failed to request set recovery email: malformed client request."
            event = SecurityEvent.RECOVERY_EMAIL_SET_REQUEST
        case 401:
            message = "Failed to request set recovery email: authentication error."
            event = SecurityEvent.RECOVERY_EMAIL_SET_REQUEST
        case 409:
            message = "Failed to request set recovery email: input rejected." # Email used by another user
            event = SecurityEvent.RECOVERY_EMAIL_SET_REQUEST
        case 500:
            message = "Error: new recovery email request not set."
            event = SecurityEvent.RECOVERY_EMAIL_SET_REQUEST
            level = "WARNING"
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



# Use for function: set_recovery_email
def log_set_recovery_email(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Function will log events from the route to the DB.

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
    
    activity = "set recovery email"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    match http_code:
        case 200:
            message = "Recovery email changed successfully."
            event = SecurityEvent.RECOVERY_EMAIL_SET_SUCCESS
        case 201:
            message = "Recovery email set successfully."
            event = SecurityEvent.RECOVERY_EMAIL_SET_SUCCESS
        case 400:
            message = "Failed to set recovery email: malformed client request." # security code wrong/expired
            event = SecurityEvent.RECOVERY_EMAIL_SET_FAILURE
        case 422:
            message = "Failed to set recovery email: email address missing."
            event = SecurityEvent.RECOVERY_EMAIL_SET_FAILURE
            level = "ERROR"
        case 440:
            message = "Failed to set recovery email: authentication error." # User not found
            event = SecurityEvent.RECOVERY_EMAIL_SET_FAILURE
        case 500:
            message = "Error: new recovery email not set."
            event = SecurityEvent.RECOVERY_EMAIL_SET_FAILURE
            level = "WARNING"
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

# Use for function: get_recovery_email
def log_get_recovery_email(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Function will log events from the route to the DB.

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
    
    activity = "view recovery email"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    event = SecurityEvent.RECOVERY_EMAIL_VIEW    
    match http_code:
        case 200:
            message = "Recovery email viewed successfully."
        case 401:
            message = "Failed to view recovery email: wrong password." # wrong password
        case 422:
            message = "Failed to view recovery email: resource not found."
            level = "ERROR"
        case 440:
            message = "Failed to view recovery email: authentication error." # User not found
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

# Use for function: delete_recovery_email
def log_delete_recovery_email(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Function will log events from the route to the DB.

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
    
    activity = "delete recovery email"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    event = SecurityEvent.RECOVERY_EMAIL_DELETION_SUCCESS   
    match http_code:
        case 200:
            message = "Recovery email deleted successfully."
        case 201:
            message = "Recovery email deleted successfully. MFA disabled."
        case 401:
            message = "Failed to delete recovery email: wrong password." # wrong password
            event = SecurityEvent.RECOVERY_EMAIL_DELETION_FAILED 
        case 422:
            message = "Failed to delete recovery email: resource not found."
            level = "ERROR"
            event = SecurityEvent.RECOVERY_EMAIL_DELETION_FAILED 
        case 440:
            message = "Failed to delete recovery email: authentication error." # User not found
        case 500:
            message = "Error: could not delete recovery email."
            event = SecurityEvent.RECOVERY_EMAIL_DELETION_FAILED 
            level = "WARNING"
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