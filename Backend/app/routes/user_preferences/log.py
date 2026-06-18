# Python/Flask libraries
import logging

# Constants
from app.constants.log_events_action import ActionEvent

# Services
from app.services.logging.activity_log_services import svc_add_log_activity

def log_set_mailing_list(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Function will log events from the route to the db.

    :param http_code (int): the http error code (eg: 200)
    :param text (str): extra information relevant to the log (for internal use)
    :param user_agent (str): the user agent
    :param user_ip (str): the user's ip address (not anonymous)
    :param user_id (int): the user's id if available (0 if not available)

    """
    if http_code is None:
        logging.error("Logging activity error: http_code is None.")
        return
    
    activity = "set mailing list"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    event = ActionEvent.SET_MAILING_LIST
    match http_code:
        case 200:
            message = "Mailing list preference changed successfully." # MFA disabled
        case 500:
            message = "Failed to set mailing list preference: system error."
            level = "WARNING"
        case _:
            level = "NOTSET"
            message = "Unkown event: code error."
            logging.error("Logging activity error: unexpected HTTP code received.")
    
    svc_add_log_activity(
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

def log_set_night_mode(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
    """
    Function will log events from the route to the db.

    :param http_code (int): the http error code (eg: 200)
    :param text (str): extra information relevant to the log (for internal use)
    :param user_agent (str): the user agent
    :param user_ip (str): the user's ip address (not anonymous)
    :param user_id (int): the user's id if available (0 if not available)

    """
    if http_code is None:
        logging.error("Logging activity error: http_code is None.")
        return
    
    activity = "set night mode"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    event = ActionEvent.SET_NIGHT_MODE
    match http_code:
        case 200:
            message = "Night mode preference changed successfully." # MFA disabled
        case 500:
            message = "Failed to set night mode preference: system error."
            level = "WARNING"
        case _:
            level = "NOTSET"
            message = "Unkown event: code error."
            logging.error("Logging activity error: unexpected HTTP code received.")
    
    svc_add_log_activity(
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