"""
**The app/routes/auth package**

**auth/__init__.py** (this) contains the Blueprint definition "auth" to be imported into the route files.

Contains logic for authentication routes in the following files:
- **routes_credential_change.py**: contains api endpoint to change login credentials (email and password)
- **routes_profile.py**: contains api endpoint of profile management (change the user's name)
- **routes_recovery.py**: contains api endpoint to set, change, and get the user's recovery email address
- **routes_registration.py**: contains api endpoint of account existence (signup, delete account)
- **routes_safety.py**: contains api endpoint related to securing the user's account (email verification and multi-factor authentication (MFA) status)
- **routes_session.py**: contains api endpoint of core authentication functionality (login, logout, get user from session)

It also contains:
- **schemas.py**: json schemas to validate client request data expected from auth routes
- **helpers_email**: directory containing files with functions that send email to users, triggered from auth routes
- **helpers_general**: directory containing files with helper functions used in routes

"""

from flask import Blueprint

auth = Blueprint("auth", __name__) 

# Import routes
from . import routes_credential_change, routes_profile, routes_recovery, routes_registration, routes_safety, routes_session