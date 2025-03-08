"""
**Recovery Blueprint**

auth/recovery/__init__.py registers the route's blueprint.

This module handles user's account recovery options, including:

- Setting/changing/removing recovery email address
- Checking whether a recovery email has been added to account

In this module:
- **routes.py**: the main file, which contains the api routes and consumes the content of all other 'helper' files in the module
- **email.py**: functions that send email to users, triggered from routes
- **log.py**: functions used for logging route activity
- **schemas.py**: json schemas to validate client request data 

"""
# from flask import Blueprint, request, jsonify, session
from flask import  Blueprint

# Blueprint
recovery = Blueprint('recovery', __name__)

# Import routes to attach them to this blueprint
from app.routes.auth.recovery import routes 