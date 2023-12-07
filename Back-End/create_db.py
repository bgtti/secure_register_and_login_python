from flask import current_app
from app.extensions import db, flask_bcrypt
from app.models.user import User
from app.account.salt import generate_salt
import os
import ast
from datetime import datetime

# Creates an admin account
# At this point the admin account is just like any other account

PEPPER_STRING_ARRAY = os.getenv('PEPPER') 
PEPPER_ARRAY = ast.literal_eval(PEPPER_STRING_ARRAY)

# Data for Admin Account creation:
ADMIN_NAME = "Super Admin"
ADMIN_EMAIL = "super@admin"
ADMIN_PW = "lad678Ut$G"

# TODO: check that admin password is of decent size and content

def create_admin_acct():
    # Check if Super Admin exists in the database, if not, add it:
    super_admin_exists = User.query.get(1)
    if not super_admin_exists:
        # create super admin
        date = datetime.utcnow()
        pepper = PEPPER_ARRAY[(date.month -1) % len(PEPPER_ARRAY)]
        salt = generate_salt()
        salted_password = salt + ADMIN_PW + pepper
        hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')
        the_super_admin = User(
            name=ADMIN_NAME, email=ADMIN_EMAIL, password=hashed_password, salt=salt, created_at=date)
        db.session.add(the_super_admin)
        db.session.commit()