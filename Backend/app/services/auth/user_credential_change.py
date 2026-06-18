"""
Docstring for Backend.app.services.user_service

Contains business logic around users, such as:

- Credential changes: email change
- ...

"""
# Python/Flask libraries
import logging
from datetime import datetime, timedelta, timezone

# Extensions
from app.extensions.extensions import db, flask_bcrypt

# Models
from app.models.user import User

# Utilities
# from app.constants.validation_input_length import INPUT_LENGTH 
# from app.constants.validation_patterns import OTP_PATTERN
# from app.constants.roles import ROLE_ID, ROLES
from app.common.salt_and_pepper.helpers import generate_salt, get_pepper
from app.common.user_credential_helpers.password_validation_and_hash import get_hashed_pw

####################################
#        PW + EMAIL CHANGE         #
####################################

def svc_record_failed_auth_change_attempt(user: User) -> None:
    """
    Function in `services/auth/user_credential_change.py`.
    Increments failed auth-change attempts and blocks user if threshold exceeded. Commits changes to the DB.

    :param user: a member of the User class db model
    """
    try:
        user.auth_change_attempts += 1
        user.last_auth_change_attempt = datetime.now(timezone.utc)

        attempts = user.auth_change_attempts

        if attempts >= 5 and not user.auth_change_blocked:
            user.auth_change_blocked = True
            logging.info(f"User id {user.id} temporarily blocked after {attempts} failed auth change attempts.")
        elif 5 < attempts <= 10:
            logging.warning(f"WARNING: User id {user.id} has {attempts} failed auth change attempts.")
        elif attempts > 10:
            logging.critical(f"CRITICAL: User id {user.id} has {attempts} failed auth change attempts.")

        db.session.commit()

    except Exception as e:
        db.session.rollback() 
        logging.error(f"Failed to record failed auth change attempt to the DB for user_id={user.id}. Error: {e}") 

def svc_reset_failed_auth_change_attempt(user: User) -> None:
    """
    Function in `services/auth/user_credential_change.py`.
    Resets counter of failed password or email change attempt to the db (`user.auth_change_attempts`) and commits changes to it. Returns `None`.

    :param user: a member of the User class db model
    """
    try:
        user.auth_change_attempts = 0
        user.auth_change_blocked = False
        db.session.commit()
    except Exception as e:
        db.session.rollback() 
        logging.error(f"Failed to reset failed auth change attempt to the DB or user_id={user.id}. Error: {e}")

def svc_check_auth_change_block_status(user: User) -> bool:
    """
    Function in `services/auth/user_credential_change.py`.
    Checks whether user is currently blocked from changing credentials.
    If the block period has expired, resets the failed attempt state.
    Returns a boolean indicating whether user is blocked (True) or not (False).

    :param user: a member of the User class db model
    """
    if not user.auth_change_blocked:
        return False
    
    attempts = user.auth_change_attempts
    
    # Define until when user is blocked
    blocked_until = user.last_auth_change_attempt

    if attempts == 5:
        blocked_until += timedelta(minutes=15) 
    elif 5 > attempts <= 7:
        blocked_until += timedelta(minutes=30) 
    elif 7 > attempts < 10:
        blocked_until += timedelta(minutes=60)
    elif attempts >= 10:
        blocked_until += timedelta(minutes=360) # 6 hrs
    
    # Check if user still blocked and, if not, reset blocked status
    if blocked_until > datetime.now(timezone.utc):
        return True
    
    svc_reset_failed_auth_change_attempt(user)
    return False


####################################
#         PASSWORD CHANGE          #
####################################


def svc_change_user_password(user: User, password: str) -> dict:
    """
    Changes the user's account password and resets failed auth-change attempts (and commits changes to the DB).

    **Returns**:
    
    dict: dictionary containing information useful for security logs. Keys:

        - log_text: (str) description of event for security log (should not be exposed to the FE). 
        - log_code: (int) code relevant for security log (200= success, 400= failure due to user input, 500= failure in saving new password to DB)
    """
    # Check if user passed in correctly:
    if not user or not user.created_at:
        raise ValueError("Invalid user passed to svc_change_user_password")
    
    # Prepare response
    res = {
        "log_code": 200,
        "log_text": "Password changed successfully.",
    }
    
    # Create new salt and hashed password
    salt = generate_salt()
    hashed_password = get_hashed_pw(password, user.created_at, salt) # will be None if password does not meet criteria

    if not hashed_password:
        logging.info(f"Password change rejected due to password policy for user_id={user.id}.")
        res["log_code"] = 400
        res["log_text"] = "New password rejected due to password policy."
        return res    
    
    try:
        user.password = hashed_password
        user.password_salt = salt
        user.auth_change_blocked = False
        user.auth_change_attempts = 0
        db.session.commit()
    except Exception as e:
        db.session.rollback() 
        logging.error(f"Failed to change password for user_id={user.id}. Error: {e}")
        res["log_code"] = 500
        res["log_text"] = f"New password could not be saved due to DB failure. Error: {e}"
        return res
    
    logging.info(f"Password changed successfully for user_id={user.id}.")
    return res

