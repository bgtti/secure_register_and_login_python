from app.extensions import  db
from app.models.log_event import LogEvent
from app.utils.log_event_utils.events_for_account import signup_event, login_event
from app.utils.log_event_utils.events_for_admin import block_user_event, delete_user_event
from app.utils.log_event_utils.events_for_contact import contact_form_event

# EVENT LOGS VERSUS OTHER LOGS:
# event logs are saved to an SQL database. These are easy to view and work with, but database errors happen.
# this is why activity events are logged to the database but another logging system is used to log... well, the system and its errors.
# keep this in mind when creating a new log_event
# log_events are displayed to admins in the FE in the form of user's history and can help flag suspiscious behaviour or answering user's question on why they are encountering some issue (admins can check the activity the user was performing when the error happened)
# do not track sensitive information in log_events or any other type of logging mechanism

LOG_EVENTS = {
    "ACCOUNT_SIGNUP": "ACCOUNT_SIGNUP",
    "ACCOUNT_LOGIN": "ACCOUNT_LOGIN",
    "ADMIN_BLOCK_USER": "ADMIN_BLOCK_USER",
    "ADMIN_DELETE_USER": "ADMIN_DELETE_USER",
    "CONTACT_FORM_MESSAGE": "CONTACT_FORM_MESSAGE"
}

# TODO: Changes: check events and delete those related to Json schema validation

def log_event(event_activity_name, event_code, user_id=0, extra_info=""):
    """
    log_event(event_activity_name: str, event_code: str, user_id: int, extra_info: str) -> None
    -----------------------------------------------------------------------------
    Function creates event log, saving it to the database. 
    Requires an event activity and code. Check log_event_utils for a list of valid log events, and the respective event for valid event_codes.
    Some events may require a user_id. When not given, defaults to 0.
    Extra information can be supplied to the log by passing it to extra_info
    -----------------------------------------------------------------------------
    Example usage 1: 
    log_event("ACCOUNT_SIGNUP", "signup successful")
    Example usage 2: 
    log_event(LOG_EVENTS["ACCOUNT_LOGIN"], "login successful", 
                user_id=23)
    """

    event_activity = LOG_EVENTS.get(event_activity_name)

    if event_activity is None:
        raise ValueError(f"log_event function: wrong event activity: {event_activity}. Possible activities: {LOG_EVENTS.keys()}.")
    
    match event_activity:
        case "ACCOUNT_SIGNUP":
            log_obj = signup_event(event_code)
        case "ACCOUNT_LOGIN":
            log_obj = login_event(event_code)
        case "ADMIN_BLOCK_USER":
            log_obj = block_user_event(event_code)
        case "ADMIN_DELETE_USER":
            log_obj = delete_user_event(event_code)
        case "CONTACT_FORM_MESSAGE":
            log_obj = contact_form_event(event_code)
        case _:
            raise ValueError(f"log_event function: wrong event activity?")

    if log_obj == False:
        raise ValueError(f"log_event function: wrong event code: {event_code}. Chech the relevant event for possibilities.")
    
    if log_obj['user_id'] == "REQUIRED" and user_id == 0:
        raise ValueError(f"log_event function: missing user_id for event code {event_code}")
    
    if extra_info == "":
        message = log_obj["message"]
    else:
        message = f"{log_obj["message"]} {extra_info}"

    new_log_event = LogEvent(
        level=log_obj["level"],
        type=log_obj["type"],
        activity=log_obj["activity"],
        message=message,
        user_uuid="", # DELETE
        user_id=user_id
    )
    db.session.add(new_log_event)
    db.session.commit()