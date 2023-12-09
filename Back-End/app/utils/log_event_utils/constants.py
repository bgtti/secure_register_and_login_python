from app.utils.log_event_utils.log_event_block_unblock import LOG_EVENT_BLOCK, LOG_EVENT_UNBLOCK
from app.utils.log_event_utils.log_event_login import LOG_EVENT_LOGIN
from app.utils.log_event_utils.log_event_signup import LOG_EVENT_SIGNUP

# CREATING NEW LOG ACTIVITIES (event types)
# 01: place the name of the activity (compatible with the name of the route you want to log) in the LOG_EVENT_ACTIVITY
# 02: create a file named log_event + activity. Create the dictionary of dictionaries like in log_event_login.py
# 03: adapt the LOG_EVENT_ACTIVITIES bellow to include the new activity dictionary
# the function to create logs is in helpers.py and should adapt to the new activity type
# it is suggested that the constants bellow be used whenever possible to avoid typos
# DO NOT MIX UP LOG_EVENT_ACTIVITIES with LOG_EVENT_ACTIVITY in the imports...

# EVENT LOGS VERSUS OTHER LOGS:
# event logs are saved to an SQL database. These are easy to view and work with, but database errors happen.
# this is why activity events are logged to the database but another logging system is used to log... well, the system and its errors.
# keep this in mind when creating a new log_event
# log_events are displayed to admins in the FE in the form of user's history and can help flag suspiscious behaviour or answering user's question on why they are encountering some issue (admins can check the activity the user was performing when the error happened)
# do not track sensitive information in log_events or any other type of logging mechanism

LOG_EVENT_ACTIVITIES = {
    "LOG_EVENT_BLOCK": LOG_EVENT_BLOCK,
    "LOG_EVENT_UNBLOCK": LOG_EVENT_UNBLOCK,
    "LOG_EVENT_LOGIN": LOG_EVENT_LOGIN,
    "LOG_EVENT_SIGNUP": LOG_EVENT_SIGNUP 
}

LOG_EVENT_ACTIVITY = {
    "block": "block",
    "unblock":"unblock",
    "signup":"signup",
    "login": "login"
}

# session_id should be either required or not. Use the following constants:
REQUIRED = "REQUIRED"
NONE = "none"

# types are self-defined log levels
LOG_EVENT_TYPE = {
    "INFO": "INFO",
    "WARN": "WARN",
    "SUSPISCIOUS":"SUSPISCIOUS"
}

# levels are compatible with the types used in python logging
LOG_EVENT_LEVEL = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0
}

# Need a refresher in the predefined levels in the logging module?
# DEBUG: Detailed information, typically used for debugging purposes.
# INFO: General information about the program's execution.
# WARNING: Indicates a potential issue that doesn't prevent the program from running but might require attention.
# ERROR: Indicates a more serious issue that prevented a specific operation from completing.
# CRITICAL: Indicates a critical error that may lead to the program's termination.