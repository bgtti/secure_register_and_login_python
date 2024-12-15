"""
**ABOUT THIS FILE**

models/user.py contains:

- Constants required for the db model or methods to function
- Helper functions used only in the db model or methods 
- **User** class (the db model)
"""
# from enum import Enum
# import ast
# import enum
# from random import randint
############# IMPORTS ##############

# Python/Flask libraries
import re
import logging
from datetime import datetime, timedelta, timezone

# Extensions and configurations
from flask_login import UserMixin
import secrets
from sqlalchemy import Enum
from utils.print_to_terminal import print_to_terminal
from config.values import SUPER_USER
from app.extensions.extensions import db
from app.extensions.sqlalchemy_config import EncryptedType, UTCDateTime

# Utilities
from app.utils.constants.account_constants import INPUT_LENGTH, OTP_PATTERN
from app.utils.constants.enum_class import modelBool, UserAccessLevel, UserFlag, LoginMethods
from app.utils.constants.enum_helpers import map_string_to_enum

############ CONSTANTS #############
ADMIN_PW = SUPER_USER["password"]
OTP_VALIDITY_MINUTES = 30 #define here the length the OTP should be valid for
MFA_VALIDITY_MINUTES = 30 #define here the length between authenticating the two methods required in mfa

############# HELPERS ##############

def get_eight_digits_number() -> int: 
    """
    Generates a random 8-digit number.

    The function uses `secrets.randbelow` to generate a secure random number between
    10,000,000 (inclusive) and 99,999,999 (inclusive). This ensures the number is
    always exactly 8 digits long.

    Returns:
        int: A secure random 8-digit number.
    
    More info:
        https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/11-Testing_Multi-Factor_Authentication
    """
    return secrets.randbelow(90000000) + 10000000  # Ensures a 6-digit number

def get_session_id(user_id: int = 0) -> str:
    """
    Generates a session ID based on the provided user ID and a random 8-digit number.

    This function creates a session ID in the format `"{user_id}-{random_number}"`. If the `user_id` 
    is not provided or is set to `0`, the session ID will default to the format 
    `"0{use_random}-{random_number}"`, where `use_random` is another randomly generated 8-digit number.

    The user_id may be 0 when seeding the database, for instance.

    It is designed to handle scenarios where:
        - A session ID needs to be generated for a user using the model's method.
        - The database is being seeded with test users, or the session ID step was skipped.

    Args:
        user_id (int): The ID of the user for whom the session ID is being generated. Defaults to `0` if not provided.

    Returns:
        str: A session ID string in the specified format.
    """
    random_number = get_eight_digits_number()  # 8-digit number
    if user_id == 0:
        use_random = get_eight_digits_number()  # another 8-digit number
        return f"0{use_random}-{random_number}"
    
    return f"{user_id}-{random_number}"

############## MODEL ###############

