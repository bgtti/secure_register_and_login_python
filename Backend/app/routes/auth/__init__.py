"""
**Auth Blueprint/Package**

This file contains the auth blueprint definition and registers the blueprints from its modules.

This package contains authentication-related modules, including:
- Credential change: routes that enable user to change credentials (password, email)
- Profile: routes that enable user to change profile (name)
- Recovery: routes that enable user to set/change/delete account recovery data (recovery email)
- Registration: routes that handle account's existence status (signup, delete account)
- Safety: account verification and safety-related routes (verify email, enable MFA)
- Session: routes that authenticate a session (login, logout, otp request)

Utility/helper files may be used by multiple route files.

**auth/__init__.py** (this) contains the Blueprint definition "auth" to be imported into the route files.

It also contains:
- **schemas.py**: json schemas to validate client request data expected from auth routes
- **helpers_email**: directory containing files with functions that send email to users, triggered from auth routes
- **helpers_general**: directory containing files with helper functions used in routes

"""

from flask import Blueprint

# auth = Blueprint('auth', __name__, url_prefix="/auth") NOTE url prefix is ommitted here, but set in app's init
auth = Blueprint('auth', __name__)

from app.routes.auth.credential_change import credential_change
from app.routes.auth.profile import profile
from app.routes.auth.recovery import recovery
from app.routes.auth.registration import registration
from app.routes.auth.safety import safety
from app.routes.auth.session import session

auth.register_blueprint(credential_change, url_prefix='/credential_change')
auth.register_blueprint(profile, url_prefix='/profile')
auth.register_blueprint(recovery, url_prefix='/recovery')
auth.register_blueprint(registration, url_prefix='/registration')
auth.register_blueprint(safety, url_prefix='/safety')
auth.register_blueprint(session, url_prefix='/session')