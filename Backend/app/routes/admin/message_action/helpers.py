import logging
import re
from flask_mail import Message as EmailMessage
from sqlalchemy.exc import IntegrityError
from utils.print_to_terminal import print_to_terminal
from config.values import EMAIL_CREDENTIALS
from app.extensions import db, mail
from app.models.spammer import Spammer
from app.utils.constants.account_constants import EMAIL_PATTERN


def set_spammer(admin_id, spammer_email):
    """
    mark_message_as(admin_id: int, spammer_email: str) -> bool
    ----------------------------------------------------------
    Adds an email to the Spammer database.
    Takes the id of the admin doing the action and the spammer's email as arguments.
    
    Returns:
        True if the spammer is added successfully or email already in spammer's list.
        False if there is an error or integrity error.
    """
    try:
        # Check if spammer is already in the database
        existing_spammer = Spammer.query.filter_by(sender_email=spammer_email).first()
        if existing_spammer:
            logging.info(f"Email {spammer_email} already exists in Spammer list.")
            return True

        # Create a new spammer entry
        new_spammer = Spammer(admin_id=admin_id, sender_email=spammer_email)
        db.session.add(new_spammer)
        db.session.commit()

        logging.info(f"Email {spammer_email} added to Spammer list by admin {admin_id}.")
        return True

    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Integrity error when adding email {spammer_email} to spammer list: {e}")
        return False

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error when adding email {spammer_email} to spammer list: {e}")
        return False

def send_answer_by_email(email_data):
    """
    send_answer_by_email(email_data: dict) -> bool
    -----------------------------------------------------------------------------
    Function sends an email based on the data provided in the email_data dictionary.
    The email_data dictionary should contain the following keys:

    Required:
      - "message" (str): The content of the email message.
      - "recepient" (str): The email address of the recipient.

    Optional:
      - "subject" (str): The subject line of the email (default: "Re: contact form submission").
      - "sender_name" (str): The name of the sender (default: "Admin Team").
      - "original_message" (str): The content of the message being replied to (default: "").
      - "original_message_date" (str): The date of the original message (default: "N/A").
      - "original_message_sender" (str): The sender of the original message (default: "N/A").
    
    Email forwarding will only work if email credentials are set up correctly in the .env file.
    -----------------------------------------------------------------------------
    Returns:
      bool: True if email forwarding succeeded, and False otherwise.
"""
# Extract required and optional parameters with defaults
    message = email_data.get("message")
    recepient = email_data.get("recepient")
    subject = email_data.get("subject", "Re: contact form submission")
    sender_name = email_data.get("sender_name", "Admin Team")
    original_message = email_data.get("original_message", "")
    original_message_date = email_data.get("original_message_date", "N/A")

    if not EMAIL_CREDENTIALS["email_set"]:
        print_to_terminal("Email credentials not set up. Email could not be sent.", "RED")
        return False
    
    if not bool(re.match(EMAIL_PATTERN, recepient)):
        logging.warning(f"send_answer_by_email: email pattern failed for {recepient}.")
        return False
    
    if message=="":
        logging.warning("send_answer_by_email: cannot send email with no message.")
        return False
    
    message_history = ""

    if original_message != "":
        message_history = f"""
        <br>
        ************************<br>
        <em><b>*** Message history ***</b></em><br>
        <em>Sender: {recepient}</em><br>
        <em>Date: {original_message_date}</em><br>
        <em>Message:</em><br>
        <em>{original_message}</em><br>
        <br>
        <br>
        <em><b>If you did not author the message above, please inform the administrators of the site.</b></em><br>
        """

    email_body = f"""
    <b>You got a response from [SafeDev App]</b><br>
    ********************************************************************<br>
    <br>
    {message}<br>
    <br>
    Best regards,<br>
    {sender_name}<br>
    {message_history}
    """
    new_email = EmailMessage(
        f"[SafeDev]: {subject}",
        sender = EMAIL_CREDENTIALS["email_address"],
        recipients = [recepient]
    )
    new_email.html = email_body

    try:
        mail.send(new_email)
    except Exception as e:
        logging.error(f"Could not send email to {recepient}. Error: {e}")
        return False

    logging.info(f"Email sent to {recepient} successfully.")

    return True