# Notes:
# - Bcrypt should output a 60-character string, so this was used as maximum password length
# - booleans ("true"/"false") should not be strings or booleans, but Enums of modelBool
# - it is best to set values using defined methods rather than directly
# - access_level should be either "user" or "admin". Change access_level using make_user_admin. The access_level "super admin" exists, but there should be only 1 user with this access. TODO: acees level defined in separate db model

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
    recovery_email = db.Column(EncryptedType, nullable=True)
    # one time password (otp):
    otp_token = db.Column(db.String(8), nullable=True)
    otp_token_creation = db.Column(UTCDateTime, nullable=True)
    # acct:
    created_at = db.Column(UTCDateTime, default=datetime.now(timezone.utc))
    email_is_verified = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False)
    # access:
    access_level = db.Column(db.Enum(UserAccessLevel), default=UserAccessLevel.USER, nullable=False)
    is_blocked = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False)
    # activity:
    flagged = db.Column(db.Enum(UserFlag), default=UserFlag.BLUE, nullable=False)
    last_seen = db.Column(UTCDateTime, default=datetime.now(timezone.utc))
    login_attempts = db.Column(db.Integer, default=0)
    last_login_attempt = db.Column(UTCDateTime, default=datetime.now(timezone.utc))
    login_blocked = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False)
    login_blocked_until = db.Column(UTCDateTime, default=datetime.now(timezone.utc))
    # auth credential change or verification:
    new_email = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), nullable=True, unique=True)
    token = db.relationship("Token", backref="user", lazy="select", cascade="all, delete-orphan")
    # preferences
    mfa_enabled = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False) 
    in_mailing_list = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False) 
    night_mode_enabled = db.Column(db.Enum(modelBool), default=modelBool.TRUE, nullable=False) 
    # multi-factor authentication (mfa)
    first_factor_used = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False)
    first_factor_used_date = db.Column(UTCDateTime, default=datetime.now(timezone.utc), nullable=True)
    first_factor_type = db.Column(db.Enum(LoginMethods), nullable=True)
    
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
    
    # One-time password (OTP) methods
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
        try:
            new_otp = get_eight_digits_number()
            self.otp_token = new_otp
            self.otp_token_creation = datetime.now(timezone.utc)
            db.session.commit()  # Save changes to the database
            return new_otp
        except Exception as e:
            logging.error(f"Failed to generate OTP for user {self.id}: {e}")
            raise

    def otp_reset(self) -> None:
        """
        Resets the fields associated with OTP.
        """
        try:
            self.otp_token = None
            self.otp_token_creation = None
            db.session.commit()
        except Exception as e:
            logging.error(f"Failed to reset OTP for user {self.id}: {e}")
            raise

    def check_otp(self, otp: str) -> bool:
        """
        Validates a given OTP against the expected format, the stored OTP token, 
        and its validity period.

        This method checks the following:
        1. Whether the provided OTP matches the expected format defined by `OTP_PATTERN`.
        2. Whether the OTP matches the stored OTP token in the database (`self.otp_token`).
        3. Whether the OTP was created within the allowed validity period (e.g., 30 minutes).

        Args:
            otp (str): The OTP provided for validation, expected to be a string.

        Returns:
            bool: True if the OTP is valid, matches the stored token, and is within the allowed time frame.
                False otherwise.
        """
        # Check if OTP matches expected pattern
        if not re.match(OTP_PATTERN, otp):
            return False
        # Check if otp matches the one in the DB
        if otp != self.otp_token:
            return False
        # Check if otp is still valid
        now = datetime.now(timezone.utc)
        otp_age = (now - self.otp_token_creation).total_seconds() / 60  # Calculate age in minutes

        if otp_age > 30:  # OTP is older than 30 minutes
            # Reset fields in the DB
            self.otp_reset()
            return False
        # Reset fields in the DB
        self.otp_reset()
        # Return otp is valid
        return True

    # MFA methods
    def mfa_first_factor_used(self, method: LoginMethods) -> None:
        """
        Logs the successfull first factor of a multi-factor authentication process.

        Args:
            method (LoginMethods): Method belonging to enum LoginMethods.
        
        user.first_factor_used will be set to true
        user.first_factor_type will be set to the method authenticated
        user.first_factor_used_date will bet set to the current datestring
        """
        self.first_factor_used = modelBool.TRUE
        self.first_factor_type = method
        self.first_factor_used_date =  datetime.now(timezone.utc)
        db.session.commit()  # Save changes to the database

    def mfa_first_factor_reset(self) -> None:
        """
        Resets the fields associated with the first step of the MFA process.
        """
        try:
            self.first_factor_used = modelBool.FALSE
            self.first_factor_type = None
            self.first_factor_used_date = None
            db.session.commit()  # Save changes to the database
        except Exception as e:
            logging.error(f"Failed to reset MFA for user {self.id}: {e}")
            raise

    def mfa_second_factor_check(self, method: LoginMethods) -> bool:
        """
        Checks if the second authentication step in mfa is valid.
        If second method is valid or time constraint overlapsed, first step data will be reset.
        
        Args:
            method (LoginMethods): Method belonging to enum LoginMethods.
        Returns:
            bool: True if the second factor is valid, False otherwise.
        """
        # Check the second method is different than the first
        if method == self.first_factor_used:
            return False
        
        # Reset the first mfa step because it is either too old or the second step is approved
        self.mfa_first_factor_reset()

        # Check if time for MFA elapsed
        now = datetime.now(timezone.utc)
        time_difference = (now - self.first_factor_used_date).total_seconds() / 60  # Calculate time in minutes
        if time_difference > 30:  
            return False
        return True
    
    # Failed login methods
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
            self.login_blocked_until = datetime.now(timezone.utc) + timedelta(minutes=2)
            logging.info(f"Successive failed log-in attempts lead user to be temporarily blocked: {self.email} .")
        elif self.login_attempts == 5:
            self.login_blocked_until = datetime.now(timezone.utc) +timedelta(minutes=3)
        elif 5 < self.login_attempts < 7:
            self.login_blocked_until = datetime.now(timezone.utc) + timedelta(minutes=5)
        elif 7 < self.login_attempts < 10:
            self.login_blocked_until = datetime.now(timezone.utc) + timedelta(minutes=10)
        elif self.login_attempts > 10:
            self.login_blocked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
            logging.critical(f"More than 10 failed login attempts detected for user {self.email}. Potential intrusion / system abuse / brute-force attack.")

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
    
    # Admin blocked user methods
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

    # Access level methods
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
    
    # Retrive users methods
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
    
    # Flag methods
    def flag_change(self, flag_colour: str) -> None:
        """
        Changes the user's flag to the specified color.

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
    
    # Auth credential change or verification methods
    def verify_account(self) -> bool:
        """
        Verifies the user's account email.

        This method sets the user's `email_is_verified` attribute to `modelBool.TRUE`, indicating that
        the email verification process is complete. It is important to ensure that a valid 
        `VerificationToken` was successfully validated before calling this method!

        Returns:
            bool: True if the account was successfully verified, False otherwise.
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
