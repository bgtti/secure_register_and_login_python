"""
**ABOUT THIS FILE**
TODO
contains helper functions that send auth-related email to users.
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
CHANGE_PASSWORD_SUCCESS = "emails/auth_credential_change/password_change_success.html"
CHANGE_CREDENTIAL_BLOCK = "emails/auth_credential_change/credential_change_block.html"
RESET_PW_REQUEST = "emails/auth_credential_change/password_reset.html"
EMAIL_CHANGE_REQUEST = "emails/auth_credential_change/email_change_request.html"
CHANGE_EMAIL_SUCCESS = "emails/auth_credential_change/email_change_success.html"


####################################
#      CHANGE OF ACCT PASSWORD     #
####################################

def send_pw_change_success_email(user_name: str, user_email: str) -> bool:
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


def send_cred_change_block_email(user_name: str, user_email: str, failed_attempts:str) -> bool:
    """
    Sends an email to inform the user about being bocked from chaging email or password.
    Returns True if email sent successfully and False otherwise.

    -----------------------------------------------------------------------------

    :param user_name: the name of the user to be addressed in the email. (user.name)
    :param user_email: the email address of the user to send the notification to.(user.email)
    :param failed_attempts: number of credential change failed attempts. (user.auth_change_attempts)
    
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False


    email_body = render_template(
        CHANGE_CREDENTIAL_BLOCK, # email template name
        user_name=user_name,
        failed_attempts=failed_attempts
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Temporarily blocked from changing credentials",
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
#       RESET PASSWORD REQUEST     #
####################################

def send_pw_reset_request_email(user_name: str, recipient_email: str, code: str) -> bool:
    """
    Sends a password reset email to the specified recipient containing a security code.
    Will return True if email was successfully sent and false otherwise.

    The email credentials must be correctly set up in the 
    `.env` file or the application's configuration for this to work.

    -----------------------------------------------------------------------------
    
    user_name (str): The name of the user to be addressed in the email.
    recipient_email (str): The email address of the recipient.
    code (str): The security code for resetting the user's password.
    
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False

    email_body = render_template(
        RESET_PW_REQUEST,  # email template name
        user_name=user_name,
        code_expiry=SECURITY_CODE_VALIDITY_MINUTES,
        code = code
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
#      CHANGE OF ACCT EMAIL        #
####################################

def send_email_reset_request_email(user_name: str, recipient_email: str, code: str) -> bool:
    """
    Sends an email to reset the account email to the specified recipient containing a security code.
    Will return True if email was successfully sent and false otherwise.

    The email credentials must be correctly set up in the 
    `.env` file or the application's configuration for this to work.

    -----------------------------------------------------------------------------
    
    user_name (str): The name of the user to be addressed in the email.
    recipient_email (str): The email address of the recipient.
    code (str): The security code for resetting the user's password.
    
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False

    email_body = render_template(
        EMAIL_CHANGE_REQUEST ,  # email template name
        user_name=user_name,
        code_expiry=SECURITY_CODE_VALIDITY_MINUTES,
        code = code
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Email change request",
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



def send_email_change_success_email(user_name: str, recipient_email: str, old_email: str, new_email: str) -> bool:
    """
    Sends emails to inform the user about a successful email address change.
    Old and new email address will be included in the email body. Returns True if email was send successfully and False otherwise.

    -----------------------------------------------------------------------------
        user_name (str): The name of the user to be addressed in the emails.
        recipient_email (str): The email address of the recepient.
        old_email (str): The user's previous email address.
        new_email (str): The user's updated email address.
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False

    email_body = render_template(
        CHANGE_EMAIL_SUCCESS,  # email template name
        user_name=user_name,
        old_email=old_email,
        new_email=new_email
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Email changed successfully.",
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











