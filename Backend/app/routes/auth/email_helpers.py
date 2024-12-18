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
CHANGE_AUTH_CRED = "emails/change_auth_creds.html"
CHANGE_AUTH_CRED_SUCCESS = "emails/change_auth_creds_success.html"
OTP = "emails/otp.html"
RECOVERY_EMAIL_ADDED = "emails/recovery_email_added.html"
USER_EXISTS = "emails/user_exists.html"
VERIFY_EMAIL = "emails/verify_email.html"
VERIFY_EMAIL_SUCCESS = "emails/verify_email_success.html"

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
#      ACCT EMAIL VERIFICATION     #
####################################

def send_acct_verification_req_email(user_name: str, verification_url: str, recipient_email: str) -> bool:
    """
    Sends an account verification email to the specified recipient.

    This function generates and sends an email containing a secure verification link for the user 
    to verify their email account. It requires the email credentials to be correctly set up 
    in the `.env` file or the application's configuration.

    -----------------------------------------------------------------------------
    **Parameters:**
        user_name (str): The name of the user to be addressed in the email.
        verification_url (str): The secure verification URL to include in the email.
        recipient_email (str): The email address of the recipient.

    **Returns:**
        - `True` if the email was sent successfully.
        - `False` if the email sending failed.
    
    -----------------------------------------------------------------------------
    **Example usage:**
    ```python
        user_name = "John Doe"
        verification_url = "https://example.com/verify?token=abc123"
        recipient_email = "john.doe@example.com"
        success = send_acct_verification_req_email(user_name, verification_url, recipient_email)
        if success:
            print("Verification email sent successfully!")
        else:
            print("Failed to send verification email.")
    ```
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False
    
    url_link = verification_url

    email_body = render_template(
        VERIFY_EMAIL,  # email template name
        user_name=user_name,
        btn_link=url_link
    )
    new_email = EmailMessage(
        subject = f"{APP_NAME} Email verification request.",
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
#      CHANGE OF ACCT PASSWORD     #
####################################

def send_pw_change_email(user_name: str, verification_url: str, recipient_email: str) -> bool:
    """
    Sends a password reset email to the specified recipient.

    This function generates and sends an email containing a secure link for the user 
    to reset their password. The email credentials must be correctly set up in the 
    `.env` file or the application's configuration for this to work.

    -----------------------------------------------------------------------------
    **Parameters:**
        user_name (str): The name of the user to be addressed in the email.
        verification_url (str): The secure URL for resetting the user's password.
        recipient_email (str): The email address of the recipient.

    **Returns:**
        - `True` if the email was sent successfully.
        - `False` if the email sending failed.
    
    -----------------------------------------------------------------------------
    **Example usage:**
    ```python
        user_name = "John Doe"
        recipient_email = "john.doe@example.com"
        verification_url = "https://example.com/reset-password?token=abc123"
        success = send_pw_change_email(user_name, verification_url, recipient_email)
        if success:
            print("Password reset email sent successfully!")
        else:
            print("Failed to send password reset email.")
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

####################################
#        CHANGE OF ACCT EMAIL      #
####################################

def send_email_change_emails(
    user_name: str,
    verification_url_old_email: str,
    verification_url_new_email: str,
    old_email: str,
    new_email: str,
    ) -> bool:
    """
    Sends email change confirmation links to both the old and new email addresses.

    This function generates and sends emails to confirm the user's request to change
    their account email address. The confirmation links are sent to both the old and
    new email accounts. Proper email credentials must be configured in the `.env` file 
    or the application's settings for the emails to be sent successfully.

    -----------------------------------------------------------------------------
    **Parameters:**
        user_name (str): The name of the user to be addressed in the emails.
        verification_url_old_email (str): The secure confirmation link sent to the old email address.
        verification_url_new_email (str): The secure confirmation link sent to the new email address.
        old_email (str): The user's current email address.
        new_email (str): The email address the user wants to change to.

    **Returns:**
        - `True` if both emails were sent successfully.
        - `False` if sending any of the emails failed.
    
    -----------------------------------------------------------------------------
    **Example usage:**
    ```python
        user_name = "John Doe"
        old_email = "old.email@example.com"
        new_email = "new.email@example.com"
        verification_url_old_email = "https://example.com/verify-old-email?token=abc123"
        verification_url_new_email = "https://example.com/verify-new-email?token=xyz456"

        success = send_email_change_emails(
            user_name,
            verification_url_old_email,
            verification_url_new_email,
            old_email,
            new_email,
        )

        if success:
            print("Email change confirmation emails sent successfully!")
        else:
            print("Failed to send email change confirmation emails.")
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

def send_email_change_sucess_emails(user_name: str, old_email: str, new_email: str) -> bool:
    """
    Sends emails to inform the user about a successful email address change.

    This function notifies the user that their account's email address has been successfully 
    changed. Notification emails are sent to both the old and new email addresses for confirmation.

    -----------------------------------------------------------------------------
    **Parameters:**
        user_name (str): The name of the user to be addressed in the emails.
        old_email (str): The user's previous email address.
        new_email (str): The user's updated email address.

    **Returns:**
        - `True` if both emails were sent successfully.
        - `False` if sending any of the emails failed.
    
    -----------------------------------------------------------------------------
    **Example usage:**
    ```python
        user_name = "John Doe"
        old_email = "old.email@example.com"
        new_email = "new.email@example.com"

        success = send_email_change_sucess_emails(user_name, old_email, new_email)

        if success:
            print("Email change success emails sent successfully!")
        else:
            print("Failed to send email change success emails.")
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False


    msg_1 = "This email address is no longer associated with your account. You can now log in using your new email address."
    msg_2 = "You can now log in using this email address."

    def send_mail(msg, recipient):
        email_body = render_template(
            CHANGE_AUTH_CRED_SUCCESS, # email template name 
            user_name=user_name,
            auth_type="email",
            more_info = msg,
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
    email_2_sent = send_mail(msg_2, new_email)
    
    if email_1_sent and email_2_sent:
        return True

    return False

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
#       RECOVERY EMAIL SETUP       #
####################################

def send_email_recovery_set(user_name: str, acct_email: str, recovery_email: str) -> bool:
    """
    Sends emails to inform the user about setting a recovery email successfully.

    Notification emails are sent to both the account and recovery email addresses.

    -----------------------------------------------------------------------------
    **Parameters:**
        user_name (str): The name of the user to be addressed in the emails.
        acct_email (str): The user's main email address.
        recovery_email (str): The user's recovery email address.

    **Returns:**
        - `True` if both emails were sent successfully.
        - `False` if sending any of the emails failed.
    
    -----------------------------------------------------------------------------
    **Example usage:**
    ```python
        user_name = "John Doe"
        acct_email = "acct.mail@example.com"
        recovery_email = "recover.acct.mail@example.com"

        success = send_email_change_sucess_emails(user_name, acct_email, recovery_email)

        if success:
            print("Emails sent successfully!")
        else:
            print("Failed to send emails.")
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False


    def send_mail(recipient):
        email_body = render_template(
            RECOVERY_EMAIL_ADDED, # email template name 
            user_name=user_name,
            acct_email=acct_email,
            recovery_email = recovery_email,
        )
        email_message = EmailMessage(
            subject = f"{APP_NAME} Recovery email set ",
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
    email_1_sent = send_mail(acct_email)
    email_2_sent = send_mail(recovery_email)
    
    if email_1_sent and email_2_sent:
        return True

    return False