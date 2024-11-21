"""
**The app/routes/auth package**

**auth/__init__.py** (this) contains the Blueprint definition "auth" to be imported into the route files.

Contains logic for authentication routes in the following files:
- **routes_main.py**: contains api endpoint of core authentication functionality (signup, login, etc)
- **routes_account.py**: contains api endpoint of account management (change email, reset password, etc)
- **schemas.py**: json schemas to validate client request data expected from auth routes
- **helpers.py**: helper functions used in routes

"""

from flask import Blueprint

auth = Blueprint("auth", __name__) 

# Import routes
from . import routes_main, routes_account