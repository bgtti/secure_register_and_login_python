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
RESET_PW = "emails/auth_credential_change/password_reset.html"
CHANGE_PASSWORD_SUCCESS = "emails/auth_credential_change/password_change_success.html"


####################################
#       RESET PASSWORD TOKEN      #
####################################

def send_pw_reset_email(user_name: str, recipient_email: str, url: str, token_url:str, token:str) -> bool:
    """
    Sends a password reset email to the specified recipient.

    This function generates and sends an email containing a secure link for the user 
    to reset their password. The email credentials must be correctly set up in the 
    `.env` file or the application's configuration for this to work.

    -----------------------------------------------------------------------------
    **Parameters:**
        user_name (str): The name of the user to be addressed in the email.
        recipient_email (str): The email address of the recipient.
        url (str): The URL for resetting the user's password, without the token ending (token=...).
        token_url (str): The secure URL for resetting the user's password, the token ending (token=...).
        token (str): The token.

    **Returns:**
        - `True` if the email was sent successfully.
        - `False` if the email sending failed.
    
    -----------------------------------------------------------------------------
    **Example usage:**
    ```python
        user_name = "John Doe"
        recipient_email = "john.doe@example.com"
        url = "https://example.com/reset-password"
        token_url = "https://example.com/reset-password/token=abc123"
        token = "abc123"
        success = send_pw_change_email(user_name, recipient_email, url, token_url, token)
        if success:
            print("Password reset email sent successfully!")
        else:
            print("Failed to send password reset email.")
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False

    email_body = render_template(
        RESET_PW,  # email template name
        user_name=user_name,
        btn_link=token_url,
        reset_pw_link = url,
        token = token
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Password reset request",
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

####################################
#      CHANGE OF ACCT PASSWORD     #
####################################

def send_pw_change_sucess_email(user_name: str, user_email: str) -> bool:
    """
    Sends an email to inform the user about a successful password change.

    This function notifies the user via email that their password has been successfully changed.
    Proper email credentials must be configured in the `.env` file or application settings for the email to be sent successfully.

    -----------------------------------------------------------------------------
    **Parameters:**
        user_name (str): The name of the user to be addressed in the email.
        user_email (str): The email address of the user to send the notification to.

    **Returns:**
        - `True` if the email was sent successfully.
        - `False` if the email sending failed.
    
    -----------------------------------------------------------------------------
    **Example usage:**
    ```python
        user_name = "John Doe"
        user_email = "john.doe@example.com"

        success = send_pw_change_sucess_email(user_name, user_email)

        if success:
            print("Password change success email sent successfully!")
        else:
            print("Failed to send password change success email.")
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False


    email_body = render_template(
        CHANGE_PASSWORD_SUCCESS, # email template name
        user_name=user_name,
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












