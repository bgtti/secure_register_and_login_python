"""
**ABOUT THIS FILE**

value_setter.py contains functions used to set values used in values.py - from where they are exported (and used in configuration and elsewhere in the code. 

--------------------
These functions will do the following:
- check if the value is available in an .env file. If not, it will be checked if they are contained in an .env.default file. If they are also not there, a default will be provided.
- the values will be checked for validity (ie: if they comply with the requirements of the app). In case they do not, they will be substituted for a default value which complies with the requirements.
- in the case the any value is missing or was substituted because it was in the wrong format, the user will be informed (unless `ENVIRONMENT` is set to "local"). 

The default values meant to be exported (into value.py) are type-hinted and followed by assert statement which should raise an AssertionError should the value be of another type than the expected.
"""
import ast
import os
from dotenv import load_dotenv, find_dotenv
from typing import Dict, List, Union
from utils.print_to_terminal import print_to_terminal

# Default values

DEFAULT = {
    "SECRET_KEY": "unsafeSecretKey123",
    "SERIALIZER_SECRET_KEY": "anotherUnsafeSecretKeyUsedHere456",
    "SUPER_USER": {
        "name": "Super Admin",
        "email": "super@admin",
        "password": "lad678Ut$G"
    },
    "EMAIL_CREDENTIALS": {
        "email_address": "email@example.com",
        "email_password": "email_password",
        "email_set": False
    },
    "PEPPER": ["&Yz1", "X$Z2", "z£@5", "3F29", "7*yx", "Y8zp"]
}

DEFAULT_URL = {
    "FRONTEND":"http://localhost:5173",
    "BACKEND":"https://localhost:5000"
}

ENVIRONMENT_OPTIONS: List[str] = ["local", "development", "production"]
"""Available environment options: `["local", "development", "production"]`

*If these options change, make sure to represent the changes in values.py, manage.py, and other places the choices in this list are used*
"""

assert isinstance(ENVIRONMENT_OPTIONS, list) and all(isinstance(item, str) for item in ENVIRONMENT_OPTIONS), \
    "ENVIRONMENT_OPTIONS should be a list of strings."

# Load env file variables (if they exist)
load_dotenv(find_dotenv(".env", usecwd=True) or ".env.default")

# Define the current environment
def set_env():
    """
    set_env() -> str
    ------------------------------------------------------

    Returns the value of FLASK_ENV if it exists and is valid 
    (i.e., present in ENVIRONMENT_OPTIONS). Otherwise, returns "local".

    ------------------------------------------------------
    Returns a string like:

    `set_env() #--> "local" or another valid environment string`
    """
    environment = os.getenv("FLASK_ENV", "local") # Default to "local" if FLASK_ENV is not set
    flask_env = environment if environment in ENVIRONMENT_OPTIONS else "local"
    return flask_env

CURRENT_ENVIRONMENT: str = set_env() 

assert isinstance(CURRENT_ENVIRONMENT, str), "CURRENT_ENVIRONMENT should be a string. Check value_setter.py inside the config directory."

# Define the current secret key value.
def set_secret_key():
    """
    set_secret_key() -> str
    ------------------------------------------------------

    Returns the value of SECRET_KEY if it exists in env file. 
    Otherwise, returns a default (DEFAULT["SECRET_KEY"]).

    ------------------------------------------------------
    Returns a string like:

    `set_secret_key() #--> "unsafeSecretKey123"`
    """
    if CURRENT_ENVIRONMENT == "local":
        return DEFAULT["SECRET_KEY"]
    secret = os.getenv("SECRET_KEY")
    if secret:
        return secret
    else:
        print_to_terminal("Set SECRET_KEY in a .env file before using this app in production.", "MAGENTA")
        return DEFAULT["SECRET_KEY"]
    
CURRENT_KEY: str = set_secret_key()

assert isinstance(CURRENT_KEY, str), "CURRENT_KEY should be a string. Check value_setter.py inside the config directory."

# Define the current secret key value.
def set_serializer_secret_key():
    """
    set_serializer_secret_key() -> str
    ------------------------------------------------------

    Returns the value of SERIALIZER_SECRET_KEY if it exists in env file. 
    Otherwise, returns a default (DEFAULT["SERIALIZER_SECRET_KEY"]).
    This value will be used by the itsdangerous extension.

    ------------------------------------------------------
    Returns a string like:

    `set_serializer_secret_key() #--> "unsafeSecretKey123"`
    """
    if CURRENT_ENVIRONMENT == "local":
        return DEFAULT["SERIALIZER_SECRET_KEY"]
    secret = os.getenv("SERIALIZER_SECRET_KEY")
    if secret:
        return secret
    else:
        print_to_terminal("Set SERIALIZER_SECRET_KEY in a .env file before using this app in production.", "MAGENTA")
        return DEFAULT["SERIALIZER_SECRET_KEY"]
    
CURRENT_SERIALIZER_KEY: str = set_serializer_secret_key()

