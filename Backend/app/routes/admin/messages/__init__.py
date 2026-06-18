"""
**Messages Blueprint**

admin/messages/__init__.py registers the route's blueprint.

This module handles the serving of messages received from users of the site, including:

- ... TODO
- ... TODO
- ... TODO

In this module:
- **routes.py**: the main file, which contains the api routes and consumes the content of all other 'helper' files in the module
- **schemas.py**: json schemas to validate client request data  

"""
from flask import  Blueprint

# Blueprint
messages = Blueprint('messages', __name__)

# Import routes to attach them to this blueprint
from app.routes.admin.messages import routes 