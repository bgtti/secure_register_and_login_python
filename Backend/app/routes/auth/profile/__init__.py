"""
**Profile Blueprint**

auth/profile/__init__.py registers the route's blueprint.

This module handles user's change of profile display, including:

- Name change

In this module:
- **routes.py**: the main file, which contains the api routes and consumes the content of all other 'helper' files in the module
- **log.py**: functions used for logging route activity
- **schemas.py**: json schemas to validate client request data 
"""
from flask import  Blueprint

# Blueprint
profile = Blueprint('profile', __name__)

# Import routes to attach them to this blueprint
from app.routes.auth.profile import routes 