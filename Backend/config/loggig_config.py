"""
**ABOUT THIS FILE**

logging_config.py contains the information necessary to configure the logger

**LOGGING_CONFIG** is a dictionary that should be imported into the configuration class to configure the logger.

**custom_log_namer** is the function that should be imported in the create_app() to customize the name of the log files.

---------------

Ideally:
- a new log file should be created at midnight, and the previous day's log file will be renamed with a timestamp, effectively creating a new log file for each day.

The log rotation is still buggy, though
"""
import os
from datetime import datetime

#TODO: fix log rotation and log naming issues

# Previous file naming used:
# today = datetime.datetime.today()
# filename = f"{today.year}_{today.month:02d}_{today.day:02d}{LOG_FILE_NAME}.txt"

LOG_FILE_NAME = "log"
filename = f"{LOG_FILE_NAME}.txt"
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "app", "system_logs", filename)

# Define the custom namer function #---> this is an attempt to solve the log rotation issue at midnight
# see: https://docs.python.org/3/library/logging.handlers.html
# Did not solve the rotation issue though

def custom_log_namer(default_name):
    """
    Appends the current date to a log file's default name.

    This function takes a default log file name, extracts the base name and extension, 
    and appends the current date (formatted as YYYY-MM-DD) between them. This modified 
    file name can be used with logging handlers to create uniquely named log files daily.
    (import it to app/__init__.py).

    **Arguments**:
        default_name (str): The default name of the log file, including its extension.

    **Returns**:
        str: The modified log file name with the current date appended before the extension.

    **Example:**
        >>> custom_namer("log.txt")
        'log_2024-11-10.txt'
    """
    base, ext = os.path.splitext(default_name)
    date_str = datetime.now().strftime('%Y-%m-%d')  # Ensures consistent date format
    return f"{base}_{date_str}{ext}"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s: %(levelname)-8s [@ %(module)s | %(funcName)s | %(lineno)d | log: %(name)s] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_FILE_PATH,
            "when": "midnight", # Rotate at midnight. !! => replace with "s" to speed up and test
            "interval": 1, # Rotate daily. !! => replace with "10" to speed up and test
            "backupCount": 90,  # Logs will be kept for 90 days.
            "encoding": "utf-8",
            "delay": True, # Consider setting delay to True to to allow any other processes writing to the log file to finish and release their references
            "formatter": "standard",
        },
        "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                # "formatter": "standard",
            },
    },
    "root": {
            'level': 'DEBUG',
            'handlers': ['file', 'console'],
        },
    "loggers": {
        "": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

