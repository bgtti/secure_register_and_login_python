import os
from dotenv import load_dotenv  # getting .env variables
import redis
import datetime
from app.utils.rate_limit_utils.rate_limit_exceeded import rate_limit_exceeded
from app.config_constants import pepper_array, secret_key, admin_credentials

load_dotenv()

# *** SETTINGS CONSTANTS
PEPPER_STRING_ARRAY = pepper_array(os.getenv('PEPPER'))
SECRET = secret_key(os.getenv('SECRET_KEY'))
ADMIN_ACCT = admin_credentials(os.getenv('ADMIN_CREDENTIALS'))

# *** BASE CONFIGURATION: used in development
class Config:
    PEPPER = PEPPER_STRING_ARRAY # used in account module when handling passwords
    SECRET_KEY = SECRET # used to protect user session data in flask
    ADMIN_CREDENTIALS = ADMIN_ACCT # used to create admin user

    # SQLAlchemy configuration 
    SQLALCHEMY_DATABASE_URI = "sqlite:///admin.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Flask-Session configuration
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True 
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None" 
    SESSION_COOKIE_NAME = "_SD_session"
    SESSION_KEY_PREFIX = "SDsession:"
    SESSION_REDIS = redis.Redis(host="localhost", port=6379, db=0)

    # Flask-Limiter
    RATELIMIT_STORAGE_URI = "redis://localhost:6379/1"
    RATELIMIT_STORAGE_OPTIONS = {}
    RATELIMIT_STRATEGY = "fixed-window"
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_DEFAULT = "200/day;60/hour"
    RATELIMIT_ON_BREACH_CALLBACK = rate_limit_exceeded

# *** TESTS' CONFIGURATION: used to create app in the tests module
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

# *** PRODUCTION CONFIGURATION: set in manage.py when environment is production
ENV_REDIS_SESSION_HOST = os.getenv('REDIS_SESSION_HOST')
ENV_REDIS_SESSION_PORT = os.getenv('REDIS_SESSION_PORT')
ENV_RATELIMIT_STORAGE_URI = os.getenv('RATELIMIT_STORAGE_URI')

class ProductionConfig(Config):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///admin.db"
    # SESSION_COOKIE_HTTPONLY=True, ---cookie cannot be read using js
    SESSION_REDIS = redis.Redis(host=ENV_REDIS_SESSION_HOST, port=ENV_REDIS_SESSION_PORT, db=0)
    SESSION_COOKIE_SAMESITE = "Lax" 
    RATELIMIT_STORAGE_URI = ENV_RATELIMIT_STORAGE_URI

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

