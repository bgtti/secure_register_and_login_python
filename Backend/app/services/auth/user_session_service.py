"""
**ABOUT THIS FILE**

auth/auth_helpers.py contains the helper functions used by auth routes.

"""
# Python/Flask libraries
import logging
# Extensions
from app.extensions.extensions import db
# Database models
from app.models.user import User


def svc_reset_user_session(user: User) -> None:
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
        svc_reset_user_session(user)
    ```
    """
    # Check if user was sent in correctly in request
    if not user or not isinstance(user, User) or not user.id:
        logging.error(f"svc_reset_user_session found no user. Session reset failed.")
    # Reset session
    user.new_session()  
    db.session.commit()


