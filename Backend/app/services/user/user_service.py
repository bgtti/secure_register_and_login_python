"""
Docstring for Backend.app.services.user_service

Contains business logic around users, such as:

- Moderation: user flag changes
- Data presentation: serialization of table 

- promote/demote admin
- block/unblock user
- update user email with checks
- login attempt + lockout logic
- verifying account
- setting preferences
- accessing roles



"""
# Python/Flask libraries
import logging
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError

# Extensions
from app.extensions.extensions import db

# Models
from app.models.user import User

# Utilities
from app.common.detect_html.detect_html import check_for_html



# Retrieve user if user exists
def svc_get_user_or_none(email: str, route: str) -> Optional[User]:
    """
    Retrieve a user from the database by their email address, or return None if no user exists.

    This function checks the database for a user with the specified email, logs the result, 
    and performs basic validation to detect potential issues (e.g., HTML in the email input).
    
    :param email (str): The email string.
    :param route (str): The route calling this function.
    
    Returns:
        User | None:
            User object as and if retrieved from the db or `None`if user not found.
    
    ---------------------
    **Example usage:**

    ```python
    svc_get_user_or_none("xyz.com", "signup")
    # Returns -> None

    svc_get_user_or_none("john@doe.com", "otp")
    # Returns: if user if found, will return user

    svc_get_user_or_none("john@doe.com", "login")
    # Returns: if user if found, will return user
    ```
    """
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            logging.info(f"svc_get_user_or_none did not find User in DB. Email: {email} sent through route: {route}.")

            # Check for HTML in the input
            html_in_email = check_for_html(email, f"{route}: email field")
            if html_in_email:
                logging.warning(
                f"WARNING: svc_get_user_or_none detected HTML in email field. Email: {email} sent through route: {route}."
            )
            return None
        return user
    except Exception as e:
        logging.error(f"Failed to access db. Error: {e}")
        return None

def svc_get_user_by_id(user_id: int) -> Optional[User]:
    """
    Retrieve a user from the database by their id, or return None if no user exists.

    :param user_id (int): The id of the user.
    
    Returns:
        User | None:
            User object as and if retrieved from the db or `None`if user not found.
    """
    if not isinstance(user_id, int) or user_id < 1:
        logging.error("Invalid parameters passed to `svc_get_user_by_id`.")
        return None
    try:
        return db.session.get(User, user_id)

    except SQLAlchemyError:
        logging.exception("svc_get_user_by_id failed to access DB.")
        return None

def svc_delete_user(user: User, commit: bool = True)-> bool:
    """
    Deletes a user from the DB.

    :param user: User model instance.
    :param commit: True if changes should be committed to DB.
    :return: True if successful, False otherwise.
    """

    #TODO: check if i already dont have something like this for auth!!!!!
    if not user or not getattr(user, "id", None):
        logging.error("Invalid or no user passed to svc_delete_user.")
        return False
    
    if user.is_super_admin:
        logging.warning(f"Attempt to delete super admin user.")
        return False
    
    user_id = user.id
    
    try:
        db.session.delete(user)
        if commit:
            db.session.commit()
            logging.info(f"User id={user_id} was deleted.")
        return True
    
    except Exception as e:
        if commit:
            db.session.rollback()

        logging.error(f"svc_delete_user failed to delete user id={user_id}. Error: {e}")
        return False


# Retrive users methods
def svc_serialize_user_table(user: User) -> dict | None:
    """
    Serializes the user information into a dictionary.
    
    :param user (User): member of User DB model

    Returns:
        dict | None: A dictionary containing user information or None if invalid user.

    Example response:
    ```
    {
        "id": 12345
        "name": "Frank Torres",
        "email": "frank.torres@fakemail.com",
        "created_at": "Thu, 25 Jan 2024 00:00:00 GMT",
        "last_seen": "Thu, 25 Jan 2024 00:00:00 GMT",
        "access": "user",
        "flagged": "blue",
        "is_blocked": "false"
    }
    ```
    """
    if not user and not user.id:
        logging.error("svc_serialize_user_table received invalid user parameter.")
        return None
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at,
        "last_seen": user.last_seen,
        "access": user.role.access_level,
        "flagged": user.flagged,
        "is_blocked": user.is_blocked,
    }