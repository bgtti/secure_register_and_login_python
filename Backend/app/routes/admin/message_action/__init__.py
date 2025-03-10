"""
**Message action Blueprint**

admin/message_action/__init__.py registers the route's blueprint.

This module handles the messages received from users of the site, including:

- ... TODO
- ... TODO
- ... TODO

In this module:
- **routes.py**: the main file, which contains the api routes and consumes the content of all other 'helper' files in the module
- **schemas.py**: json schemas to validate client request data 
- **helpers.py**: utility functions used in routes 

"""
from flask import  Blueprint

# Blueprint
message_action = Blueprint('message_action', __name__)

# Import routes to attach them to this blueprint
from app.routes.admin.message_action import routes 