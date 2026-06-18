"""
**ABOUT THIS FILE**

auth/auth_helpers.py contains the helper functions used by auth routes.

"""
# Python/Flask libraries
import re
import logging
from datetime import datetime
from typing import Optional

# Extensions
from app.extensions.extensions import flask_bcrypt

# Utilities
from app.constants.validation_password import MOST_COMMON_PASSWORDS

# from app.utils.log_event_utils.log import log_event User not in DB
from app.common.salt_and_pepper.helpers import get_pepper


def is_good_password(password: str) -> bool:
    """
    This function checks if a password meets strength criteria, such as:
    - Ensuring it is not in a list of common passwords.
    - Avoiding excessive character repetition.
    ---------------------

    **Parameters:**
        password (str): The password string to be evaluated.

    **Returns:**
        - `False` if password is weak.
        - `True` if password is strong.

    ---------------------
    **Example usage:**
    ```python
        password_to_check = "SecurePassword123"
        if is_good_password(password_to_check):
            print("Password is valid!")
        else:
            print("Password is invalid.")
    ```
    """
    # Check for sequential repetition
    sequential_repetition_pattern = r"(\S)\1{3,}"  # Matches any character repeated 4 or more times
    if re.search(sequential_repetition_pattern, password):
        return False

    # Check for common passwords only if the password is 15 characters or less
    if len(password) <= 15 and any(common_password in password for common_password in MOST_COMMON_PASSWORDS):
        return False

    # If the password passes both checks, it is considered valid
    return True

def get_hashed_pw(password: str, date: datetime, salt: str) -> Optional[str]:
    """
    This function takes a plaintext password, a creation date, and a salt value,
    verifies the password strength (excessive character repetition and list of common passwords), and hashes it using the Flask-Bcrypt library.

    ---------------------
    **Parameters:**

        password (str): The password string.
        date (datetime): Should be the same as the user's account creation date.
        salt (str): Should be the same as the salt saved to the user's db.
    
    **Returns:**

        - Optional[str]:  The hashed password string, ready to be stored in the database.
        - `None` if the password is weak or hashing fails.
    """
    if not is_good_password(password):
        logging.info("Weak password provided. Hashing password failed.")
        return None
    pepper = get_pepper(date)
    salted_password = salt + password + pepper
    hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode("utf-8")
    return hashed_password