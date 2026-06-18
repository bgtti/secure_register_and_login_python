"""
Sends email containing OTP to user.
TODO: multiple failed login email template missing
"""
import logging
from flask import render_template
from flask_mail import Message as EmailMessage
from utils.print_to_terminal import print_to_terminal
from app.extensions.extensions import mail
from config.values import EMAIL_CREDENTIALS
from app.constants.auth_otp_and_mfa import OTP_VALIDITY_MINUTES

# TODO: Name of app appears in email title. Perhaps should be mainstreamed by including it in a top-level file and importing
APP_NAME = "[SafeDev]"

# Location of email template
OTP_TEMPLATE = "emails/auth/otp.html"
MULTIPLE_FAILED_PW_INPUT_TEMPLATE = "emails/auth/otp.html" #TODO: do the template!

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
        OTP_TEMPLATE,  # email template name
        user_name=user_name,
        otp=otp,
        otp_expiry=OTP_VALIDITY_MINUTES
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
        logging.error(f"Email service could not send OTP email. Error: {e}")
        return False

    logging.info(f"OTP sent to email sucessfully.")

    return True

####################################
#      MULTIPLE WRONG PW INPUT     #
####################################

def send_multiple_failed_pw_input_email(user_name: str, geo_location: str, recipient_email: str) -> bool:
    """
    TODO
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False
    
    print_to_terminal("Email template missing. Could not send email.", "RED")
    #recommend the user changes password as a precaution and enable MFA (if not yet)
    #say account blocked temporarily with increasing time with wrong input pw

    # email_body = render_template(
    #     MULTIPLE_FAILED_PW_INPUT_TEMPLATE,  # TODO
    #     user_name=user_name,
    #     geo_location=geo_location
    # )
    # new_email = EmailMessage(
    #     subject = f"{APP_NAME} Multiple failed login attempts",
    #     sender = EMAIL_CREDENTIALS["email_address"],
    #     recipients = [recipient_email]
    # )
    # new_email.html = email_body

    # try:
    #     mail.send(new_email)
    # except Exception as e:
    #     logging.error(f"Email service could not send wrong password email. Error: {e}")
    #     return False

    # logging.info(f"Failed multiple login warning sent to email sucessfully.")

    return True