"""
**ABOUT THIS FILE**

auth/email_helpers.py contains helper functions that send auth-related email to users.
"""
import logging
from flask import render_template
from flask_mail import Message as EmailMessage
from utils.print_to_terminal import print_to_terminal
from app.extensions.extensions import mail
from config.values import EMAIL_CREDENTIALS

# TODO: Name of app appears in email title. Perhaps should be mainstreamed by including it in a top-level file and importing
APP_NAME = "[SafeDev]"

# Templates for emails
ACCOUNT_CREATED = "emails/auth_registration/account_created.html"
USER_EXISTS = "emails/auth_registration/user_exists.html"
ACCOUNT_DELETED = "emails/auth_registration/account_deleted.html"

####################################
#     ACCOUNT CREATED SUCCESS      #
####################################
def send_email_acct_created(user_name: str, recipient_email: str) -> None:
    """
    Sends the user a an email confirming the account creation.

    -----------------------------------------------------------------------------
    **Parameters:**
        user_name (str): The name of the user to be addressed in the email.
        recipient_email (str): The email address of the recipient.
    ```
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
    
    email_body = render_template(
        ACCOUNT_CREATED,  # email template name
        user_name=user_name,
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Account created successfully!",
        sender = EMAIL_CREDENTIALS["email_address"],
        recipients = [recipient_email]
    )
    new_email.html = email_body

    try:
        mail.send(new_email)
    except Exception as e:
        logging.error(f"Could not send email. Error: {e}")

    logging.info(f"Message sent to email.")


####################################
#    CANNOT SIGNUP: ACCT EXISTS    #
####################################
def send_email_acct_exists(user_name: str, recipient_email: str) -> None:
    """
    Sends the user a reminder that his account is already registered in the system: reason signup not possible.

    This function generates and sends an email containing this information.

    -----------------------------------------------------------------------------
    **Parameters:**
        user_name (str): The name of the user to be addressed in the email.
        recipient_email (str): The email address of the recipient.
    ```
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
    
    email_body = render_template(
        USER_EXISTS,  # email template name
        user_name=user_name,
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Attempted signup failed: account already registered",
        sender = EMAIL_CREDENTIALS["email_address"],
        recipients = [recipient_email]
    )
    new_email.html = email_body

    try:
        mail.send(new_email)
    except Exception as e:
        logging.error(f"Could not send email. Error: {e}")

    logging.info(f"Message sent to email.")

####################################
#      ACCOUNT DELETED SUCCESS     #
####################################

def send_email_acct_deleted(user_name: str, recipient_email: str) -> None:
    """
    Sends the user a an email confirming the account deletion.

    -----------------------------------------------------------------------------
    **Parameters:**
        user_name (str): The name of the user to be addressed in the email.
        recipient_email (str): The email address of the recipient.
    ```
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
    
    email_body = render_template(
        ACCOUNT_DELETED,  # email template name
        user_name=user_name,
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Account deleted successfully!",
        sender = EMAIL_CREDENTIALS["email_address"],
        recipients = [recipient_email]
    )
    new_email.html = email_body

    try:
        mail.send(new_email)
    except Exception as e:
        logging.error(f"Could not send email. Error: {e}")

    logging.info(f"Message sent to email.")