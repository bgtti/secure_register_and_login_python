"""
Docstring for Backend.app.services.user_auth_service

Contains:

- OTP generation: generate_otp_for_user 
- OTP validation: validate_otp_for_user
- OTP reset: reset_otp_for_user
- OTP and password validation: is_pw_or_otp_valid

"""
# Python/Flask libraries
import re
import logging
from datetime import datetime, timezone

# Extensions
from app.extensions.extensions import db, flask_bcrypt

# Constants
from app.constants.auth_otp_and_mfa import OTP_VALIDITY_MINUTES
from app.constants.validation_patterns import OTP_PATTERN
from app.constants.auth_methods import AuthMethods

# Models
from app.models.user import User

# Utilities
from app.common.generators.numbers import get_eight_digits_number
from app.common.salt_and_pepper.helpers import get_pepper

# OTP services

def svc_generate_otp(user: User) -> str | None:
    """
    Function in `services/auth/user_otp_and_pw_service.py`.
    Generates an OTP, saves it to the user's `otp_token` along with the current timestamp in UTC (`otp_token_creation`), commits to the DB, and returns the generated OTP.
    If an error occurs while committing to the DB, otp will return None.

    --------
    **Fields overview**:

    :param user: a member of the User class db model

    **Returns**:

    str | None: The generated OTP as a string or None in case of failure.

    --------
    **Example usage**:  
    ```
        otp = svc_generate_otp(user)
        print(f"Generated OTP: {otp}")
    ```
    """
    otp = str(get_eight_digits_number())
    try:
        user.otp_token = otp
        user.otp_token_creation = datetime.now(timezone.utc)
        db.session.commit()
        return otp
    except Exception as e:
        db.session.rollback()
        log_message = f"Failed to generate OTP and add it to DB. Error: {str(e)}"
        logging.warning(log_message) 
        return None

def svc_reset_otp(user: User) -> bool:
    """
    Function in `services/auth/user_otp_and_pw_service.py`.
    Resets the fields associated with OTP. 

    --------
    **Fields overview**:

    :param user: a member of the User class db model

    **Returns**:
    bool: True if successful reset, False in case of failure.

    --------
    **Example usage**:
    ```
    otp_reset = svc_reset_otp(user)
    # otp_reset -> True
    ```
    """
    try:
        user.otp_token = None
        user.otp_token_creation = None
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        log_message = f"Failed to reset OTP in the DB. User id: {user.id}. Error: {str(e)}"
        logging.exception(log_message) 
        return False
    return True

def svc_validate_otp(user: User, otp: str) -> bool:
    """
    Function in `services/auth/user_otp_and_pw_service.py`.
    Validates a given OTP against the expected format, the stored OTP token, 
    and its validity period. It will reset the OTP checked, committing changes to the DB.
    This method checks the following:
    1. Whether the provided OTP matches the expected format defined by `OTP_PATTERN`.
    2. Whether the OTP matches the stored OTP token in the database (`user.otp_token`).
    3. Whether the OTP was created within the allowed validity period (e.g., 30 minutes). Validity period is defined in `models/user.py`

    --------
    **Fields overview**:

    :param otp (str): The OTP provided for validation, expected to be a string.
    :param user (class): a member of the User class db model

    **Returns**:
    bool: True if the OTP is valid, matches the stored token, and is within the allowed time frame. False otherwise.
    """
    # Check if values exist in db
    if not user.otp_token or not user.otp_token_creation:
        return False
    # Check if OTP matches expected pattern
    if not otp or not re.match(OTP_PATTERN, otp): 
        return False
    # Check if otp matches the one in the DB
    if otp != user.otp_token: 
        return False
    
    # Check if otp is still valid
    now = datetime.now(timezone.utc)
    otp_age_minutes = (now - user.otp_token_creation).total_seconds() / 60
    if otp_age_minutes > OTP_VALIDITY_MINUTES:
        svc_reset_otp(user)
        return False
    # Reset otp so user cannot re-use it
    return svc_reset_otp(user)

def svc_is_pw_or_otp_valid(user: User, pw_or_otp: str, method: str = "password") -> bool:
    """
    Function in `services/auth/user_otp_and_pw_service.py`.
    Will check whether an OTP or password is valid. In the case of OTP, it will reset it and commit changes to the DB. 
    
    **Fields overview**:

    :param user (class): a member of the User class db model
    :param pw_or_otp (str): The OTP or plain-text password.
    :param method (str): value from AuthMethods enum (= "otp" or "password").

    **Returns**:
    bool: True if the OTP or password is valid, false otherwise.

    --------
    **Example usage**:
    ```
    is_pw_valid = svc_is_pw_or_otp_valid(user, "hello123", "password")
    if not is_pw_valid:
    #...
    ```
    """

    # Check if method is valid
    if method not in {m.value for m in AuthMethods}:
        logging.error("Invalid AuthMethods value passed to svc_is_pw_or_otp_valid.")
        return False
    
    # Check password or otp accordingly
    if method == AuthMethods.PASSWORD.value:
        salted_password = user.salt + pw_or_otp + get_pepper(user.created_at)
        return flask_bcrypt.check_password_hash(user.password, salted_password)
    
    if method == AuthMethods.OTP.value:
        return svc_validate_otp(user, pw_or_otp)
    
    return False