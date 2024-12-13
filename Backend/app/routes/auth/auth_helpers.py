"""
**ABOUT THIS FILE**

auth/auth_helpers.py contains the following helper function(s):

- **reset_user_session**
- **get_hashed_pw**
- **is_good_password**
- **get_user_or_none**

------------------------
**Purpose**

Helper functions to auth routes

"""
import re
import logging
from datetime import datetime
from typing import Optional
from flask_login import current_user
from app.extensions.extensions import db, flask_bcrypt
from app.models.user import User
from app.utils.constants.account_constants import MOST_COMMON_PASSWORDS
from app.utils.detect_html.detect_html import check_for_html
from app.utils.log_event_utils.log import log_event
from app.utils.salt_and_pepper.helpers import get_pepper

def reset_user_session(user: User) -> None:
    """
    Resets the user's session by invalidating old sessions and saving the changes to the database.

    This function overwrites the user's alternative ID in the db (used by Flask-Login to identify the user)
    with a new one, effectively invalidating any previous sessions.

    **Parameters:**
        user (User): The `User` object whose session is being reset.

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
    verifies the password strength, and hashes it using the Flask-Bcrypt library.

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

def get_user_or_none(email: str, route: str) -> Optional[User]:
    """
    Retrieve a user from the database by their email address, or return None if no user exists.

    This function checks the database for a user with the specified email, logs the result, 
    and performs basic validation to detect potential issues (e.g., HTML in the email input).

    ---------------------
    **Parameters:**

        email (str): The email string.
        route (str): The route calling this function.
    
    **Returns:**

        - user (User) object as and if retrieved from the db.
        - `None` if no user is found.
    
    ---------------------
    **Example usage:**

    ```python
    get_user_or_none("xyz.com", "signup")
    # Returns -> None

    get_user_or_none("john@doe.com", "otp")
    # Returns: if user if found, will return user

    get_user_or_none("john@doe.com", "login")
    # Returns: if user if found, will return user
    ```
    """
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            logging.info(f"User not in DB. Input email: {email}.")

            # Check for HTML in the input
            html_in_email = check_for_html(email, f"{route}: email field")
            html_info = " HTML detected in email field." if html_in_email else ""
            logging.warning(
                f"Failed to find user. Email: {email} sent through route: {route}.{html_info}"
            )
            #TODO: fix event logging and use it here
            # try:
            #     log_event("ACCOUNT_LOGIN", "login successful", user.id)
            #     if html_in_email:
            #         log_event("ACCOUNT_LOGIN", "html detected", user.id, f"Email provided: {email}")
            # except Exception as e:
            #     logging.error(f"Failed to create event log. Error: {e}")
            return None
        return user
    except Exception as e:
        logging.error(f"Failed to access db. Error: {e}")
        return None
    