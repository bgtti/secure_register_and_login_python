"""
**ABOUT THIS FILE**

auth/email_helpers.py contains the following helper function(s):

- **send_pw_change_email**: 
- **send_email_change_emails** 

------------------------
**Purpose**

These functions send auth-related email to users.
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
CHANGE_AUTH_CRED = "emails/change_auth_creds.html"
CHANGE_AUTH_CRED_SUCCESS = "emails/change_auth_creds_success.html"


def send_pw_change_email(user_name, verification_url, recipient_email):
    """
    **send_pw_change_email(user_name: str, verification_url: str, recipient_email: str) -> bool**

    -----------------------------------------------------------------------------
    Function sends user an email with the link to securely reset their password.
    Email will only be sent if email credentials were set up in the .env file correctly.

    -----------------------------------------------------------------------------
    Returns `True` if email sending succeeded and `False` otherwise.
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False
    
    url_link = verification_url

    email_body = render_template(
        CHANGE_AUTH_CRED,  # email template name
        user_name=user_name,
        auth_type="password",
        more_info = "By confirming the change you will be directed to a link where you can reset your password.",
        btn_link=url_link
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

def send_email_change_emails(user_name, verification_url_old_email, verification_url_new_email, old_email, new_email):
    """
    **send_email_change_emails(user_name: str, verification_url_old_email: str, verification_url_new_email: str, old_email: str, new_email: str) -> bool**

    -----------------------------------------------------------------------------
    Function sends user an email with the link to confirm they want to change their account email to both the old and new email accounts.
    Email will only be sent if email credentials were set up in the .env file correctly.

    -----------------------------------------------------------------------------
    Returns `True` if email sending succeeded and `False` otherwise.
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False
    
    link_1 = verification_url_old_email
    link_2 = verification_url_new_email

    msg_1 = "After confirming the change, you still need to verify the new email address so that the changes can take place."
    msg_2 = "If you confirm the change this will become the new email associated with your account. You will also be required to confirm the change through a link sent to the email address that has been associated with your account so far. Please contact support in case you lost access to your original email account."

    def send_mail(link, msg, recipient):
        email_body = render_template(
            CHANGE_AUTH_CRED,  # email template name
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
    **send_pw_change_email(user_name: str, user_email: str) -> bool**

    -----------------------------------------------------------------------------
    Function sends user an email informing about a successfull auth credential change.

    -----------------------------------------------------------------------------
    Returns `True` if email sending succeeded and `False` otherwise.
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False


    email_body = render_template(
        CHANGE_AUTH_CRED_SUCCESS, # email template name
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
    Returns `True` if email sending succeeded and `False` otherwise.
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False


    msg_1 = "This email address is no longer associated with your account. You can now log in using your new email address."
    msg_2 = "You can now log in using this email address."

    def send_mail(link, msg, recipient):
        email_body = render_template(
            CHANGE_AUTH_CRED_SUCCESS, # email template name 
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