from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flask_httpauth import HTTPBasicAuth #check if necessary
from flask_jwt_extended import JWTManager
from flask_cors import CORS


db = SQLAlchemy()
flask_bcrypt = Bcrypt()
jwt = JWTManager()
cors = CORS()
