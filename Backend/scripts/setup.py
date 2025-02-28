import redis
from datetime import datetime, timezone
from utils.print_to_terminal import print_to_terminal
from config.values import SUPER_USER
from seeds.seed_all import seed_database
from app.extensions.extensions import db, flask_bcrypt
from app.models.user import User
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper

# Creating Super Admin Account
def create_super_admin_acct():
    """
    This function creates the super admin account.
    It is called in manage.py.
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

def initial_setup(environment):
    """
    initial_setup(environment: str) -> None
    ----------------------------------------

    Pass the environment to initial_setup (exemple: "development" or "production") for the script to run accordingly.

    The function will create the super admin account. In case this app is not running in production, the script will also seed the database and check whether redis is running.

    This function should be called only once: in *manage.py* after the app has been created and the db has been initiated.
    """
    create_super_admin_acct()
    if environment != "production":
        seed_database()
        check_redis()
