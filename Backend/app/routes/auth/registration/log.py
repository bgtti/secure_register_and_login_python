"""
** Log helpers: auth > registration **

Registration routes trigger Security Events (and not Action Events)

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

# Extensions
from app.extensions.extensions import  db

# Constants
from app.constants.log_events_security import SecurityEvent
from app.models.log_activity import LogActivity

# Services
from app.services.logging.security_log_services import svc_add_log_security

# Use for function: signup_user
def log_signup_user(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Helper function for signup_user route.
    Function will call `svc_add_log_security` to add a security log to the db.

    ----------------------------------------------------
    
    :param http_code: the http-based case code (eg: 200)
    :param text: extra information relevant to the log (free text)
    :param user_agent: the user agent
    :param user_ip: the user's ip address (not anonymous)
    :param user_id: the user's id if available (0 if not available)

    """
    if http_code is None:
        logging.error(f"Logging activity error: http_code is None. Args passed: {locals()}")
        return
    
    activity = "signup"
    level = "" # According to the dictionary defined in models/log_activity.py
    message = ""
    event = ""
    match http_code:
        case 200:
            message = "Successful signup."
            level = "INFO" 
            event = SecurityEvent.ACCOUNT_CREATED
        case 207:
            message = "Successful signup. Flag assigned." #indicates user was been flagged, but signup succeeded
            level = "SUSPICIOUS"
            event = SecurityEvent.ACCOUNT_CREATED
        case 400:
            message = "Signup failed: input does not meet criteria."
            level = "WARNING"
            event = SecurityEvent.ACCOUNT_CREATION_FAILURE
        case 409:
            message = "Signup failure: user exists."
            event = SecurityEvent.ACCOUNT_CREATION_FAILURE
        case 418:
            message = "Signup required extra verification" #"Bot caught in honeypot."
            level = "BOT"
            event = SecurityEvent.HONEYPOT_TRIGGERED
        case 500:
            message = "Signup failed: could not add user to db."
            event = SecurityEvent.ACCOUNT_CREATION_FAILURE
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

# Use for function: delete_user
def log_delete_user(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Helper function for delete_user route.
    Function will call `svc_add_log_security` to add a security log to the db. 

    ----------------------------------------------------
    
    :param http_code: the http-based case code (eg: 200)
    :param text: extra information relevant to the log (free text)
    :param user_agent: the user agent
    :param user_ip: the user's ip address (not anonymous)
    :param user_id: the user's id if available (0 if not available)
    """
    if http_code is None:
        logging.error("Logging activity error: http_code is None.")
        return
    
    activity = "account deletion"
    level = "" # According to the dictionary defined in constants/log_level.py
    message = ""
    event = ""
    match http_code:
        case 200:
            message = "User successfully deleted account."
            level = "INFO"
            event = SecurityEvent.ACCOUNT_DELETED
        case 401:
            message = "Deletion failed: wrong credentials."
            level = "INFO"
            event = SecurityEvent.ACCOUNT_DELETION_FAILURE
        case 403: # to be used when trying to delete super admin account
            message = "Deletion forbidden: this account cannot be deleted."
            level = "CRITICAL"
            event = SecurityEvent.ACCOUNT_DELETION_FAILURE 
        case 404:
            message = "Deletion failed: user not found."
            level = "ERROR"
            event = SecurityEvent.ACCOUNT_DELETION_FAILURE 
        case 500:
            message = "Deletion failed: could not delete user from db."
            level = "ERROR"
            event = SecurityEvent.ACCOUNT_DELETION_FAILURE 
        case 501:
            message = "Deletion failed: system error."
            level = "CRITICAL"
            event = SecurityEvent.ACCOUNT_DELETION_FAILURE 
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
