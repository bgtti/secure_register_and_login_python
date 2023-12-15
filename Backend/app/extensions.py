from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


db = SQLAlchemy()
flask_bcrypt = Bcrypt()
cors = CORS()
server_session = Session()
limiter = Limiter(key_func=get_remote_address)
