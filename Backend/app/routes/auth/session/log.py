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

# Extensions
from app.extensions.extensions import  db

# Constants
from app.constants.log_events_security import SecurityEvent

# Services
from app.services.logging.security_log_services import svc_add_log_security

def log_get_otp(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Helper function for get_otp route.
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
    
    activity = "get otp"
    level = "" # According to the dictionary defined in constants/log_level.py
    message = ""
    event = ""
    match http_code:
        case 200:
            message = "OTP successfully sent."
            level = "INFO"
            event = SecurityEvent.OTP_SUCCESS
        case 404:
            message = "Failed: user not found."
            level = "INFO"
            event = SecurityEvent.OTP_FAILURE
        case 418:
            message = "Sign-in required extra verification" #"Bot caught in honeypot."
            level = "BOT"
            event = SecurityEvent.HONEYPOT_TRIGGERED
        case 500:
            message = "Error: OTP not sent due to server error."
            level = "WARNING"
            event = SecurityEvent.OTP_FAILURE
            logging.error(f"OTP not sent to user id {user_id} due to server error. SecurityLog likely failure")
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



def log_login_logout(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Helper function for login_user and logout_user routes.
    Function will call service `svc_add_log_security` (from `services/logging/security_log_services.py` to add a security log to the db. 

    ----------------------------------------------------
    Fields overview:

    **Parameters**

    :param http_code: the http error code (eg: 200) or one that best define the meaning of what happened. Not actual http codes sent to the front end necessarily. See inside the function to understand meaning.
    :param text: extra information relevant to the log (internal purposes)
    :param user_agent: the user agent
    :param user_ip: the user's ip address (not anonymous)
    :param user_id: the user's id if available (0 if not available)

    """
    if http_code is None:
        logging.error("Logging activity error: http_code is None.")
        return
    
    activity = "login"
    message = ""
    event = ""
    match http_code:
        case 200:
            message = "Login successfull."
            level = "INFO" # According to the dictionary defined in constants/log_level.py
            event = SecurityEvent.LOGIN_SUCCESS
        case 202:
            message = "First factor authenticated successfully."
            level = "INFO"
            event = SecurityEvent.LOGIN_MFA_FACTOR_1_SUCCESS
        case 204:
            activity = "logout"
            message = "Logout successfull."
            level = "INFO"
            event = SecurityEvent.LOGOUT
        case 401:
            message = "Failed: authentication error."
            level = "INFO"
            event = SecurityEvent.LOGIN_FAILURE
        case 403:
            message = "Failed: user is blocked."
            level = "INFO"
            event = SecurityEvent.LOGIN_FAILURE
        case 404:
            message = "Failed: user not found."
            level = "INFO"
            event = SecurityEvent.LOGIN_FAILURE
        case 408:
            message = "Failed: process time limit expired."
            level = "INFO"
            event = SecurityEvent.LOGIN_MFA_FACTOR_2_FAILURE
        case 418:
            message = "Sign-in required extra verification." #"Bot caught in honeypot."
            level = "BOT"
            event = SecurityEvent.HONEYPOT_TRIGGERED
        case 422:
            message = "Failed: MFA factor skipped or request out of sequence."
            level = "SUSPICIOUS"
            event = SecurityEvent.LOGIN_MFA_FACTOR_1_FAILURE
        case 424:
            message = "Failed: too many login attempts." # 6+ failed login attempts
            level = "SUSPICIOUS"
            event = SecurityEvent.MULTIPLE_FAILED_LOGINS
        case 429:
            message = "Failed: too many login attempts. Log-in blocked temporarily for 20 mins." # 8+ failed login attempts
            level = "WARNING"
            event = SecurityEvent.MULTIPLE_FAILED_LOGINS
        case 451:
            message = "Failed: too many login attempts. Log-in blocked temporarily for 60 mins." # 11+ failed login attempts
            level = "CRITICAL"
            event = SecurityEvent.POTENTIAL_BRUTE_FORCE
        case 500:
            message = "Error: server error."
            level = "WARNING"
            event = SecurityEvent.OTP_FAILURE
            logging.error(f"OTP not sent to user id {user_id} due to server error. SecurityLog likely failure")
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

