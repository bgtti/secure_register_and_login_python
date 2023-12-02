from flask import current_app
from app.extensions import db, flask_bcrypt
from app.models.user import User
from app.account.salt import generate_salt

# Creates an admin account
# At this point the admin account is just like any other account

# Data for Admin Account creation:
ADMIN_NAME = "Super Admin"
ADMIN_EMAIL = "super@admin"
ADMIN_PW = "admin123"

# TODO: check that admin password is of decent size and content

def create_admin_acct():
    # Check if Super Admin exists in the database, if not, add it:
    super_admin_exists = User.query.get(1)
    if not super_admin_exists:
        # create super admin
        salt = generate_salt()
        pepper = "Pepper"
        salted_pw = pepper + ADMIN_PW + salt
        hashed_password = flask_bcrypt.generate_password_hash(salted_pw).decode('utf-8')
        the_super_admin = User(
            name=ADMIN_NAME, email=ADMIN_EMAIL, password=hashed_password, salt=salt, pepper=pepper)
        db.session.add(the_super_admin)
        db.session.commit()