"""
**ABOUT THIS FILE**

auth/auth_helpers.py contains the helper functions used by auth routes.

"""
# Python/Flask libraries
import re
import logging
from datetime import datetime, timezone
from typing import Optional
# Extensions
# from flask_login import current_user
from app.extensions.extensions import db, flask_bcrypt
# Database models
from app.models.user import User
# Utilities
from app.utils.constants.account_constants import MOST_COMMON_PASSWORDS
from app.utils.detect_html.detect_html import check_for_html
from app.utils.ip_utils.ip_anonymization import anonymize_ip
from app.utils.ip_utils.ip_geolocation import geolocate_ip
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
    
def check_if_user_blocked(user: User, client_ip: str | None) -> dict:
    """
    Checks if a user is blocked from logging in, either temporarily due to failed login attempts 
    or permanently by an admin. Returns a dictionary with the block status and an appropriate message.

    Args:
        user (User): The user object being checked.
        client_ip (str | None): The IP address of the client attempting to log in. 
                                Can be `None` if the IP is unavailable.

    Returns:
        dict: A dictionary with the following keys:
        
            - "blocked" (bool): True if the user is blocked, otherwise False.
            - "temporary_block" (bool): True if the block is temporary, otherwise False.
            - "message" (str): A human-readable message explaining the block status.
    """
    status = {
    "blocked": False,
    "temporary_block": False,
    "message": ""
    }
    user_is_admin_blocked = user.has_access_blocked()

    if user_is_admin_blocked:
        status["blocked"] = True
        status["message"] = "Account blocked, contact us for more information."
        logging.info(f"User blocked. Input email: {user.email}. (typically error code: 403)")
        try:
            log_event("ACCOUNT_LOGIN", "user blocked", user.id)
        except Exception as e:
            logging.error(f"Failed to log event. Error: {e}")
        return status

    user_is_login_blocked = user.is_login_blocked()

    if user_is_login_blocked:
        # Define blocked time
        now = datetime.now(timezone.utc)
        time_difference = (user.login_blocked_until - now).total_seconds() / 60
        status["blocked"] = True
        status["temporary_block"] = True
        status["message"]  = f"Too many failed login attempts, wait {time_difference:.2f} minutes and try again."
        # Info for the logs
        geolocation = geolocate_ip(client_ip) 
        # Full IP in case 10 or more failed attempts to login, else anonymized version
        ip_address = client_ip if user.login_attempts >= 10 else anonymize_ip(client_ip)
        geo_info = f"Login attempt from IP {ip_address}. Geolocation: country = {geolocation["country"]}, city = {geolocation["city"]}."
        info = f"User account temporarily blocked from login. User: {user.email}, number of login attempts: {user.login_attempts}. {geo_info} (typically error code: 403)"
        # Log levels according to nr of failed attempts
        log_level = logging.warning if user.login_attempts >= 6 else logging.info
        log_level(info)
        try:
            event_message = (
                "wrong credentials 5x" if user.login_attempts >= 6 else "wrong credentials 3x"
            )
            log_event("ACCOUNT_LOGIN", event_message, user.id, geo_info)
        except Exception as e:
            logging.error(f"Failed to log event for login-blocked user. Error: {e}")
    return status


            