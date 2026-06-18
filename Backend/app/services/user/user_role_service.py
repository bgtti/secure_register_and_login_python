# Python/Flask libraries
import logging

# Extensions
from app.extensions.extensions import db

# Constants
from constants.roles import ROLES

# Models
from app.models.user import User
from app.models.role import Role


def svc_make_user_admin(
    user_id: int,
    commit: bool = True
) -> bool:
    """
    Changes a user's role to Admin.

    Super Admin users cannot have their role changed through
    this function.

    :param user_id (int): ID of the user.
    :param commit (bool): True if changes should be committed to DB.
    :return: True if successfull, False otherwise.
    """

    if not isinstance(user_id, int) or user_id < 1:
        logging.error("Invalid user_id passed to svc_make_user_admin.")
        return False
    
    # Check if roles list was updated
    admin_role_dict = next((item for item in ROLES if item["id"] == 2), None)
    if not admin_role_dict or admin_role_dict.get("access_level") != "admin":
        # This means the 'role' DB model access level may be different
        logging.error("Changes were made to ROLES list. Update svc_make_user_admin. ")
        return False

    try:
        user = db.session.get(User, user_id)

        if not user:
            logging.error(f"svc_make_user_admin could not find user. ID: {user_id}")
            return False

        # Protect Super Admin
        if user.role.access_level == "super_admin":
            logging.warning(f"Attempt to change role of Super Admin user {user_id}.")
            return False

        # Already admin
        if user.role.access_level == "admin":
            return True

        admin_role = Role.query.filter_by(access_level="admin").first()

        if not admin_role:
            logging.critical("svc_make_user_admin could not find Admin role.")
            return False

        user.role_id = admin_role.id

        if commit:
            db.session.commit()

        return True

    except Exception as e:
        if commit:
            db.session.rollback()

        logging.error(f"svc_make_user_admin failed. Error: {e}")

        return False
    
def svc_make_user_role_user(
    user_id: int,
    commit: bool = True
) -> bool:
    """
    Changes a user's role to [common] User.

    Super Admin users cannot have their role changed through
    this function.

    :param user_id (int): ID of the user.
    :param commit (bool): True if changes should be committed to DB.

    Returns:
        bool:
            True if successful, False otherwise.
    """

    if not isinstance(user_id, int) or user_id < 1:
        logging.error("Invalid user_id passed to svc_make_user_role_user.")
        return False
    
    # Check if roles list was updated
    admin_role_dict = next((item for item in ROLES if item["id"] == 1), None)
    if not admin_role_dict or admin_role_dict.get("access_level") != "user":
        # This means the 'role' DB model access level may be different
        logging.error("Changes were made to ROLES list. Update svc_make_user_role_user. ")
        return False

    try:
        user = db.session.get(User, user_id)

        if not user:
            logging.error(f"svc_make_user_role_user could not find user. ID: {user_id}")
            return False

        # Protect Super Admin
        if user.role.access_level == "super_admin":
            logging.warning(f"Attempt to change role of Super Admin user {user_id}.")
            return False

        # Already user
        if user.role.access_level == "user":
            return True

        user_role = Role.query.filter_by(access_level="user").first()

        if not user_role:
            logging.critical("svc_make_user_role_user could not find User role.")
            return False

        user.role_id = user_role.id

        if commit:
            db.session.commit()

        return True

    except Exception as e:
        if commit:
            db.session.rollback()

        logging.error(f"svc_make_user_role_user failed. Error: {e}")

        return False