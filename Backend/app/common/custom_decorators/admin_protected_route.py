# Python/Flask libraries
import re
from functools import wraps
import logging
from flask import jsonify, request
from flask_login import current_user


# Set up authorization decorator to access admin routes
def admin_only(f):
    """
    Route decorator used to check admin authorization before allowing route access.
    Returns error 401 if user is not authorized to access route.
    
    ```
    Example usage:
    @admin.route("/some_route", methods=["POST"])
    @admin_only
    def route_name():
    # ...
    ```
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role.access_level in {"admin", "super_admin"}:
            return f(*args, **kwargs)

        logging.warning(
            f"Unauthorized admin route access attempt. "
            f"IP={request.remote_addr}, "
            f"Path={request.path}"
        )
        return jsonify({"response": "Route unauthorized."}), 403

    return wrap