import os
from dotenv import load_dotenv  # getting .env variables
import redis

load_dotenv()

class Config:
    PEPPER = os.getenv('PEPPER')
    SECRET_KEY = os.getenv('SECRET_KEY') #used to protect user session data in flask
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')  # needed for jwf
    # SQLAlchemy configuration 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///admin.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    # Flask-Session configuration
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True #if set to True, you have to set flask.Flask.secret_key, default to be False
    SESSION_KEY_PREFIX = 'session:'
    SESSION_REDIS = redis.Redis(host='localhost', port=6379, db=0)
   
    # SESSION_REDIS = {
    #     'host': 'my-redis-container',  # Change to the hostname or IP where Redis is running, eg: 'localhost'
    #     'port': 6379,
    #     'db': 0,
    #     'password': 'your_redis_password',  # Add this line
    #     'decode_responses': True
    # }

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'