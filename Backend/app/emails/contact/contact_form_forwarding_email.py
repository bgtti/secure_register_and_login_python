import logging
from flask_mail import Message as EmailMessage
from utils.print_to_terminal import print_to_terminal
from config.values import EMAIL_CREDENTIALS
from app.extensions.extensions import mail

def forward_contact_form_to_apps_email(sender_name:str, sender_email:str, subject:str, message:str, system_notes: str | None = None)-> bool:
    """
    Function forwards information received via contact form to the site admin's email address.
    Email forwarding will only work if email credentials were set up in the .env file correctly.
    Returns True if email forwarding succeeded and False otherwise.

        :param sender_name (str): name input as given in contact form
        :param sender_email (str): email input as given in contact form
        :param subject (str): subject input as given in contact form
        :param message (str): message input as given in contact form
        :param system_notes (str): [optional] system generated notes about the message (ex: if sender_email is different than user's email in the DB)
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Contact form could not be forwarded to email.", "RED")
        return False
    
    if not system_notes:
        notes = "-"
    else:
        notes = system_notes

    email_body = f"""
    <b>[SafeDev App] New Contact Form Message received.</b><br>
    ********************************************************************<br>
    <b>Sender's name:</b> {sender_name}<br>
    <b>Sender's email:</b> {sender_email}<br>
    <em>System notes:{notes}</em><br>
    ********************************************************************<br>
    <b>Subject:</b> {subject}<br>
    <br>
    <b>Message received:</b><br>
    <br>
    {message}

    """
    new_email = EmailMessage(
        f"[SafeDev] New message from {sender_name}: {subject}",
        sender = EMAIL_CREDENTIALS["email_address"],
        recipients = [EMAIL_CREDENTIALS["email_address"]]
    )
    new_email.html = email_body

    try:
        mail.send(new_email)
    except Exception as e:
        logging.error(f"Could not forward email. Error: {e}")
        return False

    logging.info(f"Contact form message forwarded to email.")

    return True