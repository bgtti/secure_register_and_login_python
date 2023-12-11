from app.extensions import  db
from app.models.log_event import LogEvent
from app.utils.log_event_utils.log_event_activities_all import LOG_EVENT_ACTIVITIES

def log_event(event_activity_name, event_code, user_uuid="none"):
    """
    log_event(event_activity_name: str, event_code: str, user_uuid: str) -> None
    -----------------------------------------------------------------------------
    Function creates event log, saving it to the database. 
    Requires an event activity and code. 
    Some events may require a user_uuid. When not given, defaults to "none".
    -----------------------------------------------------------------------------
    Example usage 1: 
    log_event("LOG_EVENT_LOGIN", "LEL_02")
    Example usage 2: 
    log_event(LOG_EVENT_ACTIVITIES["LOG_EVENT_LOGIN"], "LEL_01", 
                user_uuid="48d1b6dd-0e1c-452c-93c8-feddb001c8b1")
    """

    event_activity = LOG_EVENT_ACTIVITIES.get(event_activity_name)

    if event_activity is None:
        raise ValueError(f"log_event function: wrong event activity: {event_activity}. Possible activities: {LOG_EVENT_ACTIVITIES.keys()}.")

    event_values = event_activity.get(event_code)

    if event_values is None:
        raise ValueError(f"log_event function: wrong event code: {event_code}. Possible codes: {event_activity.keys()}.")
    
    if event_values['user_uuid'] == "REQUIRED" and user_uuid == "none":
        raise ValueError(f"log_event function: missing user_uuid for event code {event_code}")

    new_log_event = LogEvent(
        level=event_values["level"],
        type=event_values["type"],
        activity=event_values["activity"],
        message=event_values["message"],
        user_uuid=user_uuid
    )
    db.session.add(new_log_event)
    db.session.commit()