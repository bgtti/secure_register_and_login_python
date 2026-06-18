"""
Docstring for Backend.app.services.user_auth_service

Contains:

- OTP generation and validation
- MFA first and second factor operations
- session reset logic
- email verification workflow
"""

# Python/Flask libraries
import logging
from datetime import datetime, timezone
# Extensions
from app.extensions.extensions import db
from sqlalchemy.exc import IntegrityError # for DB race condition
# Models
from app.models.user import User

# Constants
from app.constants.flags import Flag

# Utilities
from app.common.detect_html.detect_html import check_for_html
from app.common.ip_utils.ip_anonymization import anonymize_ip
from app.common.ip_utils.ip_geolocation import geolocate_ip
from app.common.profanity_check.profanity_check import has_profanity
from app.common.user_credential_helpers.name_validation import user_name_is_valid
from app.common.salt_and_pepper.helpers import generate_salt, get_pepper
from app.common.user_credential_helpers.password_validation_and_hash import get_hashed_pw
from app.common.enum_helpers.map_string_to_enum import map_string_to_enum


# TODO: inform user of failed login attempts


def svc_register_user(name: str, email: str, password: str) -> dict:
    """
    Function in `services/auth/user_acct_registration_service.py`.
    Creates a user and commits changes to the DB.

    **This function will do the following:** 
    - Check validity of user's name against a list of reserved names
    - Check strength of password (against common password list and repeated characters through *get_hashed_pw*)
    - Create salt and hash password
    - Check if email already exists in DB
    - Create User in the DB ( and commit to it)
    - Flag users if appropriate (html and profanity detection)

    **What this service does not do:**
    - It does not create a new user session: user.new_session() is not called
    - It does not send emails informing about user creation
    - It does not send the newly created User in the response
    - It does not check the validity of email addresses, character constraints in names and passwords: this is expected to happen at JSON Schema level
    - Does not raise error if committing to db fails. If this happens, log_code will be 500.

    --------
    **Fields overview**:

    :param name: name as given by user
    :param email: email as given by user
    :param password: unhashed password, as given by user

    **Returns**:
    
    dict: dictionary containing information useful for security logs. Keys:

        - success: (bool) whether user was created (True) or not (False)
        - user_already_exists: (bool) whether email already exists in DB (True) or not (False)
        - user_id: (int) will be 0 if user creation fails and user does not exist already in DB
        - log_code: (int) containing code relevant for security log
        - log_text: (str) information for logs

    --------
    **Example usage**:
    ```
    user_creation = svc_register_user("John", "john@example.com", "agdgskgGGjoe555")
    
    user_creation -> {
        "success": True,
        "user_already_exists": False,
        "user_id": 5,
        "user_name":"John"
        "log_code": 200,
        "log_text": "" 
    }
    ```
    """
    # Prepare response
    res = {
        "success": False,
        "user_already_exists": False,
        "user_id": 0,
        "user_name": "",
        "log_code": 500,
        "log_text": "",
    }

    # Check if user exists
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            res["user_already_exists"] = True
            res["user_id"] = user.id
            res["user_name"] = user.name
            res["log_code"] = 409
            res["log_text"] = f"User {email} is already registered."
            logging.info(f"svc_register_user found User in DB. Email: {email}. Registration failed.")
            return res
    except Exception as e:
        logging.error(f"Could not check if user {email} exists in db: {e}")
        res["log_text"] = f"Could not verify whether user {email} already exists."
        return res
    
    # Check if name is valid
    if user_name_is_valid(name) is False:
        res["log_code"] = 400
        res["log_text"] = f"Name does not meet criteria. Name: {name}. {email} account creation rejected."
        logging.info(f"svc_register_user rejected user name. Name: {name}. Registration failed.")
        return res
    
    # Check if password is valid
    date = datetime.now(timezone.utc) # date is required to get apropriate Pepper value
    salt = generate_salt()
    hashed_password = get_hashed_pw(password, date, salt) # will be None if password does not meet criteria
    if not hashed_password:
        res["log_code"] = 400
        res["log_text"] = f"Password does not meet criteria. Account could not be created for {email}."
        logging.info(f"svc_register_user rejected password. Name: {name}. Registration failed.")
        return res
    
    # Check for flags: profanity or html in input
    flag = None
    html_in_name = check_for_html(name, "signup - name field", email)
    html_in_email = check_for_html(email, "signup - email field", email)

    if html_in_email or html_in_name:
        flag = "YELLOW"
    else:
        profanity_in_name = has_profanity(name) 
        profanity_in_email = has_profanity(email)
        if profanity_in_name or profanity_in_email:
            flag = "PURPLE"

    # Create user
    try:
        new_user = User(name=name, email=email, password=hashed_password, salt=salt, created_at=date) # passing on the creation date to make sure it is the same used for pepper
        db.session.add(new_user)
        if flag:
            flag_colour = flag.lower()
            new_flag = map_string_to_enum(flag_colour, Flag)
            if new_flag is not None:
                new_user.flagged = new_flag
            else:
                logging.error(f"User flag could not be changed when registering user: wrong input for flag_change: {flag_colour}. Check UserFlag Enum for options.")
        db.session.commit()
        logging.info(f"User account created successfully. Id = {new_user.id}.")
        if flag:
            logging.info(f"User id = {new_user.id} has been flagged: {new_user.flagged.value} by the system.")
    except IntegrityError:
        db.session.rollback()
        res["user_already_exists"] = True
        res["log_code"] = 409
        res["log_text"] = f"User {email} is already registered (race condition)."
        return res
    except Exception as e:
        db.session.rollback() 
        logging.error(f"User registration failed for email {email}. Error: {e}")
        res["log_text"] = f"User could not be created for Name: {name}, Email: {email}"
        return res
    
    # Prepare successful response
    res["success"] = True
    res["user_id"] = new_user.id
    res["user_name"] = new_user.name
    if flag:
        res["log_code"] = 207
        if html_in_name or html_in_email:
            res["log_text"] = f"Flag assigned by system: Html detected in name or email. Name: {name}, Email: {email}"
        else:
            res["log_text"] = f"Flag assigned by system: Profanity detected in name or email. Name: {name}, Email: {email}"
    else:
        res["log_code"] = 200
    
    return res


