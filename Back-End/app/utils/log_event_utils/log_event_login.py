from app.utils.log_event_utils.constants import REQUIRED, NONE, LOG_EVENT_TYPE, LOG_EVENT_ACTIVITY, LOG_EVENT_LEVEL

LOG_EVENT_LOGIN = {
    "LEL_01": {
        "type": LOG_EVENT_TYPE["INFO"],
        "activity": LOG_EVENT_ACTIVITY["login"],
        "message": "successful login.",
        "user_uuid": REQUIRED,
        "level": LOG_EVENT_LEVEL["INFO"]
    },
    "LEL_02": {
        "type": LOG_EVENT_TYPE["INFO"],
        "activity": LOG_EVENT_ACTIVITY["login"],
        "message": "login rejected: schema validation failure.",
        "user_uuid": NONE,
        "level": LOG_EVENT_LEVEL["INFO"]
    },
    "LEL_03": {
        "type": LOG_EVENT_TYPE["INFO"],
        "activity": LOG_EVENT_ACTIVITY["login"],
        "message": "login rejected: user does not exist.",
        "user_uuid": NONE,
        "level": LOG_EVENT_LEVEL["INFO"]
    },
    "LEL_04": {
        "type": LOG_EVENT_TYPE["INFO"],
        "activity": LOG_EVENT_ACTIVITY["login"],
        "message": "login rejected: user is blocked.",
        "user_uuid": REQUIRED,
        "level": LOG_EVENT_LEVEL["INFO"]
    },
    "LEL_05": {
        "type": LOG_EVENT_TYPE["INFO"],
        "activity": LOG_EVENT_ACTIVITY["login"],
        "message": "login rejected: user is temporarily blocked.",
        "user_uuid": REQUIRED,
        "level": LOG_EVENT_LEVEL["INFO"]
    },
    "LEL_06": {
        "type": LOG_EVENT_TYPE["INFO"],
        "activity": LOG_EVENT_ACTIVITY["login"],
        "message": "login rejected: wrong password. Login attempt number: X",
        "user_uuid": REQUIRED,
        "level": LOG_EVENT_LEVEL["INFO"]
    },
    "LEL_07": {
        "type": LOG_EVENT_TYPE["WARN"],
        "activity": LOG_EVENT_ACTIVITY["login"],
        "message": "login rejected: wrong password input more than 5 times. Login attempt number: X",
        "user_uuid": REQUIRED,
        "level": LOG_EVENT_LEVEL["INFO"]
    },
    "LEL_08": {
        "type": LOG_EVENT_TYPE["SUSPISCIOUS"],
        "activity": LOG_EVENT_ACTIVITY["login"],
        "message": "html might have been supplied in form.",
        "user_uuid": REQUIRED,
        "level": LOG_EVENT_LEVEL["INFO"]
    }
}