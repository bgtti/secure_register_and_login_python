# user_id should be either required or not. Use the following constants:
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