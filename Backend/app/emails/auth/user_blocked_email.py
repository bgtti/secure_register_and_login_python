"""
**ABOUT THIS FILE**

TODO
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
BLOCKED_BY_ADMIN_TEMPLATE = "emails/auth/blocked_by_admin_reminder.html"
BLOCKED_BY_SYSTEM_TEMPORARILY = "emails/auth/blocked_temporary_failed_attempts"



####################################
#  CANNOT LOGIN: BLOCKED BY ADMIN  #
####################################

def send_admin_blocked_email(user_name: str, recipient_email: str) -> None:
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
        return
    
    email_body = render_template(
        BLOCKED_BY_ADMIN_TEMPLATE,  # email template name
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

#############################################
#  CANNOT LOGIN: TEMPORARY BLOCK BY SYSTEM  #
#############################################

def send_temporarily_blocked_email(user_name: str, recipient_email: str, wait_time:int, wait_time_measure:str) -> None:
    """
    Sends the user a reminder that his account has been temporarily blocked due to too many failed attempts to log in.

    This function generates and sends an email containing this information.

    -----------------------------------------------------------------------------
    **Parameters:**
        user_name (str): The name of the user to be addressed in the email.
        recipient_email (str): The email address of the recipient.
        wait_time (int): An integer indicating the time (in minutes or seconds) the client has to wait until the block is lifted (eg: `10` or `52`).
        "wait_time_measure" (str): Either "minute", "minutes", "second", or "seconds"
    ```
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return
    
    if wait_time or wait_time_measure is None:
        print_to_terminal("Params wait_time or wait_time_measure is None. Email could not be sent.", "RED")
        logging.info(f"Params wait_time or wait_time_measure is None. Email could not be sent.")
        return
    
    email_body = render_template(
        BLOCKED_BY_SYSTEM_TEMPORARILY,  # email template name
        user_name=user_name,
        wait_time=wait_time,
        wait_time_measure=wait_time_measure
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Account temporarily blocked",
        sender = EMAIL_CREDENTIALS["email_address"],
        recipients = [recipient_email]
    )
    new_email.html = email_body

    try:
        mail.send(new_email)
    except Exception as e:
        logging.error(f"Could not send email. Error: {e}")

    logging.info(f"Message sent to email.")