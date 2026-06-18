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


def log_password_change(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Helper function for change_password route.
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
    
    activity = "change password"
    level = "INFO" # According to the dictionary defined in models/log_security.py
    message = ""
    match http_code:
        case 200:
            message = "Password changed successfully."
            event = SecurityEvent.PASSWORD_CHANGE_SUCCESS
        case 400:
            message = "Password change failed: malformed client request."
            event = SecurityEvent.PASSWORD_CHANGE_FAILURE
            level = "ERROR"
        case 401:
            message = "Password change failed: unauthorized."
            event = SecurityEvent.PASSWORD_CHANGE_FAILURE
        case 403:
            message = "Password change failed: too many failed attempts."
            event = SecurityEvent.PASSWORD_CHANGE_FAILURE
        case 404:
            message = "Password change failed: user not found."
            event = SecurityEvent.PASSWORD_CHANGE_FAILURE
        case 418:
            message = "Password change required extra verification." #"Bot caught in honeypot."
            event = SecurityEvent.HONEYPOT_TRIGGERED
        case 500:
            message = "Error: password change or reset failed."
            level = "WARNING"
            event = SecurityEvent.PASSWORD_CHANGE_FAILURE
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


def log_request_reset_password(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Helper function for request_reset_password.
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
    
    activity = "password reset request"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    event = ""
    match http_code:
        case 200:
            message = "Password reset security code(s) sent to email."
            event = SecurityEvent.PASSWORD_RESET_REQUESTED
        case 403:
            message = "Request failed: user was blocked"
            event = SecurityEvent.PASSWORD_RESET_REQUEST_FAILURE
        case 404:
            message = "Request failed: user not found."
            event = SecurityEvent.PASSWORD_RESET_REQUEST_FAILURE
            # only suspiscious if we get a lot of logs like this..
        case 418:
            message = "Password change required extra verification." #"Bot caught in honeypot."
            event = SecurityEvent.HONEYPOT_TRIGGERED
        case 500:
            message = "Error: password reset failed."
            level = "WARNING"
            event = SecurityEvent.PASSWORD_RESET_REQUEST_FAILURE
        case 501:
            message = "Error: password reset failed due to system error."
            level = "CRITICAL"
            event = SecurityEvent.PASSWORD_RESET_REQUEST_FAILURE
        case _:
            level = "NOTSET"
            message = "Event not set."
            event = SecurityEvent.UNKNOWN_EVENT
            logging.error("Logging activity error: unexpected HTTP code received.")
    
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


def log_reset_password(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Helper function for reset_password.
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
    
    activity = "password reset"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    event = ""
    match http_code:
        case 200:
            message = "Password reset successful."
            event = SecurityEvent.PASSWORD_RESET_SUCCESS
        case 202:
            message = "Password reset required second code."
            event = SecurityEvent.PASSWORD_RESET_STEP_1
        case 400:
            message = "Password reset failed: malformed client request."
            event = SecurityEvent.PASSWORD_RESET_FAILURE
            level = "ERROR"
        case 401:
            message = "Password reset failed: invalid security code(s)."
            event = SecurityEvent.PASSWORD_RESET_FAILURE
        case 403:
            message = "Password reset failed: user was blocked"
            event = SecurityEvent.PASSWORD_RESET_FAILURE
        case 404:
            message = "Password reset failed: user not found."
            event = SecurityEvent.PASSWORD_RESET_FAILURE
            # only suspiscious if we get a lot of logs like this..
        case 418:
            message = "Password change required extra verification." #"Bot caught in honeypot."
            event = SecurityEvent.HONEYPOT_TRIGGERED
        case 500:
            message = "Error: password reset failed."
            level = "WARNING"
            event = SecurityEvent.PASSWORD_RESET_FAILURE
        case _:
            level = "NOTSET"
            message = "Event not set."
            event = SecurityEvent.UNKNOWN_EVENT
            logging.error("Logging activity error: unexpected HTTP code received.")
    
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

def log_request_change_email(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Helper function for request_change_email.
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
    
    activity = "request email change"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    event = ""
    match http_code:
        case 200:
            message = "Email change request successful."
            event = SecurityEvent.EMAIL_CHANGE_REQUESTED
        case 400:
            message = "Email change request failed: input not accepted."
            event = SecurityEvent.EMAIL_CHANGE_REQUEST_FAILURE
        case 403:
            message = "Email change request failed: user was blocked."
            event = SecurityEvent.EMAIL_CHANGE_REQUEST_FAILURE
        case 409:
            message = "Email change request failed: input rejected." # Email used by another user
            event = SecurityEvent.EMAIL_CHANGE_REQUEST_FAILURE
        case 500:
            message = "Email change request failed: system error."
            level = "WARNING"
            event = SecurityEvent.EMAIL_CHANGE_REQUEST_FAILURE
        case _:
            level = "NOTSET"
            message = "Event not set."
            event = SecurityEvent.UNKNOWN_EVENT
            logging.error("Logging activity error: unexpected HTTP code received.")
    
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

def log_change_email(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Helper function for change_email.
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
    
    activity = "change email"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    event = ""
    match http_code:
        case 200:
            message = "Email change successful."
            event = SecurityEvent.EMAIL_CHANGE_SUCCESS
        case 400:
            message = "Email change failed: input not accepted."
            event = SecurityEvent.EMAIL_CHANGE_FAILURE
        case 403:
            message = "Email change failed: user was blocked."
            event = SecurityEvent.EMAIL_CHANGE_FAILURE
        case 500:
            message = "Email change failed: system error."
            level = "WARNING"
            event = SecurityEvent.EMAIL_CHANGE_FAILURE
        case _:
            level = "NOTSET"
            message = "Event not set."
            event = SecurityEvent.UNKNOWN_EVENT
            logging.error("Logging activity error: unexpected HTTP code received.")
    
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
