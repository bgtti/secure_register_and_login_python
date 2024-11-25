"""
**ABOUT THIS FILE**

config_base.py contains the **BaseConfig** class, upon which other classes may be built.

------------------------

More information on how to handle configuration is available in the flask docs: https://flask.palletsprojects.com/en/3.0.x/config/

"""
from datetime import timedelta
from config.rate_limit_config import rate_limit_exceeded
from config.values import SECRET_KEY, SUPER_USER, EMAIL_CREDENTIALS, PEPPER, BASE_URLS


# *** BASE CONFIGURATION: other classes derive from this one
class BaseConfig:
    BASE_URL = BASE_URLS["backend"]

    # App credentials configuration
    PEPPER = PEPPER # used in account module when handling passwords
    SECRET_KEY = SECRET_KEY # used to protect user session data in flask
    ADMIN_CREDENTIALS = SUPER_USER # used to create admin user

    # Flask-Mail Config
    MAIL_SERVER = "smtp.gmail.com" # consider using mailtrap for testing?
    MAIL_PORT = 465
    MAIL_USERNAME = EMAIL_CREDENTIALS["email_address"]
    MAIL_PASSWORD = EMAIL_CREDENTIALS["email_password"]
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # SQLAlchemy/Database Config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Flask-Session & Redis Config
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = True # set to False later ---> ?
    PERMANENT_SESSION_LIFETIME = timedelta(days=1) #comment out later later ---> ?
    SESSION_USE_SIGNER = True 
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None" 
    SESSION_COOKIE_NAME = "_SD_session" # ---> TODO
    SESSION_KEY_PREFIX = "SDsession:" # ---> TODO

    # Flask-Limiter Config
    RATELIMIT_STORAGE_OPTIONS = {}
    RATELIMIT_STRATEGY = "fixed-window"
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_DEFAULT = "200/day;60/hour"
    RATELIMIT_ON_BREACH_CALLBACK = rate_limit_exceeded

