import logging
from app.extensions.extensions import  db
from app.models.log_activity import LogActivity

# Use for function: set_recovery_email
def log_set_recovery_email(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
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
    
    activity = "set recovery email"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    match http_code:
        case 200:
            message = "Recovery email set."
        case 204:
            message = "Old recovery email replaced."
        case 207:
            message = "Recovery email may be set. User flagged."
        case 400:
            message = "Failed: recovery email must be different than account email."
        case 401:
            message = "Failed: authentication error."
        case 500:
            message = "Error: recovery email not set."
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

# TODO: more log functions here