# Python/Flask libraries, extensions and config
import logging
from app.extensions.extensions import db

# DB models
from app.models.log_activity import LogActivity

# Constants and helpers
from app.constants.log_levels import LOG_LEVEL
from app.constants.log_events_action import ActionEvent

def svc_add_log_activity(level: str, event: ActionEvent, activity: str, message: str, more_info: str, ip: str, user_agent: str, user_id: int) -> None:
    """
    Adds a log to LogActivity db table.

    :param level (str): a key in LOG_LEVEL dictionary (`app/constants/log_levels.py`)
    :param event (ActionEvent): enum in ActionEvent (`app/constants/log_event_action.py`)
    :param activity (str): string describing the activity the user was trying to perform.
    :param message (str): string describing the event. Safe to show to end users.
    :param more_info (str): Internal technical details for developers / admins only.
    :param ip (str): IP address of user
    :param user_agent (str): HTTP User-Agent string.
    :param user_id (int): ID of the user who triggered the event (or 0 if unknown).

    --------
    Example usage: 
    ```
    try: 
        svc_add_log_security(
        "WARNING",
        ActionEvent.SET_MAILING_LIST,
        "set mailing list",
        "Mailing list preferences changed successfully.",
        "User included in mailing list.",
        "192.168.1.100",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        145
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"LogAction creation failed. Log event: {event}, user id: {user_id}  Error: {e}")
    ```
    """
    if not level in LOG_LEVEL:
        raise ValueError("Level must be a member of LOG_LEVEL - dictionary in 'constants' package.")
    if not isinstance(event, ActionEvent):
        raise ValueError("Event must be a member of ActionEvent - enum class in 'constants' package.")
    if not isinstance(activity, str):
        activity = "-"
    if not isinstance(message, str):
        message = "-"
    if not isinstance(more_info, str):
        more_info = "-"
    if not isinstance(ip, str):
        ip = ""
    if not isinstance(user_agent, str):
        user_agent = "N/A"
    if not isinstance(user_id, int):
        raise ValueError("User id must be an int. If unknown, enter '0'.")
    
    activity_lc = activity.lower()
    
    try:
        new_log= LogActivity(
                level=level,
                event=event,
                activity=activity_lc,
                message=message,
                more_info=more_info,
                ip=ip,
                user_agent=user_agent,
                user_id=user_id  
                )
        db.session.add(new_log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"LogActivity creation failed. Log activity: {activity_lc}, level: {level}  Error: {e}")
    return

def svc_user_activity_log_table(user_id: int, page_nr: int, items_per_page: int = 25, internal_use: bool = False) -> dict | None:
    """
    Serializes the user's activity log table paginated. Will be ordered descending by created_at date.
    Important: different from svc_user_security_log_table in that ip will be anonymized and no geo_location present.
    
    :param user_id (int): id of user whose log table is desired.
    :param page_nr (int): the page number, must be greater than 0.
    :param items_per_page (int): number of user items, must be greater than 0 and unser 100. Defaults to 25.
    :param internal_use (bool): if the table is public/user-facing (False) or for internal/admin use (True). Defaults to False.

    Returns:
        dict | None: None if no logs are found, otherwise a dictionary containing: current_page (int), total_pages (int), and logs (list of logs dict)
    
    Example of return data:
    ```python
    {
        "current_page": 1,
        "total_pages": 5,
        "logs": [
            {
            "id": 10,
            "created_at": "Thu, 25 Jan 2024 00:00:00 GMT",
            "message": "Successful login.",
            "level": "INFO", # only if internal_use == True
            "level_id": 10, # only if internal_use == True
            "event": "login", # only if internal_use == True
            "activity": "login", # only if internal_use == True
            "ip_address": "192.168.1.0", # only if internal_use == True
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", # only if internal_use == True
            }, 
            #...
        ]
    }
    ```
    """
    # Check params
    if not isinstance(user_id, int) or user_id < 1:
        logging.error("svc_user_activity_log_table received invalid user_id.")
        return None
    if page_nr < 1 or items_per_page < 1 or items_per_page > 100:
        logging.error("svc_user_activity_log_table received invalid page_nr or items_per_page.")
        return None
    
    # Get logs
    try:
        logs = LogActivity.query.filter_by(user_id=user_id).order_by(LogActivity.created_at.desc()).paginate(page=page_nr, per_page=items_per_page, error_out=False)
        if not logs.items:
            return None
    except Exception as e:
        logging.error(f"Failed to access DB. Error: {e}")
        return None
    
    def serialize(log):
        public = {
            "id": log.id,
            "created_at": log.created_at,
            "message": log.message,
        }
        # Not public-facing:
        if internal_use:
            private = {
                "level": log.level,
                "level_id": log.level_id,
                "event": (log.event.value).lower().replace("_", " "), # is enum
                "activity": log.activity,
                "more_info": log.more_info,
                "ip_address": log.ip_address, 
                "geo_location": log.geo_location,
                "user_agent": log.user_agent
            }
            return public | private
        return public
    
    return {
        "logs": [serialize(log) for log in logs.items],
        "total_pages": logs.pages,
        "current_page": logs.page,
    }