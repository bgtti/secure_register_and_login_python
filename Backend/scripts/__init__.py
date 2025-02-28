"""
**The scripts package**

Contains the files necessary to set up the application.

--------------------------------------
**setup.py** contains the functions necessary to set up the application.

**initial_setup(environment)**: Should be called in **manage.py** when creating the flask app. It will call a function to create the super admin account and, when the environment is not "production", it will also check if redis is running and also seed the database for testing purposes.
"""