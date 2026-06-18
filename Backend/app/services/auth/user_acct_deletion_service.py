# Python/Flask libraries
import logging
# Extensions
from app.extensions.extensions import db
# Models
from app.models.user import User
# Constants
from constants.roles import ROLES # for info


def svc_delete_user_account(user: User):
    """
    Function in `services/auth/user_acct_deletion_service.py`.
    Deletes a user and commits changes to the DB.

    **This function will do the following:** 
    - Check whether user exists by searching for email or pw (if user not passed as an argument)
    - Block attempts to delete super_user role
    - Delete user from DB

    **What this service does not do:**
    - It does not reset user sessions
    - It does not check who is making the request (eg: is an admin deleting the user or the user deleting own account)
    - It does not validate user credentials before deletion (recommended action in routes)
    - It does not send any emails
    - Does not raise error if committing to db fails. If this happens, log_code will be 500.

    --------
    **Fields overview**:

    :param user: member of User db model

    **Returns**:
    
    dict: dictionary containing information useful for security logs. Keys:

        - success: (bool) whether user was deleted (True) or not (False)
        - log_code: (int) containing code relevant for security log
        - log_text: (str) information for logs

    --------
    **Example usage**:
    ```
    user = get_user_or_none(current_user.email, "delete_user")
    user_deletion = delete_user(user)
    
    user_deletion -> {
        "success": True,
        "log_code": 200,
        "log_text": "" 
    }
    ```
    """
    # Prepare response
    res = {
        "success": False,
        "log_code": 500,
        "log_text": "",
    }
    # Check if user was sent in correctly in request
    if not user or not isinstance(user, User) or not user.id:
        res["log_code"] = 501
        res["log_text"] = f"Service request sent without user email or id. User could not be identified."
        logging.error(f"Service auth/user_acct_deletion_service.py/delete_user found no user deletion failed.")
        return res
    
    # Check if account can be deleted
    if user.role.access_level == "super_admin":
        res["log_code"] = 403
        res["log_text"] = f"Attempt to delete super account."
        logging.warning(f"Attempt to delete super account blocked.")
        return res
    
    # Delete account
    try:
        user_id = user.id
        db.session.delete(user)
        db.session.commit()
        logging.info(f"User account deleted successfully. Id = {user_id}.")
    except Exception as e:
        db.session.rollback()
        res["log_text"] = f"Account deletion (id={user.id}) failed."
        logging.error(f"Account deletion failed (id={user.id}). Details: {e}")
        return res
    res["success"]= True
    res["log_code"]=200
    return res

