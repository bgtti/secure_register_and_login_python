# from enum import Enum
import enum
import logging
from random import randint
from flask_login import UserMixin
import ast
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from sqlalchemy import Enum
from app.extensions import db
from app.config import ADMIN_ACCT, USER_ID_SALT
from app.utils.constants.account_constants import INPUT_LENGTH
from app.utils.constants.enum_class import modelBool, UserAccessLevel, UserFlag

ADMIN_DATA = ast.literal_eval(ADMIN_ACCT)
ADMIN_PW = ADMIN_DATA[2]


def get_uuid():
    return uuid4().hex



# Notes:
# - Bcrypt should output a 60-character string, so this was used as maximum password length
# - User blockage: the user can be blocked from accessing the account by an admin by setting is_blocked to true.
# - The user can also be temporarily blocked for failing to log in too many times, where login_blocked will be set to true. 
# - booleans ("true"/"false") should not be strings or booleans, but Enums of modelBool
# - is_blocked and login_blocked should not be set directly (user.is_blocked = ...) but rather a method should be used. Do not attempt to set login_blocked directly, as this is done by keeping a counter of wrong login attempts. 
# - access_level should be either "user" or "admin". Change access_level using make_user_admin. The access_level "super admin" exists, but there should be only 1 user with this access.
# - access_level should be defined as Enums in UserAccessLevel. There is no need to change access_level directly (user.access_level = ...), rather a method should be called.

