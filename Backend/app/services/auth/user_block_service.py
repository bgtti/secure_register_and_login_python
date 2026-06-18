"""
Docstring for Backend.app.services.user_auth_service

Contains:

- ....

"""

# Python/Flask libraries
import logging
import math
from datetime import datetime, timedelta, timezone
# Extensions
from app.extensions.extensions import db
# Models
from app.models.user import User

# Utilities
from app.common.ip_utils.ip_anonymization import anonymize_ip
from app.common.ip_utils.ip_geolocation import geolocate_ip
# from app.utils.log_event_utils.log import log_event User not in DB

def svc_check_if_user_blocked(user: User) -> dict:
    """
    Function in `services/auth/user_blocked_service.py`.
    Checks if a user is blocked from logging in, either temporarily due to failed login attempts 
    or permanently by an admin. Returns a dictionary with the block status and an appropriate message.

    Args:
        user (User): The user object being checked.

    Returns:
        dict: A dictionary with the following keys:
        
            - "blocked" (bool): True if the user is blocked, otherwise False.
            - "temporary_block" (bool): True if the block is temporary (by system), otherwise False (blocked by admin).
            - "message" (str): A human-readable message explaining the block status. May be sent in API response.
            - "log_message" (str): A log message explaining why the user is blocked. To be used internally only.
            - "wait_time" (int): An integer indicating the time (in minutes or seconds) the client has to wait until the block is lifted (eg: `10` or `52`).
            - "wait_time_measure" (str): Either "minute", "minutes", "second", or "seconds"
    """
    status = {
    "blocked": False,
    "temporary_block": False,
    "message": "",
    "log_message": "",
    "wait_time": None,
    "wait_time_measure": None,
    }
    
    if user.is_blocked:
        status["blocked"] = True
        status["message"] = "Account blocked, contact us for more information."
        status["log_message"] = "Account blocked by admin."
        return status

    now = datetime.now(timezone.utc)

    user_is_login_blocked = user.login_blocked and (user.login_blocked_until > now)
    

    if user_is_login_blocked:

        # Define blocked time in seconds
        seconds_remaining = int((user.login_blocked_until - now).total_seconds())

        if seconds_remaining <= 0:
            return status
        
        if seconds_remaining < 60:
            wait_time = seconds_remaining
            time_scale = "second" if seconds_remaining == 1 else "seconds"
        else:
            # Define blocked time in minutes
            minutes_remaining = math.ceil((seconds_remaining / 60)) # Rounds up
            wait_time = minutes_remaining
            time_scale = "minute" if minutes_remaining == 1 else "minutes"
            
        status["blocked"] = True
        status["temporary_block"] = True
        status["message"]  = f"Too many failed login attempts, wait {wait_time} {time_scale} and try again."
        status["log_message"] = f"Account temporarily blocked. Client should wait {wait_time} {time_scale} and try again."
        status["wait_time"] = wait_time 
        status["wait_time_measure"] = time_scale 
    return status