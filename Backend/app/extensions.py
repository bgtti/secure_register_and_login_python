from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session
from flask_login import LoginManager
from sqids import Sqids
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from faker import Faker
from flask_mail import Mail


db = SQLAlchemy()
flask_bcrypt = Bcrypt()
cors = CORS()
# server_session = Session()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)
sqids = Sqids(min_length=8)
faker = Faker()
mail = Mail()
