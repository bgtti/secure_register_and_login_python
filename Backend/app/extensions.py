from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_mail import Mail
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from sqids import Sqids

# The extensions bellow are used in the __init__ file, where the app is created.

db = SQLAlchemy()
cors = CORS()
faker = Faker()
flask_bcrypt = Bcrypt()
limiter = Limiter(key_func=get_remote_address)
login_manager = LoginManager()#info here
mail = Mail()
server_session = Session() #Session Middleware. Without it, Flask defaults to client-side cookies
sqids = Sqids(min_length=8)