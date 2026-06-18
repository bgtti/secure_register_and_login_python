"""
Docstring for Backend.app.services.user_auth_service

Contains:

- OTP generation and validation
- MFA first and second factor operations
- session reset logic
- email verification workflow
"""

# Python/Flask libraries
import logging
from datetime import datetime, timedelta, timezone
# Extensions
from app.extensions.extensions import db
# Models
from app.models.user import User

# Utilities
from app.common.ip_utils.ip_anonymization import anonymize_ip
from app.common.ip_utils.ip_geolocation import geolocate_ip


# TODO: inform user of failed login attempts


def svc_register_failed_login(user: User, client_ip: str, user_agent: str) -> dict:
    """
    Function in `services/auth/user_login_service.py`.
    Increments the counter for failed login attempts and commits to the db.
    This method should be called when the user enters an incorrect password.
    If the failed attempts exceed the maximum allowed, the user is temporarily blocked.
    Does not raise error if committing to db fails. If this happens, log_code will be 500.

    --------
    **Fields overview**:

    :param user: a member of the User class db model
    :param client_ip: the client's ip as string
    :param user_agent: tuser agent from the request header as string

    **Returns**:
    
    dict: dictionary containing information useful for security logs. Keys:

        - log_message: (str) description of number of failed attempts, ip, user-agent, and user id. If 7 or more failed attempts, will also contain full geolocation information. 
        - log_code: (int) containing code relevant for security log
        - geo_location: (string) with city, country if information is available. Otherwise: "N/A, N/A". Can be used to notify the user per email if desired.
        - failed_attempts: (int) number of failed login attempts.

    --------
    **Example usage**:
    ```
    if not password_ok:
        log_info = svc_register_failed_login(user)
        log_login_logout(log_info["log_code"], log_info["log_message"], ...)
    
    log_info -> {
        "log_message": "2 failed login attempts. User id: 345. Login attempt from IP 127.0.0.1. User agent: N/A",
        "log_code": 401,
        "geo_location": "N/A, N/A" 
        "failed_attempts": 2
    }
    ```
    """
    user.login_attempts += 1
    user.last_login_attempt = datetime.now(timezone.utc)

    # Info for the logs and response
    info = f"{user.login_attempts} failed login attempts. User id: {user.id}. Login attempt from IP {client_ip}. User agent: {(user_agent or 'N/A')[:300]}."
    
    res = {
        "log_message": info,
        "log_code": 401,
        "geo_location": "N/A, N/A",
        "failed_attempts": user.login_attempts
    }

    if user.login_attempts >= 3:
        # Geolocation can be expensive. 6+ failed attempts is rare, <.5% of legitimate users.

        if user.login_attempts > 6:
            geolocation = geolocate_ip(client_ip)
            geo_info = ", ".join(f"{k}: {v}" for k, v in geolocation.items())
            info = info + f" Geolocation data => " + geo_info
            res["log_message"] = info
            res["geo_location"] = f"{geolocation.get('city','N/A')}, {geolocation.get('country','N/A')}"

        # Set login_blocked and/or login_blocked_until
        if user.login_attempts == 3:
            user.login_blocked = True
            user.login_blocked_until = datetime.now(timezone.utc) + timedelta(minutes=2)
            log_info = f"Successive failed log-in attempts lead user to be temporarily blocked. {info}"
            logging.info(log_info)
            res["log_message"] = log_info
        elif 3 < user.login_attempts <= 5:
            user.login_blocked_until = datetime.now(timezone.utc) + timedelta(minutes=5)
            logging.info(info)
        elif 5 < user.login_attempts <= 7:
            user.login_blocked_until = datetime.now(timezone.utc) + timedelta(minutes=10)
            logging.warning(info)
            res["log_code"] = 424
        elif 7 < user.login_attempts <= 10:
            user.login_blocked_until = datetime.now(timezone.utc) + timedelta(minutes=20)
            logging.warning(f"WARNING! Suspicious behavior detected: user temporarily blocked for 20 minutes. {info}")
            res["log_code"] = 429
        elif user.login_attempts > 10:
            user.login_blocked_until = datetime.now(timezone.utc) + timedelta(minutes=60)
            logging.critical(f"CRITICAL! Potential intrusion / system abuse / brute-force attack. User temporarily blocked for 60 minutes. {info}")
            res["log_code"] = 451
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        log_message = f"Login attempt counter could not be incremented. User id: {user.id}. Error: {str(e)}"
        logging.exception(log_message)
        res["log_code"] = 500
        res["log_message"] = log_message
    
    return res

def svc_reset_failed_logins(user: User) -> None:
    """
    Function in `services/auth/user_login_service.py`.
    Resets the user's failed login attempt count to 0.
    This method should be called when the user successfully logs in with the correct password.
    It ensures the failed login attempt count is cleared, preventing lockouts for successful logins.
    This function does not commit to the DB.

    What it does:
    ```
    user.login_attempts = 0
    user.last_login_attempt = datetime.now(timezone.utc)
    user.login_blocked_until = datetime.now(timezone.utc)
    user.login_blocked = False`
    user.last_seen = datetime.now(timezone.utc)
    ```

    """
    user.login_attempts = 0
    user.last_login_attempt = datetime.now(timezone.utc)
    user.login_blocked_until = datetime.now(timezone.utc)
    user.login_blocked = False
    user.last_seen = datetime.now(timezone.utc)

def svc_is_login_blocked(user: User) -> bool:
    """
    Function in `services/auth/user_login_service.py`.
    Checks if the user is temporarily blocked due to exceeding failed login attempts.

    Returns:
        bool: True if the user is blocked, False otherwise.
    """
    return user.login_blocked and user.login_blocked_until > datetime.now(timezone.utc)