assert isinstance(CURRENT_SERIALIZER_KEY, str), "SERIALIZER_SECRET_KEY should be a string. Check value_setter.py inside the config directory."

# Define the admin credentials.
# Ps: Used to create super admin user
def set_super_admin_creds():
    """
    set_super_admin_creds() -> Dict[str, str]
    ------------------------------------------------------

    Returns a dictionary with the values for SUPER_ADMIN_NAME, SUPER_ADMIN_EMAIL, and SUPER_ADMIN_PASSWORD if these exist in env file. 
    Otherwise, returns a default dictionary (DEFAULT["SUPER_USER"]).

    ------------------------------------------------------
    Returns a dictionary like:
    
    {
        "name": "Super Admin",
        "email": "super@admin",
        "password": "lad678Ut$G"
    }
    """
    if CURRENT_ENVIRONMENT == "local":
        return DEFAULT["SUPER_USER"]
    
    name = os.getenv("SUPER_ADMIN_NAME")
    email = os.getenv("SUPER_ADMIN_EMAIL")
    password = os.getenv("SUPER_ADMIN_PASSWORD")

    if name and email and password:
        if len(password) < 8:
            print_to_terminal("WARNING: SUPER_ADMIN_PASSWORD in the env file is less than 8 characters. For security, it's recommended to set a longer password.", "MAGENTA")
        super_user = {
        "name": name,
        "email": email,
        "password": password
        }
        return super_user
    else:
        print_to_terminal("Set SUPER_ADMIN credentials in a .env file before using this app in production.", "MAGENTA")
        return DEFAULT["SUPER_USER"]

CURRENT_SUPER_USER: Dict[str, str] = set_super_admin_creds()  

assert isinstance(CURRENT_SUPER_USER, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in CURRENT_SUPER_USER.items()), \
    "CURRENT_SUPER_USER should be a dictionary with string keys and string values. Check value_setter.py inside the config directory."

# Define the email credentials.
# Ps: Needed to test and use the email functionality
def set_email_credentials():
    """
    set_email_credentials() -> Dict[str, str]
    ------------------------------------------------------

    Returns a dictionary with the values for `EMAIL_ADDRESS` and `EMAIL_PASSWORD` if these exist in env file and are valid. 
    Otherwise, returns a default dictionary (`DEFAULT["EMAIL_CREDENTIALS"]`).
    The dictionary also contains the key "email_set" which is a boolean. It indicated whether the default credentials are being used or not (False indicates credentials are app's default, and therefore not valid).

    ------------------------------------------------------
    Returns a dictionary like:

    {
        "email_address": "email@example.com",
        "email_password": "email_password",
        "email_set": False
    }
    """
    if CURRENT_ENVIRONMENT == "local":
        return DEFAULT["EMAIL_CREDENTIALS"]
    email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    
    if email and password:
        if email == DEFAULT["EMAIL_CREDENTIALS"]["email_address"] or password == DEFAULT["EMAIL_CREDENTIALS"]["email_password"]:
            print_to_terminal("Invalid credentials: Set valid EMAIL_ADDRESS and EMAIL_PASSWORD values in the env file. Email functionality will not work otherwise.", "MAGENTA")
            return DEFAULT["EMAIL_CREDENTIALS"]
        creds = {
            "email_address": email,
            "email_password": password,
            "email_set": True
        }
        return creds
    else:
        print_to_terminal("Set EMAIL credentials in a .env file before using this app in production.", "MAGENTA")
        return DEFAULT["EMAIL_CREDENTIALS"]

CURRENT_EMAIL_CREDS: Dict[str, Union[str, bool]] = set_email_credentials()

assert isinstance(CURRENT_EMAIL_CREDS["email_address"], str) and \
       isinstance(CURRENT_EMAIL_CREDS["email_password"], str) and \
       isinstance(CURRENT_EMAIL_CREDS["email_set"], bool), \
    "CURRENT_EMAIL_CREDS should have 'email_address' and 'email_password' as strings, and 'email_set' as a boolean. Check value_setter.py inside the config directory."

# Define the current value for pepper.
# Ps: Pepper is used to authenticate the user (create an account & log-in)
def set_pepper():
    """
    set_pepper() -> list[str]
    ------------------------------------------------------

    Returns the value of PEPPER if it exists and is valid. 
    Otherwise, returns a default (DEFAULT["PEPPER"]).

    ------------------------------------------------------
    Example usage:

    `# if in env file: PEPPER ='["&Yz1", "X$Z2", "z£@5", "3F29", "7*yx", "Y8zp"]'`
    
    `set_pepper() #--> ["&Yz1", "X$Z2", "z£@5", "3F29", "7*yx", "Y8zp"]`
    """
    if CURRENT_ENVIRONMENT == "local":
        return DEFAULT["PEPPER"]
    
    pepper = os.getenv("PEPPER")
    if pepper:
        try:
            pepper_array = ast.literal_eval(pepper)
            # if not isinstance(pepper_array, list) or len(pepper_array) != 6: #---> old version
            if not isinstance(pepper_array, list) or len(pepper_array) != 6 or not all(isinstance(item, str) and len(item) == 4 for item in pepper_array):
                print_to_terminal("PEPPER format incorrect in env file. PEPPER must be a string array comprised of 6 4-character-long strings.")
                raise ValueError("PEPPER was assigned an invalid value.")
        except (ValueError, SyntaxError, TypeError):
            print_to_terminal("Default value will be assigned to PEPPER.")
            return DEFAULT["PEPPER"]
        return pepper_array
    else:
        print_to_terminal("Set PEPPER in a .env file before using this app in production.", "MAGENTA")
        return DEFAULT["PEPPER"]

