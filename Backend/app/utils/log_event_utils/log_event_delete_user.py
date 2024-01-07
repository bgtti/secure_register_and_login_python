from app.utils.log_event_utils.constants import REQUIRED, LOG_EVENT_TYPE, LOG_EVENT_ACTIVITY, LOG_EVENT_LEVEL

# Activity = delete user
# LEDU = log event delete user

# Admin-driven events
# User_uuid is not that of the admin, but that of the user

LOG_EVENT_DELETE_USER = {
    "LEDU_01": {
        "type": LOG_EVENT_TYPE["INFO"],
        "activity":LOG_EVENT_ACTIVITY ["delete_user"],
        "message": "admin successfully deleted user.",
        "user_uuid": REQUIRED,
        "level": LOG_EVENT_LEVEL["INFO"]
    },
    "LEDU_02": {
        "type": LOG_EVENT_TYPE["WARN"],
        "activity":LOG_EVENT_ACTIVITY ["delete_user"],
        "message": "there was a problem deleting the user. User might still be in db.",
        "user_uuid": REQUIRED,
        "level": LOG_EVENT_LEVEL["ERROR"]
    } 
}