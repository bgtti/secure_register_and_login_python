"""
**Registration Blueprint**

auth/registration/__init__.py registers the route's blueprint.

This module handles user's account existence logic, including:

- Account creation (signup)
- Account deletion

In this module:
- **routes.py**: the main file, which contains the api routes and consumes the content of all other 'helper' files in the module
- **email.py**: functions that send email to users, triggered from routes
- **log.py**: functions used for logging route activity
- **schemas.py**: json schemas to validate client request data 

"""
# from flask import Blueprint, request, jsonify, session
from flask import  Blueprint

# Blueprint
registration = Blueprint('registration', __name__)

# Import routes to attach them to this blueprint
from app.routes.auth.registration import routes 