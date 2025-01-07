"""
**ABOUT THIS FILE**

auth/email_helpers_credential_change.py contains helper functions that send auth-related email to users.
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
EMAIL_CHANGE_REQUEST = "emails/auth_credential_change/email_change_request.html"
CHANGE_EMAIL_SUCCESS = "emails/auth_credential_change/email_change_success.html"


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

####################################
#    CHANGE OF ACCT EMAIL TOKEN    #
####################################

def send_email_change_token_emails(
    user_name: str,
    old_email: str,
    new_email: str,
    url_old_email: str,
    url_new_email: str,
    token_url_old_email: str,
    token_url_new_email: str,
    token_old_email: str,
    token_new_email: str,
    ) -> bool:
    """
    Sends email change confirmation links to both the old and new email addresses.

    This function sends emails to confirm a user's request to change their account email address.
    Two emails are sent:
    1. To the current (old) email address, requiring confirmation to initiate the change.
    2. To the new email address, requiring confirmation to finalize the change.

    Proper email credentials must be configured in the application's settings or the `.env` file for the emails to be sent successfully.

    Parameters:
        user_name (str): The name of the user to personalize the emails.
        old_email (str): The user's current email address.
        new_email (str): The email address the user wants to switch to.
        url_old_email (str): The URL for more information or actions related to the old email confirmation.
        url_new_email (str): The URL for more information or actions related to the new email confirmation.
        token_url_old_email (str): The secure link sent to the old email for confirmation.
        token_url_new_email (str): The secure link sent to the new email for confirmation.
        token_old_email (str): A unique token for the old email confirmation.
        token_new_email (str): A unique token for the new email confirmation.

    Returns:
        bool: 
            - `True` if both emails are sent successfully.
            - `False` if any email fails to send.

    Example:
        ```python
        success = send_email_change_token_emails(
            user_name="John Doe",
            old_email="old.email@example.com",
            new_email="new.email@example.com",
            url_old_email="https://example.com/verify-old-email",
            url_new_email="https://example.com/verify-new-email",
            token_url_old_email="https://example.com/verify-old-email?token=abc123",
            token_url_new_email="https://example.com/verify-new-email?token=xyz456",
            token_old_email="abc123",
            token_new_email="xyz456",
        )

        if success:
            print("Emails sent successfully.")
        else:
            print("Failed to send emails.")
        ```

    Notes:
        - Email credentials must be correctly configured in `EMAIL_CREDENTIALS`.
        - This function uses Flask's `render_template` to generate the email body and a configured mail object for sending emails.
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False

    msg_1 = "After confirming the change, you still need to verify the new email address so that the changes can take place."
    msg_2 = "If you confirm the change this will become the new email associated with your account. You will also be required to confirm the change through a link sent to the email address that has been associated with your account so far. Please contact support in case you lost access to your original email account."

    def get_html_body (num):
        """num == 0 means old_email, num == 1 is new_email"""
        msg = msg_1 if num == 0 else msg_2
        token_url = token_url_old_email if num == 0 else token_url_new_email
        url = url_old_email if num == 0 else url_new_email
        token = token_old_email if num == 0 else token_new_email
        email_body = render_template(
            EMAIL_CHANGE_REQUEST,  # email template name
            user_name=user_name,
            more_info = msg,
            btn_link=token_url,
            change_email_link = url,
            token= token
        )
        return email_body
    
    # Sending email to both old and new accounts
    with mail.connect() as conn:
        for num in range(2):
            recipient = old_email if num == 0 else new_email
            the_html = get_html_body(num)
            msg = EmailMessage(
                subject = f"{APP_NAME} Email change requested ",
                sender = EMAIL_CREDENTIALS["email_address"],
                html = the_html,
                recipients = [recipient]
            )
            try:
                conn.send(msg)
                logging.debug(f"Email sent to: {recipient}")
            except Exception as e:
                logging.error(f"Could not send email to {recipient}. Error: {e}")

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

    def get_html_body (num):
            """num == 0 means old_email, num == 1 is new_email"""
            msg = msg_1 if num == 0 else msg_2
            email_body = render_template(
                CHANGE_EMAIL_SUCCESS,  # email template name
                user_name=user_name,
                more_info = msg,
            )
            return email_body
        
    # Sending email to both old and new accounts
    with mail.connect() as conn:
        for num in range(2):
            recipient = old_email if num == 0 else new_email
            the_html = get_html_body(num)
            msg = EmailMessage(
                subject = f"{APP_NAME} Email change successfull",
                sender = EMAIL_CREDENTIALS["email_address"],
                html = the_html,
                recipients = [recipient]
            )
            try:
                conn.send(msg)
                logging.debug(f"Email sent to: {recipient}")
            except Exception as e:
                logging.error(f"Could not send email to {recipient}. Error: {e}")










