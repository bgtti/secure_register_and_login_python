"""
** Log helpers: auth > session **

Session routes trigger Security Events (and not Action Events)

**General:**

Log helpers to be used in routes to log to the DB.
Should be used in route functions.

Where will the logs be stored?
--> Security logs: safety-revelant events (see SecurityEvent: constant > log_events_security and relevant DB model)
--> Action logs: non-safety-relevant events (see ActionEvent: constants > log_event_action and relevant DB model)

**How these functions were designed**

Routes must pass parameters:

http_code => the function will contain rules for what it accepts. Each accepted code will translate to a standardized message, level, and event description that will be saved to the DB log.
text => allows the route to send more information about the log (this will not be sent to the FE)
user_agent => user agent of the client who accessed the route 
user_ip => ip of the client who accessed the route 
user_id => if od the user (or 0 if unkown) 

The log helper functions will then create the log by defining internally:
- activity being performed (eg: "get_otp")
- message that may be displayed by the FE to the user
- event that should be a member of either the SecurityEvent or ActionEvent class (depending on whether the function is creating a standard or a security log) 
- level that must be a member of the constant LOG_LEVEL dictionary

Note about the "http_code" function parameter:

It is not quite used as http_codes are, but rather a number to match a case described by the function (the code chosen matches the idea or sentiment of the http code). Instead of creating a random dictionary, http codes were used and may have a different meaning, but matches the overall idea of what is going on. For instance "200" will indicate something that was successfull while "400" will indicate something failed. It was arbitrarily chosen, and their meaning is explained inside the match/case part of the function.
"""
# Python/Flask libraries
import logging

# Constants
from app.constants.log_events_security import SecurityEvent

# Services
from app.services.logging.security_log_services import svc_add_log_security

def log_admin_change_user_flag(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Helper function for get_otp route.
    Function will call `svc_add_log_security` to add a security log to the db. 

    ----------------------------------------------------
    
    :param http_code: the http-based case code (eg: 200)
    :param text: extra information relevant to the log (free text)
    :param user_agent: the user agent
    :param user_ip: the admin user's ip address (not anonymous)
    :param user_id: the admin user's id 
    """
    if http_code is None:
        logging.error("Logging activity error: http_code is None.")
        return
    
    activity = "admin - change user flag"
    level = "" # According to the dictionary defined in constants/log_level.py
    message = ""
    event = SecurityEvent.ADMIN_MODIFIED_USER
    match http_code:
        case 200:
            message = "Admin changed user flag."
            level = "INFO"
        case 404:
            message = "Error: user not found. Flag not changed."
            level = "INFO"
        case 500:
            message = "Error: user flag not changed due to server error."
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

def log_user_role_change(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Helper function for get_otp route.
    Function will call `svc_add_log_security` to add a security log to the db. 

    ----------------------------------------------------
    
    :param http_code: the http-based case code (eg: 200)
    :param text: extra information relevant to the log (free text)
    :param user_agent: the user agent
    :param user_ip: the admin user's ip address (not anonymous)
    :param user_id: the admin user's id 
    """
    if http_code is None:
        logging.error("Logging activity error: http_code is None.")
        return
    
    activity = "admin - change user role"
    level = "" # According to the dictionary defined in constants/log_level.py
    message = ""
    event = SecurityEvent.USER_ROLE_CHANGED 
    match http_code:
        case 200:
            message = "Admin changed user role."
            level = "IMPORTANT"
        case 403:
            message = "Error: role change forbidden. User role unchanged."
            level = "WARNING"
        case 404:
            message = "Error: role not found. User role unchanged."
            level = "ERROR"
        case 500:
            message = "Error: user role unchanged due to server error."
            level = "ERROR"
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

def log_user_block_status(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Helper function for get_otp route.
    Function will call `svc_add_log_security` to add a security log to the db. 

    ----------------------------------------------------
    
    :param http_code: the http-based case code (eg: 200)
    :param text: extra information relevant to the log (free text)
    :param user_agent: the user agent
    :param user_ip: the admin user's ip address (not anonymous)
    :param user_id: the admin user's id 
    """
    if http_code is None:
        logging.error("Logging activity error: http_code is None.")
        return
    
    activity = "admin - change user block status"
    level = "" # According to the dictionary defined in constants/log_level.py
    message = ""
    event = SecurityEvent.ACCOUNT_BLOCKED_STATUS_CHANGED_BY_ADMIN
    match http_code:
        case 200:
            message = "Admin blocked/unblocked user."
            level = "INFO"
        case 403:
            message = "Error: block/unblock forbidden. User blocked status unchanged."
            level = "WARNING"
        case 404:
            message = "Error: user not found. User blocked status unchanged."
            level = "ERROR"
        case 500:
            message = "Error: user blocked status unchanged due to server error."
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

def log_user_deleted_by_admin(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Helper function for get_otp route.
    Function will call `svc_add_log_security` to add a security log to the db. 

    ----------------------------------------------------
    
    :param http_code: the http-based case code (eg: 200)
    :param text: extra information relevant to the log (free text)
    :param user_agent: the user agent
    :param user_ip: the admin user's ip address (not anonymous)
    :param user_id: the admin user's id 
    """
    if http_code is None:
        logging.error("Logging activity error: http_code is None.")
        return
    
    activity = "admin - user deletion"
    level = "" # According to the dictionary defined in constants/log_level.py
    message = ""
    event = SecurityEvent.ADMIN_DELETED_USER
    match http_code:
        case 200:
            message = "Admin deleted user."
            level = "INFO"
        case 403:
            message = "Error: user deletion forbidden. User not deleted."
            level = "WARNING"
        case 404:
            message = "Error: user not found. User not deleted."
            level = "ERROR"
        case 405:
            message = "Error: attemp to delete own account. User not deleted."
            level = "ERROR"
        case 500:
            message = "Error: user not deleted due to server error."
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