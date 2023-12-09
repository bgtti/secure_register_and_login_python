from app.utils.log_event_utils.constants import REQUIRED, NONE, LOG_EVENT_TYPE, LOG_EVENT_ACTIVITY, LOG_EVENT_LEVEL
# Activity = signup
# LES = log event signup

# LES-04 has a category of 'warn' because it shold indicate the front end failed to stop this request from being send.
# The front-end should have the same list of weak passwords as the backend. The fact the weak password was sent means there is a failure in sync of the common password list or the user has meddled with the front-end to send the request anyway.

LOG_EVENT_SIGNUP = {
    "LES_01": {
        "type": LOG_EVENT_TYPE["INFO"],
        "activity": LOG_EVENT_ACTIVITY["signup"],
        "message": "successful signup.",
        "session_id": REQUIRED,
        "level": LOG_EVENT_LEVEL["INFO"]
    },
    "LES_02": {
        "type": LOG_EVENT_TYPE["INFO"],
        "activity": LOG_EVENT_ACTIVITY["signup"],
        "message": "signup rejected: schema validation failure.",
        "session_id": NONE,
        "level": LOG_EVENT_LEVEL["INFO"]
    },
    "LES_03": {
        "type": LOG_EVENT_TYPE["INFO"],
        "activity": LOG_EVENT_ACTIVITY["signup"],
        "message": "signup rejected: user already exists.",
        "session_id": REQUIRED,
        "level": LOG_EVENT_LEVEL["INFO"]
    },
    "LES_04": {
        "type": LOG_EVENT_TYPE["WARN"],
        "activity": LOG_EVENT_ACTIVITY["signup"],
        "message": "signup rejected: weak password",
        "session_id": NONE,
        "level": LOG_EVENT_LEVEL["INFO"]
    },
    "LES_05": {
        "type": LOG_EVENT_TYPE["WARN"],
        "activity": LOG_EVENT_ACTIVITY["signup"],
        "message": "signup failure: user could not be created.",
        "session_id": NONE,
        "level": LOG_EVENT_LEVEL["ERROR"]
    },
    "LES_06": {
        "type": LOG_EVENT_TYPE["SUSPISCIOUS"],
        "activity": LOG_EVENT_ACTIVITY["signup"],
        "message": "html might have been supplied in form.",
        "session_id": REQUIRED,
        "level": LOG_EVENT_LEVEL["INFO"]
    }
}