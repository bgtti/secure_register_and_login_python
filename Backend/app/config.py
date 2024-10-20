import os
from dotenv import load_dotenv  # getting .env variables
import redis
# import datetime
import json
from datetime import timedelta
from enum import Enum
from app.utils.rate_limit_utils.rate_limit_exceeded import rate_limit_exceeded
from app.config_constants import pepper_array, secret_key, admin_credentials, user_id_salt, email_credentials

load_dotenv()

# *** SETTINGS CONSTANTS
PEPPER_STRING_ARRAY = pepper_array(os.getenv('PEPPER'))
SECRET = secret_key(os.getenv('SECRET_KEY'))
ADMIN_ACCT = admin_credentials(os.getenv('ADMIN_CREDENTIALS'))
USER_ID_SALT = user_id_salt(os.getenv('USER_ID_SALT'))
EMAIL_CREDENTIALS = email_credentials(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))

# *** BASE CONFIGURATION: used in development
class Config:

    # App credentials configuration
    PEPPER = PEPPER_STRING_ARRAY # used in account module when handling passwords
    SECRET_KEY = SECRET # used to protect user session data in flask
    ADMIN_CREDENTIALS = ADMIN_ACCT # used to create admin user

    # Email credential configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = EMAIL_CREDENTIALS["email_address"]
    MAIL_PASSWORD = EMAIL_CREDENTIALS["email_password"]
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # SQLAlchemy configuration 
    SQLALCHEMY_DATABASE_URI = "sqlite:///admin.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Flask-Session configuration
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = True # set to False later
    PERMANENT_SESSION_LIFETIME = timedelta(days=1) #comment out later
    # SESSION_PERMANENT = False
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
    RATELIMIT_ENABLED = False # rate limiter disabled in development

# *** TESTS' CONFIGURATION: used to create app in the tests module
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # Disable Flask-Limiter for tests
    RATELIMIT_ENABLED = False
    RATELIMIT_STORAGE_OPTIONS = {}  # Empty storage options for testing
    RATELIMIT_DEFAULT = "1000/day"  # Adjust this rate limit as needed for your tests

# *** PRODUCTION CONFIGURATION: set in manage.py when environment is production
ENV_REDIS_SESSION_HOST = os.getenv('REDIS_SESSION_HOST')
ENV_REDIS_SESSION_PORT = os.getenv('REDIS_SESSION_PORT')
ENV_RATELIMIT_STORAGE_URI = os.getenv('RATELIMIT_STORAGE_URI')

class ProductionConfig(Config):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///admin.db"
    # SESSION_COOKIE_HTTPONLY=True, ---cookie cannot be read using js
    SESSION_REDIS = redis.Redis(host=ENV_REDIS_SESSION_HOST, port=ENV_REDIS_SESSION_PORT, db=0, password= 'your_redis_password')
    SESSION_COOKIE_SAMESITE = "Lax" 
    RATELIMIT_STORAGE_URI = ENV_RATELIMIT_STORAGE_URI
    RATELIMIT_ENABLED = True

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

