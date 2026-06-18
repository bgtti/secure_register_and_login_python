"""
Docstring for Backend.app.services.user_auth_service

Contains:

- Checks if user was blocked by admin, blocks and unblocks user access
- Functions related to user role changes
"""
# Python/Flask libraries
import logging

# Extensions and configurations
from app.extensions.extensions import db
from config.values import SUPER_USER

# Constants
from constants.roles import ROLE_ID, ROLES

# Models
from app.models.user import User

############ CONSTANTS #############
ADMIN_PW = SUPER_USER["password"]

############ SERVICES #############

def svc_set_user_blocked(
    user: User,
    is_blocked: bool,
    commit: bool = True
) -> bool:
    """
    Blocks or unblocks a user account.

    Super Admin users cannot be blocked through this function.

    :param user: User model instance.
    :param is_blocked: True to block user, False to unblock user.
    :param commit: True if changes should be committed to DB.
    :return: True if successful, False otherwise.
    """

    if not user or not getattr(user, "id", None):
        logging.error("Invalid or no user passed to svc_set_user_blocked.")
        return False

    if not isinstance(is_blocked, bool):
        logging.error("Invalid is_blocked passed to svc_set_user_blocked.")
        return False

    if user.is_super_admin: 
        logging.warning(f"Attempt to block Super Admin user={user.id}.")
        return False

    try:
        if user.is_blocked == is_blocked:
            return True

        user.is_blocked = is_blocked

        if commit:
            db.session.commit()

        return True

    except Exception as e:
        if commit:
            db.session.rollback()

        logging.error(f"svc_set_user_blocked failed. Error: {e}")
        return False

# TODO: Should this be in services???... not sure
def svc_promote_to_super_admin(user: User, admin_password: str) -> None:
        """
        Promotes the user to super admin. There should only be one super admin in the system.
        Since the idea is to call it only once (as the super admin is the first user created),
        it required the admin password defined in the app's config.
        """
        from app.models.role import ROLE_ID
        if user.role_id != ROLE_ID["super_admin"]:
            existing_super_admins = User.query.filter_by(role_id=ROLE_ID["super_admin"]).count()
            if existing_super_admins == 0 and admin_password == ADMIN_PW:
                user.role_id = ROLE_ID["super_admin"]