class User(db.Model, UserMixin):
    """
    User db model.
    --------------------------------------------------------------
    Unique identifiers:
    Id used in internal queries only: do not share raw id in APIs. 
    Uuid is used as the identifier sent in APIs.
    Session is the identifier which can be changed (when expiring a session).
    --------------------------------------------------------------
    User blocking: 
    a user can block him/herself temporarily by typing the wrong password a certain number of times. This will result in login_blocked = "true". A user can also be blocked by an admin, when the admin sets is_blocked="true". Neither value should be set directly, but with the use of methods. Checking the block status should also be done using methods.
    --------------------------------------------------------------
    Example usage: adding user

    from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper
    from app.extensions import db, flask_bcrypt
    from app.models.user import User

    date = datetime.utcnow()
    salt = generate_salt()
    pepper = get_pepper(date)
    salted_password = salt + "somepsswrd" + pepper
    hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')
    user = User(
        name="josy", 
        email="josy@j.com, 
        password=hashed_password, 
        salt=salt
        )
        db.session.add(user)
        db.session.commit() 
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    uuid = db.Column(db.String(32), unique=True, default=get_uuid)
    session = db.Column(db.String(32), nullable=False, default=get_uuid)
    remember_me = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False)
    name = db.Column(db.String(INPUT_LENGTH['name']['maxValue']), nullable=False)
    email = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    salt = db.Column(db.String(8), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    last_seen = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    access_level = db.Column(db.Enum(UserAccessLevel), default=UserAccessLevel.USER, nullable=False)
    flagged = db.Column(db.Enum(UserFlag), default=UserFlag.BLUE, nullable=False)
    is_blocked = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False)
    login_attempts = db.Column(db.Integer, default=0)
    last_login_attempt = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    login_blocked = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False)
    login_blocked_until = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    def __init__(self, name, email, password, salt, created_at, **kwargs):
        self.name = name
        self.email = email
        self.password = password
        self.salt = salt
        self.created_at = created_at
    
    def __repr__(self):
        return f"<User: {self.id} {self.name} {self.email}>"
    
    def new_session(self):
        new_session_id = get_uuid()
        self.session = new_session_id
        return self.session 
    
    # def end_session(self):
    #     self._session = ""

    def should_be_remembered(self):
        """
        should_be_remembered()-> bool
        -----------------------------
        Returns a boolean indicated whether user wants to be remembered or whether the session should expire when browser closes.
        """
        return self.remember_me == modelBool.TRUE

    # used by flask_login to get a session id
    def get_id(self):
        """
        get_id() -> str
        ----------------------------
        Used by the login manager from flask_login to create a session cookie.
        """
        if self.should_be_remembered():
            return self.session
        else:
            return str(self.id)
    
    def increment_login_attempts(self):
        """
        user.increment_login_attempts()-> void
        ----------------------------
        Should be called when user types an incorrect password.
        This will keep the counter of failed log-in attempts and temporarily block the user if necessary.
        """
        self.login_attempts += 1
        self.last_login_attempt = datetime.now(timezone.utc)
        if self.login_attempts == 3:
            self.login_blocked = modelBool.TRUE
            self.login_blocked_until = datetime.now(timezone.utc) + timedelta(minutes=1)
        elif self.login_attempts == 5:
            self.login_blocked_until = datetime.now(timezone.utc) +timedelta(minutes=2)
        elif self.login_attempts > 5:
            self.login_blocked_until = datetime.now(timezone.utc) + timedelta(minutes=5)

    def reset_login_attempts(self):
        """
        user.reset_login_attempts()-> void
        ----------------------------
        Should be called when user types the correct password loging in.
        This ensures the user failed login attempt count is set to 0.
        """
        self.login_attempts = 0
        self.last_login_attempt = datetime.now(timezone.utc)
        self.login_blocked_until = datetime.now(timezone.utc)
        self.login_blocked = modelBool.FALSE

    def is_login_blocked(self):
        """
        user.is_login_blocked()-> bool
        ----------------------------
        Called to check if the user has been temporarily blocked for typing the wrong password.
        """
        return self.login_blocked == modelBool.TRUE and self.login_blocked_until > datetime.now(timezone.utc)
    
    def has_access_blocked(self):
        """
        user.has_access_blocked()-> bool
        ----------------------------
        Called to check if the user has been blocked by an admin.
        """
        return self.is_blocked == modelBool.TRUE 
    
    def block_access(self):
        """
        user.block_access()-> void
        ----------------------------
        The user's access will be blocked.
        Should be called by super admin or admins only.
        The super admin cannot be blocked.
        """
        if self.access_level == UserAccessLevel.SUPER_ADMIN:
            raise ValueError("Super admin cannot be blocked.")
        self.is_blocked = modelBool.TRUE 
    
    def unblock_access(self):
        """
        user.unblock_access()-> void
        ----------------------------
        The user's access will be unblocked.
        Should be called by super admin or admins only.
        """
        self.is_blocked = modelBool.FALSE 

    def make_user_admin(self):
        """
        user.make_user_admin() -> void
        -------------------------------
        Method will change the user's access_level.
        Make sure only the super admin calls this method on other users.
        """
        self.access_level = UserAccessLevel.ADMIN
    
    def make_user_super_admin(self, admin_password):
        """
        user.make_user_super_admin(admin_password: str) -> void
        ----------------------------------------------------------
        Method makes user a super admin. There should only be one super admin in the table.
        Since the idea is to call it only once (as the super admin is the first user created),
        it required the admin password defined in the app's config.
        """
        if self.access_level != 1:
            existing_super_admins = User.query.filter_by(access_level=UserAccessLevel.SUPER_ADMIN).count()
            if existing_super_admins == 0 and admin_password == ADMIN_PW:
                self.access_level = UserAccessLevel.SUPER_ADMIN

    
    def serialize_user_table(self):
        """
        Returns a dictionary with  base user information.
        Call when a list of user dictionaries is needed.
        Should be called in admin routes only.
        ------------------------------------------------
        Example usage:
        "users": [user.serialize_user_table() for user in users.items if user.access_level != 1]
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "last_seen": self.last_seen,
            "is_blocked": self.is_blocked.value,
        }
    def flag_change(self, flag_colour):
        """
        Changes the user flag to the appropriate colour.
        Accepts the colour as an argument: choices accepted are those in UserFlag Enum: red, yellow, purple, and blue.
        The argument flag_colour must be a string - upper or lower case.
        ------------------------------------------------
        Example usage:
        user.flag_change("blue")
        """
        flag_colour = flag_colour.upper()
        flags = [member.name for member in UserFlag]
        if flag_colour in flags:
            self.flagged = UserFlag[flag_colour].value
        else:
            logging.error(f"User flag could not be changed: wrong input for flag_change: {flag_colour}. Check UserFlag Enum for options.")
            print("Error: flag color not found. User's flagged status not changed.")
