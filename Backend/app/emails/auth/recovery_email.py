"""
**ABOUT THIS FILE**

auth/email_helpers_recovery.py contains helper functions that send auth-related email to users.
"""
import logging
from flask import render_template
from flask_mail import Message as EmailMessage
from utils.print_to_terminal import print_to_terminal
from app.extensions.extensions import mail
from config.values import EMAIL_CREDENTIALS
from app.constants.auth_otp_and_mfa import SECURITY_CODE_VALIDITY_MINUTES

# TODO: Name of app appears in email title. Perhaps should be mainstreamed by including it in a top-level file and importing
APP_NAME = "[SafeDev]"

# Templates for emails
REQ_SET_RECOVERY_EMAIL = "emails/auth_recovery/recovery_email_req_set.html"
CHANGE_OF_RECOVERY_EMAIL = "emails/auth_recovery/recovery_email_changed.html"
RECOVERY_EMAIL_SET = "emails/auth_recovery/recovery_email_set.html"
RECOVERY_EMAIL_DELETED = "emails/auth_recovery/recovery_email_deleted.html"


####################################
#   REQUEST SET RECOVERY EMAIL     #
####################################
def send_recovery_email_req_set_email(user_name: str, recipient_email: str, code: str) -> bool:
    """
    Sends an email with security code to a recovery email address - used to verify the recovery email in order to set it.
    Will return True if email was successfully sent and false otherwise.

    The email credentials must be correctly set up in the 
    `.env` file or the application's configuration for this to work.

    -----------------------------------------------------------------------------
    
    :param user_name (str): The name of the user to be addressed in the email.
    :param recipient_email (str): The new recovery email address of the recipient.
    :param code (str): The security code for resetting the user's password.
    
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False

    email_body = render_template(
        REQ_SET_RECOVERY_EMAIL ,  # email template name
        user_name=user_name,
        code_expiry=SECURITY_CODE_VALIDITY_MINUTES,
        code = code
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Request to set recovery email",
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
#       SET RECOVERY EMAIL         #
####################################

def send_recovery_email_changed_email(user_name: str, recipient_email: str, new_recovery_email: str) -> bool:
    """
    Sends an email saying the recovery email address has been changed for the account.
    Will return True if email was successfully sent and false otherwise.

    The email credentials must be correctly set up in the 
    `.env` file or the application's configuration for this to work.

    -----------------------------------------------------------------------------
    
    :param user_name (str): The name of the user to be addressed in the email.
    :param recipient_email (str): The email address of the recipient.
    :param new_recovery_email(str): The new recovery email set to the user's account.
    
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False

    email_body = render_template(
        CHANGE_OF_RECOVERY_EMAIL ,  # email template name
        user_name=user_name,
        new_recovery_email = new_recovery_email
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Recovery email changed",
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


def send_recovery_email_set_email(user_name: str, recipient_email: str, new_recovery_email: str) -> bool:
    """
    Sends an email saying the recovery email address has been set for the account.
    Can be sent to the recovery email address set, or to the user's account email.
    Will return True if email was successfully sent and false otherwise.

    The email credentials must be correctly set up in the 
    `.env` file or the application's configuration for this to work.

    -----------------------------------------------------------------------------
    
    :param user_name (str): The name of the user to be addressed in the email.
    :param recipient_email (str): The email address of the recipient.
    :param new_recovery_email(str): The new recovery email set to the user's account.
    
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False

    email_body = render_template(
        RECOVERY_EMAIL_SET,  # email template name
        user_name=user_name,
        new_recovery_email = new_recovery_email
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Recovery email set",
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
#      DELETE RECOVERY EMAIL       #
####################################
def send_email_recovery_deletion(user_name: str, acct_email: str, old_recovery_email: str) -> None:
    """
    Sends emails to inform the user about deleting a recovery email successfully.

    Notification emails are sent to both the account and recovery email addresses.

    -----------------------------------------------------------------------------

    :param user_name (str): The name of the user to be addressed in the emails.
    :param acct_email (str): The user's main email address.
    :param old_recovery_email (str): The user's recovery email address.
    
    -----------------------------------------------------------------------------
    **Example usage:**
    ```python
        user_name = "John Doe"
        acct_email = "acct.mail@example.com"
        old_recovery_email = "recover.acct.mail@example.com"

        send_email_recovery_deletion(user_name, acct_email, old_recovery_email)
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False

    # Sending email to both email accounts
    with mail.connect() as conn:
        for num in range(2):
            recipient = acct_email if num == 0 else old_recovery_email
            msg = EmailMessage(
                subject = f"{APP_NAME} Recovery email address removed ",
                sender = EMAIL_CREDENTIALS["email_address"],
                html = render_template(
                    RECOVERY_EMAIL_DELETED, # email template name 
                    user_name=user_name,
                    acct_email=acct_email,
                    old_recovery_email = old_recovery_email,
                ),
                recipients = [recipient]
            )
            try:
                conn.send(msg)
                logging.debug(f"Email sent to: {recipient}")
            except Exception as e:
                logging.error(f"Could not send email to {recipient}. Error: {e}")
