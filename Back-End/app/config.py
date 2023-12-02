import os
from dotenv import load_dotenv  # getting .env variables


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') #used to protect user session data in flask
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')  # needed for jwf 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///admin.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False