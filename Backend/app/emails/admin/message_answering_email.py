# Python and Flask
import logging
import re

# Extensions, Utils, and Config
from flask_mail import Message as EmailMessage
from utils.print_to_terminal import print_to_terminal
from config.values import EMAIL_CREDENTIALS
from app.extensions.extensions import mail

# Constants
from app.constants.validation_patterns import EMAIL_PATTERN

def send_answer_by_email(email_data: dict) -> bool:
    """
    Function sends an email based on the data provided in the email_data dictionary.
    The email_data dictionary should contain the following keys:

    Required:
      - "message" (str): The content of the email message.
      - "recipient" (str): The email address of the recipient.
      - "thread_ref" (str): The thread reference.

    Optional:
      - "subject" (str): The subject line of the email (default: "Re: contact form submission").
      - "sender_name" (str): The name of the sender (default: "Admin Team").
      - "original_message" (str): The content of the message being replied to (default: "").
      - "original_message_date" (str): The date of the original message (default: "N/A").
      - "original_message_sender" (str): The sender of the original message (default: "N/A").
    
    Email forwarding will only work if email credentials are set up correctly in the .env file.
    
    Returns:
      bool: True if email forwarding succeeded, and False otherwise.
"""
# Extract required and optional parameters with defaults
    message = email_data.get("message")
    recipient = email_data.get("recipient")
    thread_ref = email_data.get("thread_ref")
    subject = email_data.get("subject", "Re: contact form submission")
    sender_name = email_data.get("sender_name", "Admin Team")
    original_message = email_data.get("original_message", "")
    original_message_date = email_data.get("original_message_date", "N/A")

    if not EMAIL_CREDENTIALS["email_set"]:
        print_to_terminal("Email credentials not set up. Email could not be sent.", "RED")
        return False
    
    if not bool(re.match(EMAIL_PATTERN, recipient)):
        logging.warning(f"send_answer_by_email: email pattern failed for {recipient}.")
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
        <em>Reference: {thread_ref}</em><br>
        <em>Sender: {recipient}</em><br>
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
        recipients = [recipient]
    )
    new_email.html = email_body

    try:
        mail.send(new_email)
    except Exception as e:
        logging.error(f"Could not send email to {recipient}. Error: {e}")
        return False

    logging.info(f"Email sent to {recipient} successfully.")

    return True