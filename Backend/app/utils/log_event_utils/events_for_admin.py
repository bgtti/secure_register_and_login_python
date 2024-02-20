from app.utils.log_event_utils.constants import REQUIRED, NONE, LOG_EVENT_TYPE, LOG_EVENT_LEVEL


def block_user_event(event):
    log_obj = {
        "activity": "block_user",
        "message": "",
        "user_id": REQUIRED,
        "type": LOG_EVENT_TYPE["INFO"],
        "level": LOG_EVENT_LEVEL["INFO"],
    }
    match event:
        case "block user":
            log_obj["message"] = "admin successfully blocked user."
        case "unblock user":
            log_obj["message"] = "admin successfully unblocked user."
        case "block problem":
            log_obj["message"] = "there was a problem blocking the user. User might still be unblocked."
            log_obj["type"] = LOG_EVENT_TYPE["WARN"]
            log_obj["level"] = LOG_EVENT_LEVEL["ERROR"]
        case "unblock problem":
            log_obj["message"] = "there was a problem unblocking the user. User might still be blocked."
            log_obj["type"] = LOG_EVENT_TYPE["WARN"]
            log_obj["level"] = LOG_EVENT_LEVEL["ERROR"]
        case _:
            log_obj = False
    return log_obj

def delete_user_event(event):
    log_obj = {
        "activity": "delete_user",
        "message": "",
        "user_id": REQUIRED,
        "type": LOG_EVENT_TYPE["INFO"],
        "level": LOG_EVENT_LEVEL["INFO"],
    }
    match event:
        case "deletion successful":
            log_obj["message"] = "admin successfully deleted user."
        case "deletion problem":
            log_obj["message"] = "there was a problem deleting the user. User might still be in db."
            log_obj["type"] = LOG_EVENT_TYPE["WARN"]
            log_obj["level"] = LOG_EVENT_LEVEL["ERROR"]
        case _:
            log_obj = False
    return log_obj