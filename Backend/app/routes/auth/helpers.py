"""
**ABOUT THIS FILE**

auth/helpers.py contains the following helper function(s):

- **is_good_password**: 
- **login_schema** 

------------------------
## More information

These schemas are passed in to `validate_schema` (see `app/utils/custom_decorators/json_schema_validator.py`) through the route's decorator to validate client data received in json format by comparing it to the schema rules.

"""
import re
from app.utils.constants.account_constants import MOST_COMMON_PASSWORDS
import logging
from flask_mail import Message as EmailMessage
from utils.print_to_terminal import print_to_terminal
from config.values import EMAIL_CREDENTIALS, BASE_URLS
from app.extensions.extensions import mail
from flask import render_template

# TODO: hardcoded links are a bad idea. The urls bellow should be transfered to a common file used by both FE and BE
BE_URL = BASE_URLS["backend"]
FE_URL = BASE_URLS["frontend"]

# TODO: build FE pages
LINK_CONFIRM_EMAIL_CHANGE_OLD = f"{FE_URL}/confirmEmailChange"
LINK_CONFIRM_EMAIL_CHANGE_NEW = f"{FE_URL}/confirmNewEmail"
LINK_CONFIRM_PASSWORD_CHANGE = f"{FE_URL}/setNewPw"

# TODO: Name of app appears in email title. Perhaps should be mainstreamed by including it in a top-level file and importing
APP_NAME = "[SafeDev]"



def is_good_password(password):
    """
    is_good_password(password: str) -> bool
    ---------------------------------------

    Defines whether a password is weak or strong.
    It will search it in a list of most common passwords and check for character repetition.

    **Returns:**
        - `False` if password is weak.
        - `True` if password is strong.
    ---------------------------------------
    **Example usage:**
    ```python
        password_to_check = "SecurePassword123"
        if is_good_password(password_to_check):
            print("Password is valid!")
        else:
            print("Password is invalid.")
    ```
    """
    # Check for sequential repetition
    sequential_repetition_pattern = r"(\S)\1{3,}"  # Matches any character repeated 4 or more times
    if re.search(sequential_repetition_pattern, password):
        return False

    # Check for common passwords only if the password is 15 characters or less
    if len(password) <= 15 and any(common_password in password for common_password in MOST_COMMON_PASSWORDS):
        return False

    # If the password passes both checks, it is considered valid
    return True


def send_pw_change_email(user_name, token, recipient_email):
    """
    send_pw_change_email(user_name: str, token: str, recipient_email: str) -> bool
    -----------------------------------------------------------------------------

    Function sends user an email with the link to securely reset their password.
    Email will only be sent if email credentials were set up in the .env file correctly.

    -----------------------------------------------------------------------------
    Returns True if email sending succeeded and False otherwise.
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False
    
    verification_link = f"{LINK_CONFIRM_PASSWORD_CHANGE}/{token}" 


    email_body = render_template(
        'change_auth_creds.html',  # email template name
        user_name=user_name,
        auth_type="password",
        more_info = "By confirming the change you will be directed to a link where you can reset your password.",
        btn_link=verification_link
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Password change request.",
        sender = EMAIL_CREDENTIALS["email_address"],
        recipients = [recipient_email]
    )
    new_email.html = email_body

    try:
        mail.send(new_email)
    except Exception as e:
        logging.error(f"Could not send email. Error: {e}")
        return False

    logging.info(f"Message sent to email.")

    return True

def send_email_change_emails(user_name, token, new_email_token, old_email, new_email):
    """
    send_email_change_emails(user_name: str, token: str, new_email_token: str, old_email: str, new_email: str) -> bool
    -----------------------------------------------------------------------------

    Function sends user an email with the link to confirm they want to change their account email to both the old and new email accounts.
    Email will only be sent if email credentials were set up in the .env file correctly.

    -----------------------------------------------------------------------------
    Returns True if email sending succeeded and False otherwise.
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False
    
    link_1 = f"{LINK_CONFIRM_EMAIL_CHANGE_OLD}{token}" 
    link_2 = f"{LINK_CONFIRM_EMAIL_CHANGE_NEW}/{new_email_token}" 

    msg_1 = "After confirming the change, you still need to verify the new email address so that the changes can take place."
    msg_2 = "If you confirm the change this will become the new email associated with your account. You will also be required to confirm the change through a link sent to the email address that has been associated with your account so far. Please contact support in case you lost access to your original email account."

    def send_mail(link, msg, recipient):
        email_body = render_template(
            'change_auth_creds.html',  # email template name
            user_name=user_name,
            auth_type="email",
            more_info = msg,
            btn_link=link
        )
        email_message = EmailMessage(
            subject = f"{APP_NAME} Email change requested ",
            sender = EMAIL_CREDENTIALS["email_address"],
            recipients = [recipient]
        )
        email_message.html = email_body

        try:
            mail.send(email_message)
        except Exception as e:
            logging.error(f"Could not send email to {recipient}. Error: {e}")
            return False
        
        logging.info(f"Message sent to {recipient}.")
        return True
    
    # Sending email to both old and new accounts
    email_1_sent = send_mail(link_1, msg_1, old_email)
    email_2_sent = send_mail(link_2, msg_2, new_email)
    
    if email_1_sent and email_2_sent:
        return True

    return False

def send_pw_change_sucess_email(user_name, user_email):
    """
    send_pw_change_email(user_name: str, user_email: str, user_new_email: str) -> bool
    -----------------------------------------------------------------------------

    Function sends user an email informing about a successfull auth credential change.

    -----------------------------------------------------------------------------
    Returns True if email sending succeeded and False otherwise.
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False


    email_body = render_template(
        'change_auth_creds_success.html', 
        user_name=user_name,
        auth_type="email",
        more_info = "You can now log in using your new password.",
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Password changed successfully.",
        sender = EMAIL_CREDENTIALS["email_address"],
        recipients = [user_email]
    )
    new_email.html = email_body

    try:
        mail.send(new_email)
    except Exception as e:
        logging.error(f"Could not send email. Error: {e}")
        return False

    logging.info(f"Message sent to email.")

    return True

def send_email_change_sucess_emails(user_name, old_email, new_email):
    """
    send_pw_change_email(user_name: str, old_email: str, user_new_email: str) -> bool
    -----------------------------------------------------------------------------

    Function sends user an email informing about a successfull auth credential change.

    -----------------------------------------------------------------------------
    Returns True if email sending succeeded and False otherwise.
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False


    msg_1 = "This email address is no longer associated with your account. You can now log in using your new email address."
    msg_2 = "You can now log in using this email address."

    def send_mail(link, msg, recipient):
        email_body = render_template(
            'change_auth_creds_success.html',  
            user_name=user_name,
            auth_type="email",
            more_info = msg,
            btn_link=link
        )
        email_message = EmailMessage(
            subject = f"{APP_NAME} Email change successfull ",
            sender = EMAIL_CREDENTIALS["email_address"],
            recipients = [recipient]
        )
        email_message.html = email_body

        try:
            mail.send(email_message)
        except Exception as e:
            logging.error(f"Could not send email to {recipient}. Error: {e}")
            return False
        
        logging.info(f"Message sent to {recipient}.")
        return True
    
    # Sending email to both old and new accounts
    email_1_sent = send_mail(msg_1, old_email)
    email_2_sent = send_mail( msg_2, new_email)
    
    if email_1_sent and email_2_sent:
        return True

    return False