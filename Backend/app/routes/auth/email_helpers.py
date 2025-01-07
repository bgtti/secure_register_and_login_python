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
BLOCKED_BY_ADMIN_REMINDER = "emails/blocked_by_admin_reminder.html"
OTP = "emails/otp.html"

####################################
#      ONE-TIME PASSWORD / OTP     #
####################################

def send_otp_email(user_name: str, otp: str, recipient_email: str) -> bool:
    """
    Sends a one-time password (OTP) email to the specified recipient.

    This function generates and sends an email containing the provided OTP to the recipient's 
    email address. It uses an HTML template to format the email body. Proper email credentials 
    must be configured in the application's settings for this to work.

    -----------------------------------------------------------------------------
    **Parameters:**
        user_name (str): The name of the user to be addressed in the email.
        otp (str): The one-time password to include in the email.
        recipient_email (str): The email address of the recipient.

    **Returns:**
        - `True` if the email was sent successfully.
        - `False` if the email sending failed.
    
    -----------------------------------------------------------------------------
    **Example usage:**
    ```python
        user_name = "John Doe"
        otp = "123456"
        recipient_email = "john.doe@example.com"

        success = send_otp_email(user_name, otp, recipient_email)

        if success:
            print("OTP email sent successfully!")
        else:
            print("Failed to send OTP email.")
    ```
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False
    
    email_body = render_template(
        OTP,  # email template name
        user_name=user_name,
        otp=otp
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} One-Time Password",
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
#  CANNOT LOGIN: BLOCKED BY ADMIN  #
####################################

def send_email_admin_blocked(user_name: str, recipient_email: str) -> None:
    """
    Sends the user a reminder that his account has been blocked by an admin.

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
        BLOCKED_BY_ADMIN_REMINDER,  # email template name
        user_name=user_name,
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Account blocked by site admin",
        sender = EMAIL_CREDENTIALS["email_address"],
        recipients = [recipient_email]
    )
    new_email.html = email_body

    try:
        mail.send(new_email)
    except Exception as e:
        logging.error(f"Could not send email. Error: {e}")

    logging.info(f"Message sent to email.")


