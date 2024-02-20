from flask import jsonify
from functools import wraps
import logging
from flask_login import current_user
from app.utils.constants.enum_class import UserAccessLevel


# Set up authorization decorator to access admin routes
def admin_only(f):
    """
    admin_only() -> None
    ---------------------------------------------------------------
    Route decorator used to check admin authorization before allowing route access.
    Returns error 401 if user is not authorized to access route.
    ---------------------------------------------------------------
    Example usage:
    @admin.route("/some_route", methods=["POST"])
    @admin_only
    def route_name():
    # ...
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.access_level == UserAccessLevel.SUPER_ADMIN or current_user.access_level == UserAccessLevel.ADMIN:
            return f(*args, **kwargs)
        else:
            logging.warning(f"Attempt to access admin route blocked.")
            error_response = {"response": "Route unauthorized."}
            return jsonify(error_response), 401
    return wrap