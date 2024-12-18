"""
**The app/routes/auth package**

**auth/__init__.py** (this) contains the Blueprint definition "auth" to be imported into the route files.

Contains logic for authentication routes in the following files:
- **routes_profile.py**: contains api endpoint of account management (change email, reset password, etc)
- **routes_session.py**: contains api endpoint of core authentication functionality (login, logout, get user from session)
- **routes_registration.py**: contains api endpoint of account existence (signup, delete account, verify account)
- **schemas.py**: json schemas to validate client request data expected from auth routes
- **helpers.py**: helper functions used in routes

"""

from flask import Blueprint

auth = Blueprint("auth", __name__) 

# Import routes
from . import routes_profile, routes_session, routes_registration, routes_recovery