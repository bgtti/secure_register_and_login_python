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

# TODO: Name of app appears in email title. Perhaps should be mainstreamed by including it in a top-level file and importing
APP_NAME = "[SafeDev]"

# Templates for emails
RECOVERY_EMAIL_ADDED = "emails/auth_recovery/recovery_email_added.html"
RECOVERY_EMAIL_DELETED = "emails/auth_recovery/recovery_email_deleted.html"
RECOVERY_EMAIL_CHANGE = "emails/auth_recovery/recovery_email_changed.html"


####################################
#       SET RECOVERY EMAIL         #
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


    # def send_mail(recipient):
    #     email_body = render_template(
    #         RECOVERY_EMAIL_ADDED, # email template name 
    #         user_name=user_name,
    #         acct_email=acct_email,
    #         recovery_email = recovery_email,
    #     )
    #     email_message = EmailMessage(
    #         subject = f"{APP_NAME} Recovery email set ",
    #         sender = EMAIL_CREDENTIALS["email_address"],
    #         recipients = [recipient]
    #     )
    #     email_message.html = email_body

    #     try:
    #         with mail.connect() as conn:
    #             conn.send(email_message)
    #     except Exception as e:
    #         logging.error(f"Could not send email to {recipient}. Error: {e}")
    #         return False
        
    #     logging.info(f"Message sent to {recipient}.")
    #     return True
    
    # # Sending email to both old and new accounts
    # email_1_sent = send_mail(acct_email)
    # email_2_sent = send_mail(recovery_email)
    
    # if email_1_sent and email_2_sent:
    #     return True

    # return False
    # Sending email to both email accounts
    with mail.connect() as conn:
        for num in range(2):
            recipient = acct_email if num == 0 else recovery_email
            msg = EmailMessage(
                subject = f"{APP_NAME} Recovery email set ",
                sender = EMAIL_CREDENTIALS["email_address"],
                html = render_template(
                        RECOVERY_EMAIL_ADDED, # email template name 
                        user_name=user_name,
                        acct_email=acct_email,
                        recovery_email = recovery_email,
                    ),
                recipients = [recipient]
            )
            try:
                conn.send(msg)
                logging.debug(f"Email sent to: {recipient}")
            except Exception as e:
                logging.error(f"Could not send email to {recipient}. Error: {e}")

####################################
#      DELETE RECOVERY EMAIL       #
####################################
def send_email_recovery_deletion(user_name: str, acct_email: str, old_recovery_email: str) -> bool:
    """
    Sends emails to inform the user about deleting a recovery email successfully.

    Notification emails are sent to both the account and recovery email addresses.

    -----------------------------------------------------------------------------
    **Parameters:**
        user_name (str): The name of the user to be addressed in the emails.
        acct_email (str): The user's main email address.
        old_recovery_email (str): The user's recovery email address.

    **Returns:**
        - `True` if both emails were sent successfully.
        - `False` if sending any of the emails failed.
    
    -----------------------------------------------------------------------------
    **Example usage:**
    ```python
        user_name = "John Doe"
        acct_email = "acct.mail@example.com"
        old_recovery_email = "recover.acct.mail@example.com"

        success = send_email_recovery_deletion(user_name, acct_email, old_recovery_email)

        if success:
            print("Emails sent successfully!")
        else:
            print("Failed to send emails.")
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False


    # def send_mail(recipient):
    #     email_body = render_template(
    #         RECOVERY_EMAIL_DELETED, # email template name 
    #         user_name=user_name,
    #         acct_email=acct_email,
    #         old_recovery_email = old_recovery_email,
    #     )
    #     email_message = EmailMessage(
    #         subject = f"{APP_NAME} Recovery email address removed ",
    #         sender = EMAIL_CREDENTIALS["email_address"],
    #         recipients = [recipient]
    #     )
    #     email_message.html = email_body

    #     try:
    #         mail.send(email_message)
    #     except Exception as e:
    #         logging.error(f"Could not send email to {recipient}. Error: {e}")
    #         return False
        
    #     logging.info(f"Message sent to {recipient}.")
    #     return True
    
    # # Sending email to both old and new accounts
    # email_1_sent = send_mail(acct_email)
    # email_2_sent = send_mail(old_recovery_email)
    
    # if email_1_sent and email_2_sent:
    #     return True

    # return False
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

####################################
#      CHANGE RECOVERY EMAIL       #
####################################
def send_email_recovery_change(user_name: str, acct_email: str, old_recovery_email: str) -> bool:
    """
    Sends emails to inform the user about changing a recovery email successfully.

    Notification emails are sent to both the account and old recovery email addresses.
    No email is sent to the new recovery email address. 

    -----------------------------------------------------------------------------
    **Parameters:**
        user_name (str): The name of the user to be addressed in the emails.
        acct_email (str): The user's main email address.
        old_recovery_email (str): The user's recovery email address.

    **Returns:**
        - `True` if both emails were sent successfully.
        - `False` if sending any of the emails failed.
    
    -----------------------------------------------------------------------------
    **Example usage:**
    ```python
        user_name = "John Doe"
        acct_email = "acct.mail@example.com"
        old_recovery_email = "recover.acct.mail@example.com"

        success = send_email_recovery_change(user_name, acct_email, old_recovery_email)

        if success:
            print("Emails sent successfully!")
        else:
            print("Failed to send emails.")
    """
    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Could not send email.", "RED")
        return False


    # def send_mail(recipient):
    #     email_body = render_template(
    #         RECOVERY_EMAIL_CHANGE, # email template name 
    #         user_name=user_name,
    #         acct_email=acct_email,
    #         old_recovery_email = old_recovery_email,
    #     )
    #     email_message = EmailMessage(
    #         subject = f"{APP_NAME} Recovery email address changed ",
    #         sender = EMAIL_CREDENTIALS["email_address"],
    #         recipients = [recipient]
    #     )
    #     email_message.html = email_body

    #     try:
    #         with mail.connect() as conn:
    #             conn.send(email_message)
    #     except Exception as e:
    #         logging.error(f"Could not send email to {recipient}. Error: {e}")
    #         return False
        
    #     logging.info(f"Message sent to {recipient}.")
    #     return True
        # Sending email to both email accounts
    with mail.connect() as conn:
        for num in range(2):
            recipient = acct_email if num == 0 else old_recovery_email
            msg = EmailMessage(
                subject = f"{APP_NAME} Recovery email address changed ",
                sender = EMAIL_CREDENTIALS["email_address"],
                html = render_template(
                    RECOVERY_EMAIL_CHANGE, # email template name 
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
    
    # Sending email to both old and new accounts
    # email_1_sent = send_mail(acct_email)
    # email_2_sent = send_mail(old_recovery_email)
    
    # if email_1_sent and email_2_sent:
    #     return True

    # return False


####################################
#  CHANGE AND SET RECOVERY EMAIL   #
####################################
def send_email_change_and_set_recovery(name:str, acct_email:str, old_recovery_email: str, new_recovery_email: str) -> bool:
    try:
        send_email_recovery_change(name, acct_email, old_recovery_email)
    except Exception as e:
        logging.error(f"Failed to send confirmation emails of change in account recovery email.")
        return False
    try:
        send_email_recovery_set(name, acct_email, new_recovery_email)
    except Exception as e:
        logging.error(f"Failed to send confirmation emails of new set account recovery email.")
        return False
    return True