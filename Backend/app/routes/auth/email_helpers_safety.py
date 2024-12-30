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
MFA_ENABLED = "emails/auth_safety/mfa_enabled.html"
MFA_DISABLED = "emails/auth_safety/mfa_disabled.html"

####################################
#      ACCT EMAIL VERIFICATION     #
####################################

def send_acct_verification_sucess_email(user_name: str, user_email: str) -> bool:
    """
    Sends an email to inform the user about successful email verification.

    This function notifies the user via email that their email verification was successful. 
    The email is sent to the user's verified email address.

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

####################################
#    MFA ENABLE/DISABLE EMAIL      #
####################################

def send_email_mfa_set(user_name: str, user_email: str, mfa_enabled: bool) -> bool:
    """
    Sends an email to inform the user about successfully enabling or disabling MFA.

    This function notifies the user via email that they have set MFA in their account. 
    The email is sent to the user's verified email address.

    -----------------------------------------------------------------------------
    **Parameters:**
        user_name (str): The name of the user to be addressed in the email.
        user_email (str): The email address of the user to send the notification to.
        mfa_enabled (bool): True if mfa was enabled, False otherwise

    **Returns:**
        - `True` if the email was sent successfully.
        - `False` if the email sending failed.
    
    -----------------------------------------------------------------------------
    **Example usage:**
    ```python
        user_name = "John Doe"
        user_email = "john.doe@example.com"
        success = send_email_mfa_set(user_name, user_email, True)
        if success:
            print("MFA enabled success email sent!")
        else:
            print("Failed to send the MFA enabled success email.")
    ```
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False
    
    template = MFA_ENABLED if mfa_enabled else MFA_DISABLED # email template name
    email_subject = "enabled" if mfa_enabled else "disabled"

    email_body = render_template(
        template, 
        user_name=user_name,
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} MFA {email_subject}.",
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