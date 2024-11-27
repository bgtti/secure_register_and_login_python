"""
**ABOUT THIS FILE**

auth/routes_account.py contains routes responsible for account management functionalities related to authentication.
Here you will find the following routes:
- **change_user_name** route
- **change_email** route #TODO
- **change_password** route #TODO
- **reset_password** route #TODO

The format of data sent by the client is validated using Json Schema. 
Reoutes receiving client data are decorated with `@validate_schema(name_of_schema)` for this purpose. 

------------------------
## More information

This app relies on Flask-Login (see `app/extensions`) to handle authentication. It provides user session management, allowing us to track user logins, manage sessions, and protect routes.

Checkout the docs for more information about how Flask-Login works: https://flask-login.readthedocs.io/en/latest/#configuring-your-application

"""
import logging
from flask import Blueprint, request, jsonify, session
from flask_login import login_user as flask_login_user, current_user, logout_user as flask_logout_user, login_required
from app.extensions.extensions import flask_bcrypt, db, limiter, login_manager
from app.models.user import User
from app.models.token import Token
from app.utils.constants.enum_class import TokenPurpose, modelBool
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.utils.detect_html.detect_html import check_for_html
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.profanity_check.profanity_check import has_profanity
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper
from app.utils.token_utils.group_id_creation import get_group_id
from app.utils.token_utils.sign_and_verify import verify_signed_token
from app.utils.token_utils.verification_urls import create_verification_url
from app.routes.auth.schemas import change_name_schema, req_auth_change_schema, req_token_validation_schema
from app.routes.auth.helpers import is_good_password, get_hashed_pw
from app.routes.auth.email_helpers import send_pw_change_email, send_email_change_emails, send_email_change_sucess_emails, send_pw_change_sucess_email
from . import auth

# CHAGE USER'S NAME
@auth.route("/change_user_name", methods=["POST"])
@login_required
@validate_schema(change_name_schema)
@limiter.limit("10/day")
def change_user_name(): # TODO --> Add to logs so user actions can show in history
    """
    change_user_name() -> JsonType
    ----------------------------------------------------------

    Route changes the name associated with the user's account. 
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "user" value only included if response is "success".

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "user": {
                    "name": "John", 
                    "email": "john@email.com",
                    "access": "user"
                    }, 
            }
    ``` 
    """
    # Standard error response
    error_response = {"response": "There was an error changing user's name."}

    # Get the JSON data from the request body
    json_data = request.get_json()
    new_name = json_data["new_name"]

    the_user = User.query.filter_by(email=current_user.email).first()
    old_name = the_user.name

    try:
        the_user.name = new_name
        db.session.commit()
        logging.info(f"User {current_user.email} name changed from {old_name} to {new_name}.")
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"User could not change name. Error: {e}")
        return jsonify(error_response), 500

    flag = False

    html_in_name = check_for_html(new_name, "auth - change_user_name", current_user.email)
    if html_in_name:
        flag = "YELLOW"
        the_user.flag_change(flag)
    else:
        profanity_in_name = has_profanity(new_name) 
        if profanity_in_name:
            flag = "PURPLE"
            the_user.flag_change(flag)
    
    if flag:
            the_user.flag_change(flag)
            db.session.commit()

    response_data ={
            "response":"success",
            "user": {
                "access": the_user.access_level.value, 
                "name": the_user.name, 
                "email": the_user.email},
        }
    return jsonify(response_data)

# REQUEST TO CHAGE USER'S  EMAIL OR PASSWORD (STEP 1)
@auth.route("/request_auth_change", methods=["POST"]) # TODO: TEST
@login_required
@validate_schema(req_auth_change_schema)
@limiter.limit("5/day")
def request_auth_change(): # TODO --> Add to logs so user actions can show in history, consider db rollbacks
    """
    **request_auth_change() -> JsonType**

    ----------------------------------------------------------
    Route receives the request to change a user's login credential (email or password)
    and sends email(s) with verification url(s) to the user. 
    
    Returns Json object containing strings:
    - "response" value is always included.  
    - "mail_sent" boolean value only included if response is "success".

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "mail_sent": True, 
            }
    ``` 
    """
    # Standard error response
    error_response = {"response": "There was an error changing the user's credentials."}

    # Get the JSON data from the request body
    json_data = request.get_json()
    change_request_type = json_data["type"]
    user_agent = json_data.get("user_agent", "")

    client_ip = get_client_ip(request)

    user = User.query.filter_by(email=current_user.email).first()

    if change_request_type == "password":
        try:
            token = Token(user_id=user.id, purpose=TokenPurpose.PW_CHANGE, ip_address=client_ip, user_agent=user_agent) 
            db.session.add(token)
            db.session.commit()

        except Exception as e:
            logging.error(f"Token creation failed. Error: {e}")
            return jsonify(error_response), 500
        
        link = create_verification_url(token.token, TokenPurpose.PW_CHANGE)
        mail_sent = send_pw_change_email(user.name, link, user.email)
    
    elif change_request_type == "email":
        new_email = json_data["new_email"]
        if new_email is None:
            return jsonify({"response": "New email is required."}), 400
        try:
            user.new_email = new_email
            token_group = get_group_id(user.id)
            # logging.debug(f"Creating token for EMAIL_CHANGE_OLD_EMAIL with purpose: {TokenPurpose.EMAIL_CHANGE_OLD_EMAIL}")
            token_old_email = Token(user_id=user.id, group_id=token_group, purpose=TokenPurpose.EMAIL_CHANGE_OLD_EMAIL, ip_address=client_ip, user_agent=user_agent) 
            # logging.debug(f"Creating token for EMAIL_CHANGE_NEW_EMAIL with purpose: {TokenPurpose.EMAIL_CHANGE_NEW_EMAIL}")
            token_new_email = Token(user_id=user.id, group_id=token_group, purpose=TokenPurpose.EMAIL_CHANGE_NEW_EMAIL, ip_address=client_ip, user_agent=user_agent) 
            db.session.add(token_old_email)
            db.session.add(token_new_email)
            db.session.commit()
        except Exception as e:
            logging.error(f"New email/Token could not be added to user. Error: {e}")
            return jsonify(error_response), 500
        link_old_email = create_verification_url(token_old_email.token, TokenPurpose.EMAIL_CHANGE_OLD_EMAIL)
        link_new_email = create_verification_url(token_new_email.token, TokenPurpose.EMAIL_CHANGE_NEW_EMAIL)
        mail_sent = send_email_change_emails(user.name, link_old_email, link_new_email, user.email, new_email)
    else:
        return jsonify(error_response), 400
    
    response_data ={
            "response":"success",
            "mail_sent": mail_sent,
        }
    return jsonify(response_data)

