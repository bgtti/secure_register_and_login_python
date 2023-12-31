from app.utils.log_event_utils.constants import REQUIRED, LOG_EVENT_TYPE, LOG_EVENT_ACTIVITY, LOG_EVENT_LEVEL

# Activity = block and unblock users
# LEB = log event block
# LEU = log event unblock

# Admin-driven events
# User_uuid is not that of the admin, but that of the user

LOG_EVENT_BLOCK = {
    "LEB_01": {
        "type": LOG_EVENT_TYPE["INFO"],
        "activity":LOG_EVENT_ACTIVITY ["block"],
        "message": "admin successfully blocked user.",
        "user_uuid": REQUIRED,
        "level": LOG_EVENT_LEVEL["INFO"]
    },
    "LEB_02": {
        "type": LOG_EVENT_TYPE["WARN"],
        "activity":LOG_EVENT_ACTIVITY ["block"],
        "message": "there was a problem blocking the user. User might still be unblocked.",
        "user_uuid": REQUIRED,
        "level": LOG_EVENT_LEVEL["ERROR"]
    } 
}

LOG_EVENT_UNBLOCK = {
    "LEU_01": {
        "type": LOG_EVENT_TYPE["INFO"],
        "activity":LOG_EVENT_ACTIVITY ["unblock"],
        "message": "admin successfully unblocked user.",
        "user_uuid": REQUIRED,
        "level": LOG_EVENT_LEVEL["INFO"]
    },
    "LEU_02": {
        "type": LOG_EVENT_TYPE["WARN"],
        "activity":LOG_EVENT_ACTIVITY ["unblock"],
        "message": "there was a problem unblocking the user. User might still be blocked.",
        "user_uuid": REQUIRED,
        "level": LOG_EVENT_LEVEL["ERROR"]
    } 
}