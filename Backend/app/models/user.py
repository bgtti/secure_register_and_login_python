# from enum import Enum
import ast
import enum
import logging
from datetime import datetime, timedelta, timezone
from flask_login import UserMixin
from uuid import uuid4
import secrets
from random import randint
from sqlalchemy import Enum
from utils.print_to_terminal import print_to_terminal
from config.values import SUPER_USER
from app.extensions.extensions import db
from app.utils.constants.account_constants import INPUT_LENGTH
from app.utils.constants.enum_class import modelBool, UserAccessLevel, UserFlag
from app.utils.constants.enum_helpers import map_string_to_enum

ADMIN_PW = SUPER_USER["password"]

def get_session_id(user_id=0):
    random_number = secrets.randbelow(90000000) + 10000000  # 8-digit number

    # as a user is created, a session id should be generated using the model's method
    # however, in the case this step is forgotten ( or in the case the database is being seeded with some fake test users), a random number will be assigned
    if user_id == 0:
        use_random = secrets.randbelow(90000000) + 10000000  # another 8-digit number
        return f"0{use_random}-{random_number}"
    
    return f"{user_id}-{random_number}"

def get_six_digit_code(): # TODO: check owasp oppinion on one-time passwords: https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html#email
    # Generate a secure random integer between 100000 and 999999
    return secrets.randbelow(900000) + 100000  # Ensures a 6-digit number

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
    # TABLE
    id = db.Column(db.Integer, primary_key=True, unique=True)
    session = db.Column(db.String(50), nullable=False, default=get_session_id) # used by the login manager to get the user
    remember_me = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False) #TODO: implement
    name = db.Column(db.String(INPUT_LENGTH['name']['maxValue']), nullable=False)
    # auth:
    email = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    salt = db.Column(db.String(8), nullable=False)
    # one time password (otp):
    otp_token = db.Column(db.String(6), nullable=True)
    otp_token_creation = db.Column(db.DateTime, nullable=True)
    # acct:
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    email_is_verified = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False)
    # access:
    access_level = db.Column(db.Enum(UserAccessLevel), default=UserAccessLevel.USER, nullable=False)
    is_blocked = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False)
    # activity:
    flagged = db.Column(db.Enum(UserFlag), default=UserFlag.BLUE, nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    login_attempts = db.Column(db.Integer, default=0)
    last_login_attempt = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    login_blocked = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False)
    login_blocked_until = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    # auth credential change or verification:
    new_email = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), nullable=True, unique=True)
    token = db.relationship("Token", backref="user", lazy="select", cascade="all, delete-orphan")
    # preferences
    mfa_enabled = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False) # multi-factor authentication
    in_mailing_list = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False) 
    night_mode_enabled = db.Column(db.Enum(modelBool), default=modelBool.TRUE, nullable=False) 
    
    # METHODS
    def __init__(self, name, email, password, salt, created_at, **kwargs):
        self.name = name
        self.email = email
        self.password = password
        self.salt = salt
        self.created_at = created_at
    
    def __repr__(self):
        return f"<User: {self.id} {self.name} {self.email}>"

    def should_be_remembered(self) -> bool:
        """ TODO:
        This method checks the `remember_me` attribute to decide if the user's session should persist
        beyond the current browser session or expire when the browser is closed.

        Returns:
            bool: True if the user wants to be remembered (persistent session), False otherwise.
        """
        return self.remember_me == modelBool.TRUE
    
    # used in routes to invalidate active sessions
    def new_session(self) -> str:
        """
        Generates a new session ID for the user.

        This method should be called immediately after a user is created or when a session reset is required.
        It generates a new session ID using the `get_session_id` function, associating it with the user's ID.
        Any previously active user sessions will be invalidated, requiring the user to log in again.

        Returns:
            str: The newly generated session ID.
        """
        self.session = get_session_id(self.id)
        return self.session 

    # used by flask_login to get a session id
    def get_id(self) -> str:
        """
        Retrieves the user's unique identifier ("session").

        This method is used by Flask-Login's `LoginManager` to associate a user with 
        a session. The returned identifier is stored in the session cookie.

        Returns:
            str: The unique identifier for the user. This should typically be the 
        """
        return self.session
    
    def generate_otp(self) -> str:
        """
        Generates an OTP, saves it to the user's `otp_token` along with the current timestamp in UTC
        (`otp_token_creation`), and returns the generated OTP.

        Returns:
            str: The generated OTP as a string.
        
        Example:
            otp = user.generate_otp()
            print(f"Generated OTP: {otp}")
        """
        new_otp = get_six_digit_code()
        self.otp_token = new_otp
        self.otp_token_creation = datetime.now(timezone.utc)
        return new_otp
    
    def increment_login_attempts(self) -> None:
        """
        Increments the counter for failed login attempts.

        This method should be called when the user enters an incorrect password.
        If the failed attempts exceed the maximum allowed, the user is temporarily blocked.
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

    def reset_login_attempts(self) -> None:
        """
        Resets the user's failed login attempt count to 0.

        This method should be called when the user successfully logs in with the correct password.
        It ensures the failed login attempt count is cleared, preventing lockouts for successful logins.
        """
        self.login_attempts = 0
        self.last_login_attempt = datetime.now(timezone.utc)
        self.login_blocked_until = datetime.now(timezone.utc)
        self.login_blocked = modelBool.FALSE

    def is_login_blocked(self) -> bool:
        """
        Checks if the user is temporarily blocked due to exceeding failed login attempts.

        Returns:
            bool: True if the user is blocked, False otherwise.
        """
        return self.login_blocked == modelBool.TRUE and self.login_blocked_until > datetime.now(timezone.utc)
    
    def has_access_blocked(self) -> bool:
        """
        Checks if the user has been blocked by an admin.

        Returns:
            bool: True if the user has been blocked by an admin, False otherwise.
        """
        return self.is_blocked == modelBool.TRUE 
    
    def block_access(self) -> None:
        """
        Blocks the user's access.

        This method should be called by a super admin or admin only. 
        It ensures that a super admin cannot be blocked.

        Raises:
            ValueError: If attempting to block a super admin.
        """
        if self.access_level == UserAccessLevel.SUPER_ADMIN:
            raise ValueError("Super admin cannot be blocked.")
        self.is_blocked = modelBool.TRUE 
    
    def unblock_access(self) -> None:
        """
        Unblocks the user's access.

        This method should be called by a super admin or admin only.
        """
        self.is_blocked = modelBool.FALSE 

    def make_user_admin(self) -> None:
        """
        Promotes the user to an admin role.

        This method changes the user's `access_level` to 'admin'. 
        It should only be called by a super admin..
        """
        self.access_level = UserAccessLevel.ADMIN
    
    def make_user_regular_user(self) -> None:
        """
        Demotes the user to a regular user role.

        This method changes the user's `access_level` to 'user', effectively removing admin rights. 
        Ensure that the method is not called on a super admin!

        Raises:
            ValueError: If the user is already a regular user or a super admin.
        """
        if self.access_level == UserAccessLevel.SUPER_ADMIN.value:
            raise ValueError("Super admin cannot be demoted to a regular user.")
        else:
            self.access_level = UserAccessLevel.USER
    
    def make_user_super_admin(self, admin_password: str) -> None:
        """
        Promotes the user to super admin. There should only be one super admin in the system.
        Since the idea is to call it only once (as the super admin is the first user created),
        it required the admin password defined in the app's config.
        """
        if self.access_level != UserAccessLevel.SUPER_ADMIN:
            existing_super_admins = User.query.filter_by(access_level=UserAccessLevel.SUPER_ADMIN).count()
            if existing_super_admins == 0 and admin_password == ADMIN_PW:
                self.access_level = UserAccessLevel.SUPER_ADMIN
    
    def serialize_user_table(self) -> dict:
        """
        Serializes the user information into a dictionary.

        This method returns a dictionary with basic user information, 
        suitable for use in admin routes or API responses where a list 
        of user data is required.

        Example usage:
            "users": [
                user.serialize_user_table()
                for user in users.items
                if user.access_level != UserAccessLevel.SUPER_ADMIN.value
            ]

        Returns:
            dict: A dictionary containing user information.
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at,
            "last_seen": self.last_seen,
            "access": self.access_level.value,
            "flagged": self.flagged.value,
            "is_blocked": self.is_blocked.value,
        }
    
    def flag_change(self, flag_colour: str) -> None:
        """
        hanges the user's flag to the specified color.

        Accepts a flag color as an argument. Valid choices are those defined in the UserFlag Enum:
        'red', 'yellow', 'purple', and 'blue'. The argument `flag_colour` is case-insensitive.

        Args:
            flag_colour (str): The desired flag color (case-insensitive).

        Example usage:
            `user.flag_change("blue")`
        """
        the_colour = flag_colour.lower()
        flag = map_string_to_enum(the_colour, UserFlag)
        if flag is not None:
            self.flagged = flag
        else:
            logging.error(f"User flag could not be changed: wrong input for flag_change: {flag_colour}. Check UserFlag Enum for options.")
            print_to_terminal("Error (user method flag_change): flag color not found. User's flagged status not changed.", "YELLOW")
    
    def verify_account(self) -> bool:
        """
        Verifies the user's account email.

        This method sets the user's `email_is_verified` attribute to `modelBool.TRUE`, indicating that
        the email verification process is complete. It is important to ensure that a valid 
        `VerificationToken` was successfully validated before calling this method!

        Returns:
            bool: True if the account was successfully verified, False otherwise.

        Example usage:
            `user.verify_account()`
        """
        if self.email_is_verified == modelBool.FALSE:
            self.email_is_verified = modelBool.TRUE
            return True
        else:
            logging.error(f"User account could not be verified. It is possible the account has been verified before. email_is_verified = {self.email_is_verified}. Check User model.")
            return False

    def change_email(self) -> bool:
        """
        Changes the user's account email.

        This method updates the user's email to the value stored in `user.new_email`. 
        It is crucial to ensure that a `VerificationToken` was successfully validated before 
        calling this method to confirm ownership of the new email address.

        Returns:
            bool: True if the email was successfully changed, False otherwise.

        Example usage:
            `user.change_email()`
        """
        if self.new_email is None:
            logging.error("Attempted email change but no new_email stored.")
            return False
        
        self.email = self.new_email 

        if self.access_level == UserAccessLevel.SUPER_ADMIN:
            logging.warning("Super admin account email change.")

        if self.access_level == UserAccessLevel.ADMIN:
            logging.info("Admin account email change.")

        return True