####################################
#           EMAIL CHANGE           #
####################################


def svc_reset_new_email(user: User) -> None:
    """
    Sets `user.new_email` to None and commits to the db.
    """
    if not user or not user.new_email:
        return
        
    # Save new email to db
    try:
        user.new_email = None
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"svc_reset_new_email failed to set user.new_email to None. {e}")

def svc_save_new_email(user: User, email:str) -> dict:
    """
    Saves an email to `user.new_email` as the first step of an email change flow.
    This function will:
    - check if email is valid
    - check whether email is equal to account's email and recovery email adress.
    - save and commit to the db

    Returns a dictionary containing the following keys:
        success (bool): True if new email was successfully saved to the db, False otherwise.
        res_code (int): An http code that may be passed in the response (200, 400, or 500)
        res_msg (str): A message that may me passed on to the FE in the response
        log_code (int): An http-like code to be passed log functions (200, 400, 409, or 500)
        log_text (str): A log text.
    """
    # Prepare response
    res = {
        "success": False,
        "res_code": None,
        "res_msg": None,
        "log_code": None,
        "log_text": "",
    }
    # Make sure there are no trailing spaces, and all is lower case
    email = email.strip().lower()

    # Check that new email is different to current email or recovery email
    if email == user.email:
        res["log_code"] = 400
        res["log_text"] = f"New email must be different to current email. New email: {email}"
        res["res_code"] = 400
        res["res_msg"] = "Error: new email cannot be the same as the current email."
        return res
    
    if user.recovery_email and email == user.recovery_email:
        res["log_code"] = 400
        res["log_text"] = f"New email must be different to current recovery email. New email: {email}"
        res["res_code"] = 400
        res["res_msg"] = "Error: new email cannot be the same as the recovery email."
        return res

    # Check if email is already used by another user
    try:
        another_user = User.query.filter_by(email=email).first()
        if another_user:
            res["log_code"] = 409
            res["log_text"] = f"User {email} is already in use by another user."
            res["res_code"] = 400
            res["res_msg"] = "Error: email address not valid - please choose another email."
            logging.info(f"svc_save_new_email failed to save new email: email already in use. ")
            return res
    except Exception as e:
        res["log_code"] = 500
        res["log_text"] = f"Could not verify whether user {email} already exists."
        res["res_code"] = 500
        res["res_msg"] = f"System error: please try again later."
        logging.error(f"svc_save_new_email could not check if new email exists in db: {e}")
        return res
    
    # Save new email to db
    try:
        user.new_email = email
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        res["log_code"] = 500
        res["log_text"] = f"Could not save new email ({email} ) the the db."
        res["res_msg"] = f"System error: please try again later."
        res["res_code"] = 500
        logging.error(f"svc_save_new_email could not save new email to the db. {e}")
        return res
    
    # Warn in case its a super user
    if user.role.access_level == "super_admin":
        logging.warning("Super admin account requested email change.")
    
    res["success"] = True
    res["log_code"] = 200
    res["log_text"] = "New email successfully saved to the db."
    res["res_msg"] = "New email successfully saved to the db."
    res["res_code"] = 200
    
    return res

def svc_change_email(user: User) -> bool:
    """
    Changes the user's account email.
    This method updates the user's email to the value stored in `user.new_email`. 
    It is crucial to ensure that the security codes were successfully validated before 
    calling this method to confirm ownership of the new email address.
    Returns:
        bool: True if the email was successfully changed, False otherwise.
    """
    if not user or not user.new_email:
        logging.error("Attempted email change but no new_email stored.")
        return False
    
    try:
        user.email = user.new_email 
        user.new_email = None
        user.email_is_verified = True
        db.session.commit()

        if user.role.access_level == "super_admin":
            logging.warning("Super admin account email changed.")
        if user.role.access_level == "admin":
            logging.info("Admin account email changed.")
        return True
    except Exception as e:
        db.session.rollback()
        logging.error(f"svc_change_email could not save email to the db. Error: {e}")
        return False


