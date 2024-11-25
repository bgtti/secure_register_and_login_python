"""
**ABOUT THIS FILE**

config_dev.py contains the **DevelopmentConfig** class, used to configure the application for local development. 

DevelopmentConfig was created on top of *BaseConfig*, the class from config_base.py.

"""
import redis
from config.config_base import BaseConfig
from config.loggig_config import LOGGING_CONFIG as BASE_LOGGING_CONFIG

class DevelopmentConfig(BaseConfig):

    # Flask Config
    DEBUG = True

    # Flask-Session & Redis Config
    SESSION_REDIS = redis.Redis(host="localhost", port=6379, db=0) 

    # SQLAlchemy/Database Config
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"

    # Flask-Limiter Config
    RATELIMIT_STORAGE_URI = "redis://localhost:6379/1" 
    RATELIMIT_ENABLED = False # Rate limiter disabled

    LOGGING_CONFIG = BASE_LOGGING_CONFIG

