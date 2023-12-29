from flask import current_app
import ast
from datetime import datetime
from app.config import ADMIN_ACCT
from app.extensions import db, flask_bcrypt
from app.models.user import User
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper

# Data for Admin Account creation:
ADMIN_DATA = ast.literal_eval(ADMIN_ACCT)
ADMIN_NAME = ADMIN_DATA[0]
ADMIN_EMAIL = ADMIN_DATA[1]
ADMIN_PW = ADMIN_DATA[2]

# TODO: check that admin password is of decent size and content

def create_admin_acct():
    # Check if Super Admin exists in the database, if not, add it:
    super_admin_exists = User.query.get(1)
    if not super_admin_exists:
        date = datetime.utcnow()
        salt = generate_salt()
        pepper = get_pepper(date)
        salted_password = salt + ADMIN_PW + pepper
        hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')
        the_super_admin = User(
            name=ADMIN_NAME, email=ADMIN_EMAIL, password=hashed_password, salt=salt, created_at=date)
        db.session.add(the_super_admin)
        the_super_admin.make_user_admin(ADMIN_PW)
        db.session.commit()