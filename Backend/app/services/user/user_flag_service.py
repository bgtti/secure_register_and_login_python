# Python/Flask libraries
import logging
# Extensions and configurations
from app.extensions.extensions import db
# Constants
from app.constants.flags import Flag
# Models
from app.models.user import User
# Utilities
from app.common.enum_helpers.map_string_to_enum import map_string_to_enum

# Flag methods
def svc_user_flag_change(user: User, flag_colour: str | Flag, commit: bool = False) -> bool:
    """
    Changes the user's flag to the specified color.
    Accepts a flag color as an argument. Valid choices are those defined in the Flag Enum (eg: 'red', 'yellow', 'purple', 'blue', etc).
    Does not commit changes to the db => this function may be used by other services.
    Returns False if successfull and True otherwise.
    
    :param user (User): Member of the User db model class.
    :param flag_colour (str | Flag): The flag colour (lower case or enum).
    :param commit (bool): Whether the function should commit changes to the DB.

    Example usage:
        `changed_flag = svc_user_flag_change(user, "blue", True) # => True/False`
    """
    # Validate params
    if not user or not flag_colour:
        logging.error(f"Invalid parameters passed to `svc_user_flag_change`.")
        return False

    if not commit or not isinstance(commit, bool):
        commit = False
    
    flag = map_string_to_enum(flag_colour, Flag)

    if flag is None:
        logging.error(f"User flag could not be changed: invalid flag_colour input for svc_user_flag_change. Check Flag Enum for options. flag_colour = {flag_colour}")
        return False
    
    try:
        user.flagged = flag
        if commit:
            db.session.commit()
        return True
    except Exception as e:
        if commit:
            db.session.rollback()
        logging.error(f"svc_user_flag_change was unable to change user flag. Error: {e}")
        return False