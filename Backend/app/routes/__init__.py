"""
**The app/routes package**

Holds all api endpoints, subdivided into directories holding the names of the blueprints registered in them.

Sub-directories will include a `routes.py` file with the blueprint registration and api endpoints. 
They may also include and a `schemas.py` to validade json data received from the client and/or a `helpers.py` to include some specific logic that a route may need.
Some sub-directories might be further sub-divided.

"""