import ast
from colorama import Fore
from app.utils.console_warning.print_warning import console_warn
# The functions in this file are meant to be used in the config file.
# They check whether the proper key-value pairs exist in an .env file and, if so, if they are set properly. If they are not set or no .env exists, they set defaults to the required values.
# They print a warning in the terminal about missing data in the .env

def pepper_array(pepper_str_array):
    """
    pepper_array(pepper_str_array: str) -> str
    ---------------------------------------------------------
    Checks whether there is an env variable PEPPER and, if 
    so, if it is formatted correctly. 
    PEPPER should be a string array with 6 4-char-long values

    Returns:
        The argument, if valid or a default array if not
    ---------------------------------------------------------
    Example usage:

    in config.py:
    PEPPER_STRING_ARRAY = pepper_array(os.getenv('PEPPER'))
    """
    DEFAULT_PEPPER = '["&Yz1", "X$Z2", "z£@5", "3F29", "7*yx", "Y8zp"]'
    if pepper_str_array:
        try:
            pepper_array = ast.literal_eval(pepper_str_array)
            if not isinstance(pepper_array, list) or len(pepper_array) != 6:
                raise ValueError("PEPPER must have exactly 6 values.")
        except (ValueError, SyntaxError, TypeError):
            return DEFAULT_PEPPER
        return pepper_str_array
    else:
        console_warn("Set PEPPER in a .env file before using this app in production.", "MAGENTA")
        return DEFAULT_PEPPER

def secret_key(key_string):
    """
    secret_key(key_string: str) -> str
    ---------------------------------------------------------
    Checks whether there is an env variable SECRET_KEY.

    Returns:
        The argument, if valid or a default key if not.
    ---------------------------------------------------------
    Example usage:

    in config.py:
    SECRET = secret_key(os.getenv('SECRET_KEY'))
    """
    if key_string:
        return key_string
    else:
        console_warn("Set SECRET_KEY in a .env file before using this app in production.", "MAGENTA")
        return "unsafeSecretKey"

def admin_credentials(cred_str_array):
    """
    admin_credentials(cred_str_array: str) -> str
    ---------------------------------------------------------
    Checks whether there is an env variable ADMIN_CREDENTIALS 
    and, if so, if it is formatted correctly. 
    ADMIN_CREDENTIALS should be a string array with 3 values:
    '["admin_name", "admin_email", "admin_password"]'

    Returns:
        The argument, if valid or a default array if not
    ---------------------------------------------------------
    Example usage:

    in config.py:
    ADMIN_ACCT = admin_credentials(os.getenv('ADMIN_CREDENTIALS))
    """
    DEFAULT_CRED = '["Super Admin", "super@admin", "lad678Ut$G"]'
    if cred_str_array:
        try:
            cred_array = ast.literal_eval(cred_str_array)
            if not isinstance(cred_array, list) or len(cred_array) != 3:
                raise ValueError("ADMIN_CREDENTIALS must have exactly 3 values.")
        except (ValueError, SyntaxError, TypeError):
            return DEFAULT_CRED
        return cred_str_array
    else:
        console_warn("Set ADMIN_CREDENTIALS in a .env file before using this app in production.", "MAGENTA")
        return DEFAULT_CRED

def user_id_salt(id_salt):
    """
    user_id_salt(id_salt: str) -> int
    ---------------------------------------------------------
    Checks whether there is an env variable USER_ID_SALT 
    and, if so, if it is formatted correctly. 
    USER_ID_SALT should be a string with 3 ints:
    '123'.

    Returns:
        The argument as int, if valid or a default string int if not
    ---------------------------------------------------------
    Example usage:

    in config.py:
    USER_ID_SALT = user_id_salt(os.getenv('USER_ID_SALT))
    """
    DEFAULT_CRED = 203
    if id_salt:
        if id_salt.isnumeric():
            try:
                id_salt_int = int(id_salt)
                if id_salt_int > 99 and id_salt_int < 1000:
                    return id_salt_int
                else:
                    raise ValueError("USER_ID_SALT must be a 3-digit integer string.")
            except (ValueError, SyntaxError, TypeError):
                return DEFAULT_CRED
    else:
        console_warn("Set USER_ID_SALT in a .env file before using this app in production.", "MAGENTA")
        return DEFAULT_CRED
    
def email_credentials(email_address, password):
    """
    email_credentials(email_addres: str, password: str) -> obj
    ---------------------------------------------------------
    Checks whether there is an env variable EMAIL_ADDRESS and EMAIL_PASSWORD. 
    When these variables are set, email functionality can be used.

    Returns:
        Object with dummie credentials
    ---------------------------------------------------------
    Example usage:

    in config.py:
    EMAIL_CREDENTIALS = email_credentials(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
    """
    EMAIL_CREDENTIALS = {
        "email_address": "email@example.com",
        "email_password": "email_password",
        "email_set": False
    }
    if email_address and password:
        EMAIL_CREDENTIALS["email_address"] = email_address
        EMAIL_CREDENTIALS["email_password"] = password
        EMAIL_CREDENTIALS["email_set"] = True
        return EMAIL_CREDENTIALS
    else:
        console_warn("Set EMAIL_ADDRESS and EMAIL_PASSWORD in a .env file before using this app in production.", "MAGENTA")
        return EMAIL_CREDENTIALS