import logging
from app.extensions.extensions import  db
from app.models.log_activity import LogActivity

# CRED_CHANGE_FUNCTION_DIC = {
#     "reset_password_token": "password reset token request",
#     "change_password": "change password request"
# }

# TODO: other functions for logging

# Use for function: reset_password_token
def log_reset_password_token(http_code: int, text: str="", user_agent: str="", user_ip: str="", user_id: int=0) -> None: 
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
    
    activity = "password reset token request"
    level = "INFO" # According to the dictionary defined in models/log_activity.py
    message = ""
    match http_code:
        case 200:
            message = "Password reset token sent to email."
        case 418:
            message = "Bot caught in honeypot."
        case 403:
            message = "User was blocked, request failed."
        case 404:
            message = "User not found."
            level = "SUSPICIOUS" #is it suspiscious?? user could have typed wrong..
        case 500:
            message = "Error in token creation."
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


