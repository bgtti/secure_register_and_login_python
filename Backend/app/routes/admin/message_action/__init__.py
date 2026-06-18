"""
**Admin / Message action Blueprint**

admin/message_action/__init__.py registers the route's blueprint.

Users may contact the site (eg: using contact form).
This module focuses on the handling of those messages.

Admins may take actions such:
- Reply to messages
- Mark messages as spam
- Handle prioritization of messages
- Delete message threads
"""
from flask import  Blueprint

# Blueprint
message_action = Blueprint('message_action', __name__)

# Import routes to attach them to this blueprint
from app.routes.admin.message_action import routes 