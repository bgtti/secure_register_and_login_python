"""
**Credential Change Blueprint**

auth/credential_change/__init__.py registers the route's blueprint.

This module handles user's change of auth credentials, including:

- Password reset (forgotten password)
- Password change
- Email change

In this module:
- **routes.py**: the main file, which contains the api routes and consumes the content of all other 'helper' files in the module
- **email.py**: functions that send email to users, triggered from routes
- **helpers.py**: helper/util functions used in routes
- **log.py**: functions used for logging route activity
- **schemas.py**: json schemas to validate client request data 

"""
from flask import  Blueprint

# Blueprint
credential_change = Blueprint('credential_change', __name__)

# Import routes to attach them to this blueprint
from app.routes.auth.credential_change import routes 
