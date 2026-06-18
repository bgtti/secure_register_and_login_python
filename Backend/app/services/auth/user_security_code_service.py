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
import secrets
from datetime import datetime, timezone


# Extensions
from app.extensions.extensions import db, flask_bcrypt


# Constants
from app.constants.auth_otp_and_mfa import OTP_VALIDITY_MINUTES, SECURITY_CODE_VALIDITY_MINUTES
from app.constants.validation_patterns import OTP_PATTERN
from app.constants.auth_methods import AuthMethods

# Models
from app.models.user import User

# Utilities
from app.common.generators.numbers import get_eight_digits_number
from app.common.salt_and_pepper.helpers import get_pepper

# OTP services

def svc_generate_security_code(user: User, second_code: bool = False) -> list[str] | None:
    """
    Generates a security code, saves a hash of it to the user's `security_code` along with the current timestamp in UTC (`security_code_creation`), commits to the DB, and returns the generated code inside a list.
    Optionally, also generates `security_code_2` if second_code is set to True. Second code will be in index 1 of the array.
    If an error occurs while committing to the DB, function will return None.

    --------

    :param user: a member of the User class db model
    :param second_code: if True will also generate security_code_2

    **Returns**:

    list[str] | None: A list with the generated code(s) as a string or None in case of failure.

    --------
    **Example usage**:  
    ```
        code = generate_security_code(user, True)
        print(code) #=> [3FUR889Z, K55Z7PR2]
    ```
    """
    def generate_security_code() -> str:
        alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        return ''.join(secrets.choice(alphabet) for _ in range(8))

    code_1 = generate_security_code()
    hashed_code_1 = flask_bcrypt.generate_password_hash(code_1).decode("utf-8")

    codes = [code_1]
    hashed_code_2 = None

    if second_code:
        code_2 = generate_security_code()
        hashed_code_2 = flask_bcrypt.generate_password_hash(code_2).decode("utf-8")
        codes.append(code_2)
    
    try:
        user.security_code = hashed_code_1
        user.security_code_creation = datetime.now(timezone.utc)
        user.security_code_2 = hashed_code_2
        db.session.commit()
        return codes
    except Exception as e:
        db.session.rollback()
        log_message = f"Failed to generate security code and add it to DB. Error: {str(e)}"
        logging.warning(log_message) 
        return None

def svc_reset_security_codes(user: User) -> bool:
    """
    Resets the user fields associated with security codes. 
    Returns True if successful reset, False in case of failure.

    --------

    :param user: a member of the User class db model
    ```
    """
    try:
        user.security_code = None
        user.security_code_creation = None
        user.security_code_2 = None
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        log_message = f"Failed to reset security code in the DB. User id: {user.id}. Error: {str(e)}"
        logging.exception(log_message) 
        return False

def svc_validate_security_codes(user: User, security_code: str, second_code: str = "") -> bool:
    """
    Validates security code(s) against the hashes stored in the DB and checks expiry (const SECURITY_CODE_VALIDITY_MINUTES).

    If the code(s) are valid, they are reset.
    If the codes are expired, they are reset.
    If the input is wrong, they are not reset so the user can try again.

    --------

    :param user (class): a member of the User class db model
    :param security_code (str): The security_code for validation
    :param second_code (str): The security_code_2 for validation (optional)

    """
    # Check if values exist in db
    if not user.security_code or not user.security_code_creation:
        return False
    if user.mfa_enabled and not second_code:
        return False
    
    # Check timestamp
    now = datetime.now(timezone.utc)
    code_age_minutes = (now - user.security_code_creation).total_seconds() / 60
    if code_age_minutes > SECURITY_CODE_VALIDITY_MINUTES:
        svc_reset_security_codes(user)
        return False
    
    # Check if first code matches the one in the DB
    code_1_ok = flask_bcrypt.check_password_hash(user.security_code, security_code)

    # Only one code required
    if not user.mfa_enabled and not second_code:
        if code_1_ok:
            svc_reset_security_codes(user)
        return code_1_ok
    
    # Check second code
    if not user.security_code_2:
        svc_reset_security_codes(user)
        return False
    
    code_2_ok = flask_bcrypt.check_password_hash(user.security_code_2, second_code)

    if code_1_ok and code_2_ok:
        svc_reset_security_codes(user)
        return True
    
    # Check if codes were mixed up (check in reversed order)
    reversed_1_ok = flask_bcrypt.check_password_hash(user.security_code, second_code)
    reversed_2_ok = flask_bcrypt.check_password_hash(user.security_code_2, security_code)

    if reversed_1_ok and reversed_2_ok:
        svc_reset_security_codes(user)
        return True
    
    return False