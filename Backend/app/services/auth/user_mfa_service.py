"""
Docstring for Backend.app.services.user_auth_service

Contains:

- OTP generation and validation
- MFA first and second factor operations
- session reset logic
- email verification workflow
"""
# Python/Flask libraries
import re
import logging
from datetime import datetime, timezone

# Extensions
from app.extensions.extensions import db

# Constants
from app.constants.auth_otp_and_mfa import MFA_VALIDITY_MINUTES
from app.constants.auth_methods import AuthMethods

# Models
from app.models.user import User

def svc_set_MFA(user: User, set_MFA: bool) -> bool:
    """
        Sets `user.mfa_enabled` to True or False and commits to the DB.
        Will return True if MFA status was set and False otherwise.

        :param user (User): Member of User DB model 
        :param set_MFA (bool): `True` to set MFA as enabled, `False` to disable MFA.

        Returns:
            bool:
                True if successful, False if function encounters an error.
    """
    if not user or not isinstance(set_MFA, bool):
        return False
    
    try:
        user.mfa_enabled = set_MFA
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.error(f"svc_set_MFA failed to change user's MFA status. {e}")
        return False


def svc_mark_mfa_first_factor_success(user: User, method: AuthMethods | str) -> None:
    """
        Function in `services/auth/user_mfa_service.py`.
        Sets first factor of a multi-factor authentication process.

        Args:
            method (AuthMethods): Method belonging to enum AuthMethods (enum or its value).
            user: Member of User db 
        
        user.first_factor_used will be set to true
        user.first_factor_type will be set to the method authenticated
        user.first_factor_used_date will bet set to the current datestring

        Example:
        `
        method = "otp"
        svc_mark_mfa_first_factor_success(user, AuthMethods(method))
        `
    """
    try:
        method = AuthMethods(method)
    except ValueError:
        raise ValueError("Invalid authentication method.")

    if method not in {AuthMethods.OTP, AuthMethods.PASSWORD}:
        raise ValueError("Only OTP or PASSWORD allowed as authentication methods.")
    
    user.first_factor_used = True
    user.first_factor_type = method
    user.first_factor_used_date = datetime.now(timezone.utc)

def svc_reset_mfa_first_factor(user: User) -> None:
    """
    Function in `services/auth/user_mfa_service.py`.
    Resets the fields associated with the first step of the MFA process.
    """
    user.first_factor_used = False
    user.first_factor_type = None
    user.first_factor_used_date = None

def svc_check_mfa_second_factor(user: User, method: AuthMethods | str) -> bool:
    """
    Function in `services/auth/user_mfa_service.py`.
    Checks if the second authentication step in mfa is valid.
    If second method is valid or time constraint overlapsed, first step data will be reset.
    
    Args:
        method (AuthMethods): Method belonging to enum AuthMethods.
    Returns:
        bool: True if the second factor is valid, False otherwise.
    """
    try:
        method = AuthMethods(method)
    except ValueError:
        raise ValueError("Invalid authentication method, cannot check second factor auth.")

    if method not in {AuthMethods.OTP, AuthMethods.PASSWORD}:
        raise ValueError("Only OTP or PASSWORD allowed as authentication methods.")
    
    # Check the second method is different than the first
    if method == user.first_factor_type:
        svc_reset_mfa_first_factor(user)
        return False

    # Reset the first mfa step because it is either too old or the second step is approved
    date = user.first_factor_used_date
    svc_reset_mfa_first_factor(user)

    if date is None:
        return False
    
    # Check if time for MFA elapsed
    now = datetime.now(timezone.utc)
    diff_minutes = (now - date).total_seconds() / 60 # Calculate time in minutes
    return diff_minutes <= MFA_VALIDITY_MINUTES