"""
Docstring for Backend.app.services.user_service

Contains business logic around users, such as:

- Credential changes: email change
- ...

"""
# Python/Flask libraries
import logging

# Extensions
from app.extensions.extensions import db

# Models
from app.models.user import User


####################################
#       SET RECOVERY EMAIL         #
####################################


def svc_reset_new_recovery_email(user: User) -> None:
    """
    Sets `user.new_recovery_email` to None and commits to the db.
    """
    if not user or not user.new_recovery_email:
        return 
        
    # Reset "new_recovery_email"
    try:
        user.new_recovery_email = None
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"svc_reset_new_recovery_email failed to set user.new_recovery_email to None. {e}")

def svc_save_new_recovery_email(user: User, email:str) -> dict:
    """
    Saves an email to `user.new_recovery_email` as the first step of an email change flow.
    This function will:
    - check if email is valid
    - check whether email is equal to account's email and current recovery email adress.
    - save and commit to the db

    Returns a dictionary containing the following keys:
        success (bool): True if new recovery email was successfully saved to the db, False otherwise.
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

    # Check that new recovery email is different to current email or current recovery email
    if email == user.email:
        res["log_code"] = 400
        res["log_text"] = f"Recovery email must be different to current email. New email: {email}"
        res["res_code"] = 400
        res["res_msg"] = "Error: recovery email cannot be the same as the current email."
        return res
    
    if user.recovery_email and email == user.recovery_email:
        res["log_code"] = 400
        res["log_text"] = f"New email must be different to current recovery email. New email: {email}"
        res["res_code"] = 400
        res["res_msg"] = "Error: new recovery email cannot be the same as the recovery email."
        return res

    # Check if email is already used by another user
    try:
        another_user = User.query.filter_by(email=email).first()
        if another_user:
            res["log_code"] = 409
            res["log_text"] = f"User {email} is already in use by another user."
            res["res_code"] = 400
            res["res_msg"] = "Error: email address not valid - please choose another email."
            logging.info(f"svc_save_new_recovery_email failed to save new recovery email: email already in use. ")
            return res
    except Exception as e:
        res["log_code"] = 500
        res["log_text"] = f"Could not verify whether user {email} already exists."
        res["res_code"] = 500
        res["res_msg"] = f"System error: please try again later."
        logging.error(f"svc_save_new_recovery_email could not check if new email exists in db: {e}")
        return res
    
    # Save new email to db
    try:
        user.new_recovery_email = email
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        res["log_code"] = 500
        res["log_text"] = f"Could not save new recovery email ({email} ) the the db."
        res["res_msg"] = f"System error: please try again later."
        res["res_code"] = 500
        logging.error(f"svc_save_new_recovery_email could not save new recovery email to the db. {e}")
        return res
    
    # Warn in case its a super user
    if user.role.access_level == "super_admin":
        logging.warning("Super admin account requested to set a new recovery email.")
    
    res["success"] = True
    res["log_code"] = 200
    res["log_text"] = "New recovery email successfully saved to the db."
    res["res_msg"] = "New recovery email successfully saved to the db."
    res["res_code"] = 200
    
    return res

def svc_set_recovery_email(user: User) -> bool:
    """
    Sets the user's recovery email.
    This method updates the user's recovery email to the value stored in `user.new_recovery_email`. 
    It is crucial to ensure that the security code was successfully validated before 
    calling this method to confirm ownership of the new recovery email address.
    Returns:
        bool: True if the recovery email was successfully set, False otherwise.
    """
    if not user or not user.new_recovery_email:
        logging.error("Attempted email change but no new_recovery_email stored.")
        return False
    
    try:
        user.email = user.new_recovery_email 
        user.new_recovery_email = None
        db.session.commit()

        if user.role.access_level == "super_admin":
            logging.warning("Super admin account set new recovery email.")
        if user.role.access_level == "admin":
            logging.info("Admin account set new recovery email.")
        return True
    except Exception as e:
        db.session.rollback()
        logging.error(f"svc_set_recovery_email could not set recovery email to the db. Error: {e}")
        return False
    

def svc_delete_recovery_email(user: User) -> bool:
    """
    Sets `user.recovery_email` to None and commits to the DB.
    Disables MFA because a recovery email is required.
    Returns True if successful, False otherwise.
    """
    if not user or not user.recovery_email:
        logging.error(f"svc_delete_recovery_email could not find user or recovery email.")
        return False
        
    # Delete "recovery_email"
    try:
        user.recovery_email = None
        # If MFA enabled, it will be disabled because recovery email is a requirement
        user.mfa_enabled = False
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.error(f"svc_delete_recovery_email failed to set user.recovery_email to None. {e}")
        return False