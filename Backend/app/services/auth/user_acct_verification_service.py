# Python/Flask libraries
import logging

# Extensions
from app.extensions.extensions import db

# Models
from app.models.user import User

def svc_verify_user_acct_email(user: User) -> bool:
    """
    Verifies the user's account email and commits changes to the DB.
    Returns True if successful and False otherwise.

    Ensure an OTP is validated before calling this service.

    :param user (User): a member of the User class db model
    """
    if not user:
        return False
    if user.email_is_verified:
        return True
        
    try:
        user.email_is_verified = True
        db.session.commit()
        return True
    
    except Exception as e:
        db.session.rollback()
        logging.error(f"svc_verify_user_acct_email failed to set user.email_is_verified to True. {e}")
        return False