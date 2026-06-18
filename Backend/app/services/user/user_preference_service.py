"""
Services affecting the User model:
- set mailing list preferences
- set light versus night mode preferences
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

def svc_set_mailing_list(user: User, wants_mail: bool) -> bool:
    """
        Sets `user.in_mailing_list` to True or False and commits to the DB.

        :param user (User): Member of User DB model 
        :param wants_mail (bool): `True` if user desires to be included in mailing list, `False` otherwise.

        Returns:
            bool:
                True if successful, False if function encounters an error.
    """
    if not user or not isinstance(wants_mail, bool):
        return False
    if user.in_mailing_list == wants_mail:
        return True
    try:
        user.in_mailing_list = wants_mail
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.error(f"svc_set_mailing_list failed to change user's mailing list preferences. {e}")
        return False
    
def svc_set_night_mode(user: User, wants_night_mode: bool) -> bool:
    """
        Sets `user.night_mode_enabled` to True or False and commits to the DB.

        :param user (User): Member of User DB model 
        :param wants_night_mode (bool): `True` if user prefers to view app in nightmode, `False` otherwise.

        Returns:
            bool:
                True if successful, False if function encounters an error.
    """
    if not user or not isinstance(wants_night_mode, bool):
        return False
    if user.night_mode_enabled == wants_night_mode:
        return True
    try:
        user.night_mode_enabled = wants_night_mode
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.error(f"svc_set_night_mode failed to change user's nightmode preferences. {e}")
        return False