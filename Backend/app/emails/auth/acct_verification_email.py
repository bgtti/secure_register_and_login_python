"""
**ABOUT THIS FILE**

auth/email_helpers_safety.py contains helper functions that send auth-related email to users.
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
VERIFY_EMAIL_SUCCESS = "emails/auth_safety/verify_email_success.html"


####################################
#      ACCT EMAIL VERIFICATION     #
####################################

def send_acct_verification_success_email(user_name: str, user_email: str) -> bool:
    """
    Sends an email to inform the user about successful email verification.

    This function notifies the user via email that their email verification was successful. 
    The email is sent to the user's verified email address.

    -----------------------------------------------------------------------------

        :param user_name (str): The name of the user to be addressed in the email.
        :param user_email (str): The email address of the user to send the notification to.

    **Returns:**
        - `True` if the email was sent successfully.
        - `False` if the email sending failed.
    
    -----------------------------------------------------------------------------
    **Example usage:**
    ```python
        user_name = "John Doe"
        user_email = "john.doe@example.com"
        success = send_acct_verification_sucess_email(user_name, user_email)
        if success:
            print("Account verification success email sent!")
        else:
            print("Failed to send the account verification success email.")
    ```
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False

    email_body = render_template(
        VERIFY_EMAIL_SUCCESS, # email template name
        user_name=user_name,
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Account verified successfully.",
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