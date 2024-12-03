"""
**ABOUT THIS FILE**

auth/auth_helpers.py contains the following helper function(s):

- **reset_user_session**
- **get_hashed_pw**
- **is_good_password**

------------------------
**Purpose**

Helper functions to auth routes

"""
import re
import logging
from flask_login import current_user
from app.extensions.extensions import db, flask_bcrypt
from app.utils.constants.account_constants import MOST_COMMON_PASSWORDS
from app.utils.salt_and_pepper.helpers import get_pepper

def reset_user_session(user):
    """
    **reset_user_session(user: User) -> None**

    ---------------------------------------
    Resets the user's session by invalidating old sessions and committing the changes to the database.
    It does this by overwriting the alternative id (used by Flask-Login to identify the user) with a new one.

    **Argumets:**
        user: The User object whose session is being reset
    ---------------------------------------
    **Example usage:**
    ```python
        # inside route:
        user = current_user
        reset_user_session(user)
    ```
    """
    user.new_session()  
    db.session.commit()

def is_good_password(password):
    """
    **is_good_password(password: str) -> bool**

    ---------------------------------------
    Defines whether a password is weak or strong.
    It will search it in a list of most common passwords and check for character repetition.

    **Returns:**
        - `False` if password is weak.
        - `True` if password is strong.
    ---------------------------------------
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

def get_hashed_pw(password, date, salt):
    """
    **get_hashed_pw(password: str, date: datetime, salt:str)--> str | null**

    ---------------------
    Returns a password that is properly hashed and includes salt and pepper.

    ---------------------
    **Parameters:**

        password (str): The password string.
        date (datetime): Should be the same as the user's account creation date.
        salt (str): Should be the same as the salt saved to the user's db.
    
    **Returns:**

        str: Hashed password string ready to be stored in the database.
        None: If the password is weak or hashing fails.
    """
    if not is_good_password(password):
        logging.info("Weak password provided. Hashing password failed.")
        return None
    pepper = get_pepper(date)
    salted_password = salt + password + pepper
    hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode("utf-8")
    return hashed_password