from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flask_httpauth import HTTPBasicAuth #check if necessary
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_session import Session


db = SQLAlchemy()
flask_bcrypt = Bcrypt()
jwt = JWTManager() #maybe disuse
cors = CORS()
server_session = Session()
