"""
**ABOUT THIS FILE**

config_prod.py contains the **ProductionConfig** class, used to configure the application for the production environment. 

"""

#TODO: ProductionConfig is still under construction

import os
import redis
from config.config_base import BaseConfig

ENV_REDIS_SESSION_HOST = os.getenv('REDIS_SESSION_HOST')
ENV_REDIS_SESSION_PORT = os.getenv('REDIS_SESSION_PORT')
ENV_RATELIMIT_STORAGE_URI = os.getenv('RATELIMIT_STORAGE_URI')

class ProductionConfig(BaseConfig):

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///prod.db" #---> TODO
    TESTING = False #---> ??

    # Session cookies //=> Redis
    # SESSION_COOKIE_HTTPONLY=True, ---cookie cannot be read using js, default is true
    SESSION_REDIS = redis.Redis(host=ENV_REDIS_SESSION_HOST, port=ENV_REDIS_SESSION_PORT, db=0, password= 'your_redis_password')
    SESSION_COOKIE_SAMESITE = "Lax" 
    SESSION_COOKIE_SECURE = True

    # Flask rate limiter
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URI = ENV_RATELIMIT_STORAGE_URI

    LOGGING_CONFIG = {
        # Dev-specific logging config
    }