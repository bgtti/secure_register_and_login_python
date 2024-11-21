import logging
from flask_mail import Message as EmailMessage
from utils.print_to_terminal import print_to_terminal
from config.values import EMAIL_CREDENTIALS
from app.extensions.extensions import mail

def contact_form_email_forwarding(sender_name, sender_email, subject, message, is_user=False, email_in_db=""):
    """
    contact_form_email_forwarding(sender_name: str, sender_email: str, subject: str, message: str, is_user: bool, email_in_db: str) -> bool
    -----------------------------------------------------------------------------
    Function forwards information received via contact form to the site admin's email address.
    Email forwarding will only work if email credentials were set up in the .env file correctly.
    -----------------------------------------------------------------------------
    Returns True if email forwarding succeeded and False otherwise.
    """

    if EMAIL_CREDENTIALS["email_set"] == False:
        print_to_terminal("Email credentials not set up. Contact form could not be forwarded to email.", "RED")
        return False
    
    if is_user:
        if sender_email == email_in_db:
            is_registered = f"Sender is a registered user."
        else:
            is_registered = f"Sender is a user registered with email {email_in_db}."
    else:
        is_registered = "Sender is not a registered user."

    email_body = f"""
    <b>[SafeDev App] New Contact Form Message received.</b><br>
    ********************************************************************<br>
    <b>Sender's name:</b> {sender_name}<br>
    <b>Sender's email:</b> {sender_email}<br>
    <em>{is_registered}</em><br>
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

