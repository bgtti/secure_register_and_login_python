# Python/Flask libraries
import logging

# Constants
from app.constants.log_events_security import SecurityEvent

# Services
from app.services.logging.security_log_services import svc_add_log_security

# Use for function: verify_account
def log_verify_account(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Function will log events from the route to the DB.

    :param http_code (int): the http error code (eg: 200)
    :param text (str): extra information relevant to the log
    :param user_agent (str): the user agent
    :param user_ip (str): the user's ip address (not anonymous)
    :param user_id (int): the user's id if available (0 if not available)

    """
    if http_code is None:
        logging.error("Logging security error: http_code is None.")
        return
    
    activity = "verify account email"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    event = SecurityEvent.EMAIL_VERIFICATION_SUCCESS
    match http_code:
        case 200:
            message = "Account successfully verified."
        case 206:
            message = "Account successfully verified." #Email sending failure
        case 401:
            message = "Account verification failed: OTP incorrect or expired." # OTP wrong/expired
            event = SecurityEvent.EMAIL_VERIFICATION_FAILURE
        case 440:
            message = "Account verification failed: authentication error." # User not found
            event = SecurityEvent.EMAIL_VERIFICATION_FAILURE
        case 500:
            message = "Account verification failed: system error."
            event = SecurityEvent.EMAIL_VERIFICATION_FAILURE
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

# Use for function: set_mfa
def log_set_mfa(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Function will log events from the route to the db.

    :param http_code (int): the http error code (eg: 200)
    :param text (str): extra information relevant to the log
    :param user_agent (str): the user agent
    :param user_ip (str): the user's ip address (not anonymous)
    :param user_id (int): the user's id if available (0 if not available)

    """
    if http_code is None:
        logging.error("Logging security error: http_code is None.")
        return
    
    activity = "set MFA"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    match http_code:
        case 200:
            message = "MFA successfully disabled." # MFA disabled
            event = SecurityEvent.MFA_DISABLED
        case 201:
            message = "MFA successfully enabled." # MFA enabled
            event = SecurityEvent.MFA_ENABLED
        case 206:
            message = "MFA successfully enabled." # MFA enabled but email failed
            event = SecurityEvent.MFA_ENABLED
        case 207:
            message = "MFA successfully disabled." # MFA disabled but email failed
            event = SecurityEvent.MFA_DISABLED
        case 401:
            message = "Failed to set MFA: incorrect password."
            event = SecurityEvent.MFA_SET_FAILURE
        case 403:
            message = "Failed to set MFA: pre-conditions not met." #verified email/missing recovery
            event = SecurityEvent.MFA_SET_FAILURE
            level = "ERROR"
        case 500:
            message = "Failed to set MFA: system error."
            event = SecurityEvent.MFA_SET_FAILURE
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