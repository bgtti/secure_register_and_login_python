"""
**ABOUT THIS FILE**

values.py centralizes all important constants needed in config files, manage.py, or even functions inside the app.

These values are derived from an .env file if it exist, if it does't, from .env.default if it exists, and it case it also does not, default values will be assigned. 
"""
from config.value_setter import ENVIRONMENT_OPTIONS, CURRENT_ENVIRONMENT, CURRENT_PEPPER, CURRENT_KEY, CURRENT_SERIALIZER_KEY, CURRENT_SUPER_USER, CURRENT_EMAIL_CREDS, BASE_URLS, CORS_ACCEPT_ORIGINS, CRYPTO_KEY

ENVIRONMENT_OPTIONS = ENVIRONMENT_OPTIONS
"""`ENVIRONMENT_OPTIONS = ["local", "development", "production"]`"""

ENVIRONMENT = CURRENT_ENVIRONMENT
"""`ENVIRONMENT` could have one of the following values: "local", "development", or "production". 

It's value should be equal to that of `FLASK_ENV` set in an env file. If not given or set to a value different from the options listed in `ENVIRONMENT_OPTIONS`, "local" will be used as the default.

--------------------
**OPTIONS**

**"local"** => the app will be configured for a development environment. The main difference between "local" and "development is that the environment variables used will be hard-coded defaults and for this reason, the email functionality will not work. Certain Terminal warning will also not be shown - as this environment was only created to allow for quick first-time setup.

**"development"** =>  the app will be configured for a development environment. Certain variables should be present in an env file for the app to be properly functional. Terminal warnings have been set up to guide what is missing prior to deploying this project to production. The database will also be seeded to help with testing.

**"production"** =>  the app will be configured for a production environment. Certain variables should be present in an env file for the app to be properly functional. This should only be done after properly adjusting the configuration in the config_prod file (*which currently only contains placeholder configuration*)
""" 

SECRET_KEY = CURRENT_KEY
"""`SECRET_KEY` should be a string value pulled from an env file. If none is given, a default value is used. Required value to initiate flask.""" 

SERIALIZER_SECRET_KEY = CURRENT_SERIALIZER_KEY
"""`SERIALIZER_SECRET_KEY` should be a string value pulled from an env file. If none is given, a default value is used. Required value to initiate itsdangerous (used to sign tokens).""" 

SUPER_USER = CURRENT_SUPER_USER
"""`SUPER_USER` is a dictionary containing the following keys: name, email, and password. Their values are imported from an env file (if it exists and contains values for `SUPER_ADMIN_NAME`, `SUPER_ADMIN_EMAIL`, and `SUPER_ADMIN_PASSWORD`) or defaults are assigned otherwise. 

Example:

    "SUPER_USER": {
        "name": "John Doe",
        "email": "fakemail@admin.com",
        "password": "thisShouldBeSafeEnough!389k&abt"
    }
""" 

EMAIL_CREDENTIALS = CURRENT_EMAIL_CREDS
"""`EMAIL_CREDENTIALS` is a dictionary containing the following keys: email_address: str, email_password: str, and email_set: bool. 

email_address and email_password are imported from an env file (if it exists) or defaults are assigned otherwise. Should defaults be assigned, "email_set" will be set to False.

Example:

    "EMAIL_CREDENTIALS": {
        "email_address": "email@example.com",
        "email_password": "aSafePw4EmailHerePlease00916gTz",
        "email_set": False
    }

--------------------
**WARNING:**

These values are required so that the email functionality of this app works.
Set `EMAIL_ADDRESS` and `EMAIL_PASSWORD` in an env file. Should these values not be present, the app will not be able to send emails ("email_set" will be set to False). Should the credentials be in the env file, but invalid, "email_set" will be set to True but attempting to use the message functionality may cause errors.

*Flask-Mail is configured in the base configuration to be used with gmail. You can re-configure it to work with any other server, but the credentials should be valid.*
""" 

PEPPER = CURRENT_PEPPER
"""`PEPPER` is a list of 6 4-character long strings. It's value should be derived from an env file. If none is given (or value is not accepted), a default value is used.

Example:

    PEPPER = ["&Yz1", "X$Z2", "z£@5", "3F29", "7*yx", "Y8zp"]

--------------------
**WARNING:**

`PEPPER` is used in authentication. 

*Changing the values in the list while having registered users will cause authentication issues for these users if the authentication logic is not adapted to handle the change beforehand. This is added to the user's password (along with the salt), and the hashed version of that is added to the db. Possible solutions would be: ask the users to change their passwords (and save the new hash logic) OR store the PEPPER used for that users in the db model to bridge the change in the authentication process.*
""" 

BASE_URLS = BASE_URLS
"""`BASE_URLS` is a dictionary containing the following keys: frontend: str, and backend: str. 

These are used to configure the app and generate links throughout the application and do not contain trailing slashes.

Example:

    "BASE_URLS": {
        "frontend": "http://localhost:5173",
        "backend": "http://localhost:5000"
    }

--------------------
**INFO:**

These values are required for running the app. You can define url for local development in value_setter.py, and urls for development and production environments in an env file, like so: 
- `DEV_URL_FRONTEND="http://localhost:5173"`
- `DEV_URL_BACKEND="http://localhost:5173"`
- `PROD_URL_FRONTEND="https:..."`
- `PROD_URL_BACKEND="https:..."`
""" 

CORS_ORIGINS = CORS_ACCEPT_ORIGINS
"""`CORS_ORIGINS` is an array containing strings. This should be used to accept requests from URLs that are allowed to use the api.

In local development, these are: ["http://localhost:5173", "http://127.0.0.1:5173"]

--------------------
**INFO:**
This should be used when initiating the flask cors extension in app > __init__.py

"""

# NOTE it would be best to set the base (and any) url in a shared env or json file -- along with the relative paths for both FE and BE apps -- so as to keep one source of truth. hardcoding links is a bad idea.

ENCRYPTION_KEY = CRYPTO_KEY
"""`ENCRYPTION_KEY` should be a string value pulled from an env file. If none is given, a default value is used. Required value to encrypt/decrypt certain database values.""" 