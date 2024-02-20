from app.utils.log_event_utils.constants import REQUIRED, NONE, LOG_EVENT_TYPE, LOG_EVENT_LEVEL

def contact_form_event(event):
    log_obj = {
        "activity": "contact_form",
        "message": "",
        "user_id": NONE,
        "type": LOG_EVENT_TYPE["INFO"],
        "level": LOG_EVENT_LEVEL["INFO"],
    }
    match event:
        case "message successful":
            log_obj["message"] = "contact form message successfully submitted."
        case "schema validation failure":
            log_obj["message"] = "message rejected: schema validation failure."
        case "html detected":
            log_obj["message"] = "html might have been supplied in form."
            log_obj["type"] = LOG_EVENT_TYPE["SUSPISCIOUS"]
        case "profanity":
            log_obj["message"] = "possible use of profanity in input."
            log_obj["type"] = LOG_EVENT_TYPE["WARN"]
        case "message failed":
            log_obj["message"] = "message rejected: message could not be saved."
            log_obj["type"] = LOG_EVENT_TYPE["WARN"]
            log_obj["level"] = LOG_EVENT_LEVEL["ERROR"]
        case _:
            log_obj = False
    return log_obj