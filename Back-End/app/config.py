import os
from dotenv import load_dotenv  # getting .env variables
import redis
import datetime
from app.utils.rate_limit_utils.rate_limit_exceeded import rate_limit_exceeded

load_dotenv()

# *** APP'S CONFIGURATION ("app")
class Config:
    PEPPER = os.getenv("PEPPER") # used in account module when handling passwords
    SECRET_KEY = os.getenv("SECRET_KEY") # used to protect user session data in flask

    # SQLAlchemy configuration 
    SQLALCHEMY_DATABASE_URI = "sqlite:///admin.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Flask-Session configuration
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True #if set to True, you have to set flask.Flask.secret_key, default to be False
    SESSION_KEY_PREFIX = "session:"
    SESSION_REDIS = redis.Redis(host="localhost", port=6379, db=0)

    # Flask-Limiter
    RATELIMIT_STORAGE_URI = "redis://localhost:6379/1"
    RATELIMIT_STORAGE_OPTIONS = {}
    RATELIMIT_STRATEGY = "fixed-window"
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_DEFAULT = ["200 per day", "60 per hour"]
    RATELIMIT_ON_BREACH_CALLBACK = rate_limit_exceeded

# *** TESTS' CONFIGURATION (tests)
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

# *** LOGGING CONFIGURATION (system_logs)

# A new log file will be created at midnight, and the previous day's log file will be renamed with a timestamp, effectively creating a new log file for each day. 
# Previous file naming used:
# today = datetime.datetime.today()
# filename = f"{today.year}_{today.month:02d}_{today.day:02d}{LOG_FILE_NAME}.txt"

LOG_FILE_NAME = "log"
filename = f"{LOG_FILE_NAME}.txt"
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "system_logs", filename)

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
            "when": "midnight", # A new log file is created at midnight
            "interval": 1, # This specifies that the rotation interval is 1 day
            "backupCount": 90,  # Logs will be kept for 90 days.
            "encoding": "utf-8",
            "delay": False,
            "formatter": "standard",
        },
        "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                # "formatter": "standard",
            },
    },
    'root': {
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

