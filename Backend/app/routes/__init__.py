"""
**The app/routes package**

Holds all api endpoints, subdivided into directories holding the names of the blueprints registered in them.

Sub-directories will include a `routes.py` file with the blueprint registration and api endpoints. 
They may also include and a `schemas.py` to validade json data received from the client and/or a `helpers.py` to include some specific logic that a route may need.
Some sub-directories might be further sub-divided.

"""
#TODO: this file could include a blueprint registration function (see bellow)

"""
Define a Function to Register All Blueprints

in app/routes/__init__.py
from flask import Flask
from app.routes.auth import auth
from app.routes.admin import admin

def register_blueprints(app: Flask):
    #Register all blueprints for the application.
    app.register_blueprint(auth, url_prefix="/api/auth")
    app.register_blueprint(admin, url_prefix="/api/admin")

in app/__init__.py
from app.routes import register_blueprints

def create_app():
    app = Flask(__name__)
    register_blueprints(app)  # Registers all routes
    return app
"""