CURRENT_PEPPER: List[str] = set_pepper()

assert isinstance(CURRENT_PEPPER, list), "CURRENT_PEPPER should be a list. Check value_setter.py inside the config directory."
assert len(CURRENT_PEPPER) == 6, "CURRENT_PEPPER should contain exactly 6 items. Check value_setter.py inside the config directory."
assert all(isinstance(item, str) and len(item) == 4 for item in CURRENT_PEPPER), \
    "Each item in CURRENT_PEPPER should be a 4-character string. Check value_setter.py inside the config directory."

# Define the base urls 
def set_base_urls():
    """
    set_base_urls() -> Dict[str, str]
    ------------------------------------------------------

    Returns a dictionary containing the base urls being used in the front and backend apps. 
    If the environment it is running is 'local' or if DEV or PROD urls are not available in the env file, 
    defaults (localhost) will be used.
    Ensures no trailing slashes in the URLs.

    ------------------------------------------------------
    Returns a string like:

    `set_base_urls() #--> {
    "FRONTEND":"http://...",
    "BACKEND":"http://..."
    }`
    """
    fe_url = DEFAULT_URL["FRONTEND"]
    be_url = DEFAULT_URL["BACKEND"]

    if CURRENT_ENVIRONMENT == "development":
        fe_url = os.getenv("DEV_URL_FRONTEND", fe_url)
        be_url = os.getenv("DEV_URL_BACKEND", be_url)
    elif CURRENT_ENVIRONMENT == "production":
        fe_url = os.getenv("PROD_URL_FRONTEND", fe_url)
        be_url = os.getenv("PROD_URL_BACKEND", be_url)

    URLS = {
    "frontend":fe_url.rstrip('/'),
    "backend":be_url.rstrip('/')
    }
    
    return URLS


BASE_URLS: Dict[str, str] = set_base_urls() 

assert isinstance(BASE_URLS["frontend"], str) and \
       isinstance(BASE_URLS["backend"], str), \
    "BASE_URLS should have 'frontend' and 'backend' as strings. Check value_setter.py inside the config directory."

assert BASE_URLS["frontend"].startswith("http"), \
    f"frontend URL should start with 'http': {BASE_URLS['frontend']}, check url format!"
assert BASE_URLS["backend"].startswith("http"), \
    f"backend URL should start with 'http': {BASE_URLS['backend']}, check url format!"

# Generate a cryptographic key
def generate_cripto_key():
    """
    Generate or retrieve a cryptographic key to be used with Fernet.
    If the ENCRYPTION_KEY environment variable is invalid or not set,
    check for or create a 'secret.key' file in the parent directory. 
    """
    encryption_key = os.getenv("ENCRYPTION_KEY", None) 

    from cryptography.fernet import Fernet

    # Step 1: Check if ENCRYPTION_KEY is provided via environment
    if encryption_key:
        try:
            # Verify that the key from the environment is valid for Fernet
            Fernet(encryption_key.encode())
            return encryption_key.encode()
        except Exception as e:
            print_to_terminal(
                "Invalid ENCRYPTION_KEY in environment. Falling back to file-based key.", "YELLOW"
            )
    # Step 2: Check if 'secret.key' exists in the parent directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    key_file_path = os.path.join(os.path.dirname(script_dir), "secret.key")
    if os.path.exists(key_file_path):
        try:
            print_to_terminal("Reading encryption key from existing file...", "CYAN")
            with open(key_file_path, "rb") as key_file:
                key = key_file.read()
                # Validate the key from the file
                Fernet(key)
                return key
        except Exception:
            print_to_terminal(
                "Error with existing secret.key. Recreating a new one...", "YELLOW"
            )
    # Step 3: Create a new key and save it in 'secret.key'
    try:
        print_to_terminal("Creating a new encryption key file...", "CYAN")
        key = Fernet.generate_key()
        with open(key_file_path, "wb") as key_file:
            key_file.write(key)
        print_to_terminal("...secret.key file created. Do not use this in production!", "CYAN")
        return key
    except Exception as e:
        print_to_terminal(f"Error creating secret.key: {e}", "RED")
        raise RuntimeError("Failed to generate an encryption key")
    
CRYPTO_KEY = generate_cripto_key()