# VALIDATE TOKEN TO CHAGE USER'S  EMAIL OR PASSWORD (STEP 2)
@auth.route('/request_token_validation', methods=['GET']) # TODO: TEST and improve logging, consider db rollbacks
@limiter.limit("5/day")
@validate_schema(req_token_validation_schema)
def request_token_validation(token):
    """
    request_token_validation() -> JsonType 

    ----------------------------------------------------------
    Validate a token to change the user's email or password.
    
    Returns:
        JsonType: Response JSON containing:
            - "response": String status of the operation ("success" or error message).
            - "cred_changed": Boolean indicating if auth credentials were changed.
            - "signed_token": String echo of the input token.
            - "purpose": String echo purpose of the token. One of: TokenPurpose.value
            - "email_sent": Boolean whether a success email was sent to user or not

    ----------------------------------------------------------
    **Response example:**

    ```python
        response_data = {
                "response":"success",
                "cred_changed": True, 
                "signed_token": "knslsknskns27t21o....", 
                "purpose": "pw_change",
                "email_sent": True
            }
    ``` 
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    signed_token = json_data["signed_token"]
    purpose = json_data["purpose"]

    # Standard error response
    error_response = {
        "response": "Invalid or expired token.",
        "cred_changed": False,
        "signed_token": signed_token,
        "purpose": purpose,
        "email_sent": False
        }

    token_purpose = TokenPurpose(purpose) 

    # Verify token signature and timestamp
    token = verify_signed_token(signed_token, token_purpose)

    if not token:
        logging.info(f"Invalid or expired token could not be validated.")
        return jsonify(error_response), 400 #=> TODO: make sure front end displays this correctly
    
    # Fetch the token from the database
    try:
        the_token =Token.query.filter_by(token=token).first()
    except Exception as e:
        logging.error(f"Database error while fetching token. Error: {e}")
        return jsonify(error_response), 500

    if not the_token:
        logging.info(f"Token not found in the database.")
        return jsonify(error_response), 400 #=> TODO: make sure front end displays this correctly
    
    # Validate token
    if the_token.validate_token() is False:
        logging.info(f"Token validation failed.")
        return jsonify(error_response), 400 #=> TODO: make sure front end displays this correctly
    
    # Token validated, now take appropriate action
    credentials_changed = False
    email_sent = False

    # Case: password change
    if token_purpose == TokenPurpose.PW_CHANGE:
        new_pw = json_data["new_password"]
        if not new_pw:
            logging.error(f"No new password provided in request. Failed to change password.")
            return jsonify(error_response), 400  
        
        try: 
            user = the_token.user
            new_pw_hashed = get_hashed_pw(new_pw, user.created_at, user.salt)
            if not new_pw_hashed:
                logging.error(f"Password in request does not meet standards.")
                return jsonify(error_response), 400
            
            user.password = new_pw_hashed
            db.session.delete(the_token)
            db.session.commit()
            credentials_changed = True
            email_sent = send_pw_change_sucess_email(user.name, user.email)
        except Exception as e:
            logging.error(f"Failed to change password. Error: {e}")
            return jsonify(error_response), 500
        
    # Case: email change    
    else:
        related_tokens = Token.query.filter_by(group_id=the_token.group_id).all()
        if len(related_tokens) != 2:
            logging.error(f"Invalid number of related tokens for group_id: {the_token.group_id}. 2 are required for email changes")
            return jsonify(error_response), 500
        
        second_token = next((t for t in related_tokens if t != the_token), None)
        if not second_token:
            logging.error(f"Second token not found for group_id: {the_token.group_id}.")
            return jsonify(error_response), 500
        
        if second_token.token_verified == modelBool.TRUE:
            # User has validated both required tokens and may now change emails
            try: 
                user = the_token.user
                new_email = user.new_email
                old_email = user.email
                email_was_changed = user.change_email() 

                if email_was_changed:
                    db.session.delete(the_token)
                    db.session.delete(second_token)
                    db.session.commit()
                    email_sent = send_email_change_sucess_emails(user.name, old_email, new_email)
                    credentials_changed = True
                else:
                    logging.error(f"Email change failed. Possible reason: no new_email stored in User.")
                    return jsonify(error_response), 500
            except Exception as e:
                logging.error(f"Failed to change email. Error: {e}")
                return jsonify(error_response), 500

    response_data ={
                "response":"success",
                "cred_changed": credentials_changed,
                "signed_token": signed_token,
                "purpose": purpose,
                "email_sent": email_sent
            }
    return jsonify(response_data), 200