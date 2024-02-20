from app.utils.log_event_utils.constants import REQUIRED, NONE, LOG_EVENT_TYPE, LOG_EVENT_LEVEL

def signup_event(event):
    log_obj = {
        "activity": "signup",
        "message": "",
        "user_id": REQUIRED,
        "type": LOG_EVENT_TYPE["INFO"],
        "level": LOG_EVENT_LEVEL["INFO"],
    }
    match event:
        case "signup successful":
            log_obj["message"] = "successful signup."
        case "schema validation failure":
            log_obj["message"] = "signup rejected: schema validation failure."
            log_obj["user_id"] = NONE
        case "user exists":
            log_obj["message"] = "signup rejected: user already exists."
            log_obj["user_id"] = NONE
        case "weak password":
            log_obj["message"] = "signup rejected: weak password. Frontend validation failed?"
            log_obj["user_id"] = NONE
            log_obj["type"] = LOG_EVENT_TYPE["WARN"]
        case "signup failed":
            log_obj["message"] = "signup rejected: user could not be created"
            log_obj["user_id"] = NONE
            log_obj["type"] = LOG_EVENT_TYPE["WARN"]
            log_obj["level"] = LOG_EVENT_LEVEL["ERROR"]
        case "html detected":
            log_obj["message"] = "html might have been supplied in form."
            log_obj["type"] = LOG_EVENT_TYPE["SUSPISCIOUS"]
        case "profanity":
            log_obj["message"] = "possible use of profanity in input."
            log_obj["type"] = LOG_EVENT_TYPE["WARN"]
        case _:
            log_obj = False
    return log_obj

def login_event(event):
    log_obj = {
        "activity": "login",
        "message": "",
        "user_id": REQUIRED,
        "type": LOG_EVENT_TYPE["INFO"],
        "level": LOG_EVENT_LEVEL["INFO"],
    }
    match event:
        case "login successful":
            log_obj["message"] = "successful login."
        case "schema validation failure":
            log_obj["message"] = "login rejected: schema validation failure."
            log_obj["user_id"] = NONE
        case "user not found":
            log_obj["message"] = "login rejected: user does not exist."
            log_obj["user_id"] = NONE
        case "user blocked":
            log_obj["message"] = "login rejected: user is blocked."
        case "user temporary block":
            log_obj["message"] = "login rejected: user is temporarily blocked."
        case "user temporary block":
            log_obj["message"] = "login rejected: user is temporarily blocked."
        case "wrong credentials 3x":
            log_obj["message"] = "login rejected: wrong password input more than 3 times."
        case "wrong credentials 5x":
            log_obj["message"] = "login rejected: wrong password input 5 times or more."
            log_obj["type"] = LOG_EVENT_TYPE["WARN"]
        case "html detected":
            log_obj["message"] = "html might have been supplied in form."
            log_obj["type"] = LOG_EVENT_TYPE["SUSPISCIOUS"]
        case _:
            log_obj = False
    return log_obj