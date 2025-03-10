"""
**Admin Blueprint/Package**

This file contains the auth blueprint definition and registers the blueprints from its modules.

This package contains authentication-related modules, including:
- Dashboard: routes that provide the admin dashboard's content
- Message action: routes that enable admin to answer/modify/delete messages
- Messages: routes that enable admin to view all messages
- User action: routes that enable edit subscribed users (flag, access type, block, delete)
- Users: routes that enable admins to view user information, logs, and messages

Utility/helper files may be used by multiple route files.

**auth/__init__.py** (this) contains the Blueprint definition "auth" to be imported into the route files.

It also contains:
- **schemas.py**: json schemas to validate client request data expected from auth routes
- **helpers**: directory containing files with helper functions used in routes

"""

from flask import Blueprint

admin = Blueprint('admin', __name__)

from app.routes.admin.dashboard.routes import admin_dash
from app.routes.admin.message_action.routes import message_action
from app.routes.admin.messages.routes import messages
from app.routes.admin.user_action.routes import user_action
from app.routes.admin.users.routes import users

admin.register_blueprint(admin_dash, url_prefix='/dash')
admin.register_blueprint(message_action, url_prefix='/message_action')
admin.register_blueprint(messages, url_prefix='/messages')
admin.register_blueprint(user_action, url_prefix='/user_action')
admin.register_blueprint(users, url_prefix='/users')