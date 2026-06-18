"""
**ABOUT THIS FILE**

scripts/setup.py contains:
- create_super_admin_acct: function that creates a user with the role of super_admin.
- check_redis: a function that checks if Redis is running, without it the app may not function properly.
- initial_setup: calls the function to create the super_admin and check_redis. Thi function is called in manage.py, the entry point of the application.

This file sets up the application by creating a super admin and creating the roles (which define site permissions). More information about roles and user creation, please check: app/models/role.py and user.py.

Note that when not in production environment, the script will also seed the database with dummy data for testing purposes. 
More about dummie data in the seeds module.
"""

import redis
from datetime import datetime, timezone
from utils.print_to_terminal import print_to_terminal
from config.values import SUPER_USER
from seeds.seed_all import seed_database
from app.extensions.extensions import db, flask_bcrypt
from app.models.user import User
from app.models.role import Role
from app.common.salt_and_pepper.helpers import generate_salt, get_pepper

# Creating Super Admin Account
def create_super_admin_acct():
    """
    This function creates the super admin account.
    There can only be one super_admin, and this user has the most permissions in the app.
    You can configure it's name, email, and password in your env file.
    The function is called once by the initial_setup function in scripts/setup.py .
    """
    # Check if Super Admin exists in the database, if not, add it:
    super_admin_exists = db.session.query(User).first() is not None
    if not super_admin_exists:
        print_to_terminal("Creating super admin user...", "CYAN")
        date = datetime.now(timezone.utc)
        salt = generate_salt()
        pepper = get_pepper(date)
        salted_password = salt + SUPER_USER["password"] + pepper
        hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')
        the_super_admin = User(
            name=SUPER_USER["name"], 
            email=SUPER_USER["email"], 
            password=hashed_password, 
            salt=salt, 
            created_at=date
            )
        db.session.add(the_super_admin)
        the_super_admin.make_user_super_admin(SUPER_USER["password"])
        db.session.commit()
        print_to_terminal("...super admin user successfully added!", "CYAN")

# Checking if Redis is running: this is important for flask session to work
def check_redis():
    """
    This function checks if Redis is running.
    -----------------------------------------
    In case it is not running, it will log the information to the terminal in red.
    In case it is running, the terminal log will be displayed in blue.
    """
    try:
        r = redis.Redis(host="localhost", port=6379, db=0)
        r.ping()  # Ping Redis to check if it's running
    except redis.ConnectionError:
        print_to_terminal("Failed to connect to Redis:", "RED")
        print_to_terminal("Flask session relies on Redis to authenticate users. The app may not function correctly.", "MAGENTA")

# Setting up the app
def initial_setup(environment):
    """
    initial_setup(environment: str) -> None
    ----------------------------------------

    Pass the environment to initial_setup (exemple: "development" or "production") for the script to run accordingly.

    The function will create the super admin account. In case this app is not running in production, the script will also seed the database and check whether redis is running.

    This function should be called only once: in *manage.py* after the app has been created and the db has been initiated.
    """
    create_super_admin_acct()
    Role.insert_roles()
    if environment != "production":
        seed_database()
        check_redis()
