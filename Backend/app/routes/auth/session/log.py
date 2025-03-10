import logging
from app.extensions.extensions import  db
from app.models.log_activity import LogActivity

# Use for function: get_otp
def log_get_otp(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
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
    
    activity = "get otp"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    match http_code:
        case 200:
            message = "OTP successfully sent."
        case 404:
            message = "Failed: user not found."
        case 418:
            message = "Bot caught in honeypot."
            level = "BOT"
        case 500:
            message = "Error: OTP not sent."
            level = "WARNING"
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

# Use for function: login/logout
def log_login(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
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
    
    activity = "login"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    match http_code:
        case 200:
            message = "Login successfull."
        case 202:
            message = "First factor authenticated successfully."
        case 204:
            message = "Logout successfull."
        case 401:
            message = "Failed: authentication error."
        case 403:
            message = "Failed: user is blocked."
        case 404:
            message = "Failed: user not found."
        case 408:
            message = "Failed: process time limit expired."
        case 418:
            message = "Bot caught in honeypot."
            level = "BOT"
        case 422:
            message = "Failed: MFA factor skipped or request out of sequence."
            level = "SUSPICIOUS"
        case 500:
            message = "Error: OTP not sent."
            level = "WARNING"
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