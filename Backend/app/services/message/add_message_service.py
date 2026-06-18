# Python/Flask libraries
import logging
from enum import Enum
from datetime import datetime, timezone

# Extensions and configurations
from app.extensions.extensions import db

# Constants
from app.constants.message_and_thread import MessageDirection, MessageChannel
from app.constants.flags import Flag, FLAG_PRIORITY

# Models
from app.models.message_thread import MessageThread
from app.models.message import Message

# Utilities
from app.common.detect_html.detect_html import check_for_html
from app.common.profanity_check.profanity_check import has_profanity
from app.common.enum_helpers.map_string_to_enum import map_string_to_enum
from app.common.detect_spam.spam_filter import looks_like_spam

#Services
from app.services.message.edit_thread_service import svc_set_thread_is_spam

def svc_add_message(
        thread: MessageThread, 
        sender_name: str, 
        sender_email: str,
        sender_id: int,
        subject: str,
        message_body: str,
        direction: str | Enum = MessageDirection.INBOUND,
        channel: str | Enum = MessageChannel.CONTACT_FORM,
        user_agent: str | None = None,
        ip_address: str | None = None,
        geo_location: str | None = None,
        recipient_id: int = 1,
        recipient_email: str | None = None,
        recipient_name: str | None = None,
        ) -> dict:
    """
    Creates and stores a Message linked to a MessageThread.

    The function:
    - validates enum values
    - checks content for HTML
    - checks content for profanity
    - flags the message if appropriate
    - creates and stores the message in the database (commits)
    - updates the Thread accordingly
    
    :param thread (MessageThread): member of MessageThread model.
    :param sender_name (str): Name of the message sender.
    :param sender_email (str): Email address of the sender.
    :param sender_id (int): User ID associated with the sender. Use 0 for anonymous users.
    :param subject (str): Message subject/title.
    :param message_body (str): Main body/content of the message.
    :param direction (str | Enum): Message direction. (Eg.: MessageDirection.INBOUND or "inbound")
    :param channel (str | Enum): Message source channel. (Eg.: MessageChannel.CONTACT_FORM or "contact_form")
    :param user_agent (str | None): Optional sender user agent.
    :param ip_address (str | None): Optional sender IP address.
    :param geo_location (str | None): Optional sender geolocation.
    :param recipient_id (int): Optional id of intended recipient. (0 if recipient is the system)
    :param recipient_email (str | None): Optional email of intended recipient.
    :param recipient_name (str | None): Optional name of intended recipient..

    Returns:
        dict: 
            - success (bool): indicates whether action was successful or not.
            - flag (str | None): flag color str indicates message has been flagged. None = it hasn't.
            - log_code (int): useful for logging.
            - log_txt (str | None): useful for logging (not meant for public view).
            - http_code (int): response code 500 or 200
            - message (str): message that can be sent in the response.
    """
    # Preparing response
    res = {
        "success": False,
        "flag": None,
        "log_code": 500, # private
        "log_txt": "", # private
        "http_code": 500, # public
        "message": "" # public
    }
    # Check thread
    if not thread or not getattr(thread, "id", None):
        logging.error(f"svc_add_message received no or invalid thread.")
        res["log_txt"] = "Error prevented Message creation: invalid thread."
        res["message"] = "An error occurred: message failed. Please try again later."
        return res

    # Check enums
    direction_enum = map_string_to_enum(direction, MessageDirection)
    channel_enum = map_string_to_enum(channel, MessageChannel)
    if not direction_enum or not channel_enum :
        logging.error(f"svc_add_message could not map param to enum.")
        res["log_txt"] = "Error prevented Message creation: could not map param to enum."
        res["message"] = "An error occurred: message failed. Please try again later."
        return res

    # Check for html
    if direction_enum == MessageDirection.INBOUND:
        html_in_name = check_for_html(sender_name, "svc_add_message - name field", sender_email)
        html_in_email = check_for_html(sender_email, "svc_add_message - email field", sender_email)
        html_in_subject = check_for_html(subject, "svc_add_message - subject field", sender_email)
        html_in_message = check_for_html(message_body, "svc_add_message - message body field", sender_email)

        if html_in_email or html_in_name or html_in_subject or html_in_message:
            res["flag"] = "YELLOW"
            res["log_txt"] = "Message flagged for possible html."
        else:
            # Check for profanity
            profanity_in_name = has_profanity(sender_name) 
            profanity_in_email = has_profanity(sender_email)
            profanity_in_subject = has_profanity(subject)
            profanity_in_message = has_profanity(message_body)
            if profanity_in_name or profanity_in_email or profanity_in_subject or profanity_in_message:
                res["flag"] = "PURPLE"
                res["log_txt"] = "Message flagged for possible profanity."

    # Create message
    try:
        new_message = Message(
            thread_id=thread.id,
            direction=direction_enum,
            channel=channel_enum,
            subject=subject,
            body=message_body,
            sender_name=sender_name,
            sender_email=sender_email,
            sender_id=sender_id,
            user_agent=user_agent,
            ip_address=ip_address,
            geo_location=geo_location,
            recipient_id=recipient_id,
            recipient_email=recipient_email,
            recipient_name=recipient_name,
        ) 
        db.session.add(new_message)

        # Flag thread if appropriate
        if res["flag"]:
            # Only flag if new flag is of higher priority 
            new_flag = map_string_to_enum(res["flag"], Flag)
            if (new_flag and FLAG_PRIORITY[new_flag] > FLAG_PRIORITY[thread.flagged]):
                thread.flagged = new_flag
        
        # Spam check and set thread as spam if appropriate
        is_spam = False

        if direction_enum == MessageDirection.INBOUND and looks_like_spam(message_body,subject,sender_name):
            is_spam = True
            svc_set_thread_is_spam(thread, True, False)
            res["log_txt"] = (f"{res['log_txt']} " if res["log_txt"] else "") + "System marked thread as spam."
        
        # Update thread last message
        thread.last_message_at = datetime.now(timezone.utc)
        
        # Commit changes to the db
        db.session.commit()

        # Prepare response
        res["success"] = True
        res["log_code"] = 207 if (res["flag"] or is_spam) else 200
        res["log_txt"] = ("Message successfully added to DB." + (f" {res['log_txt']}" if res["log_txt"] else ""))
        res["http_code"] = 200
        res["message"] = "Message saved successfully!"

        return res

    except Exception as e:
        db.session.rollback()
        logging.error(f"`svc_add_message` was unable to save message. Error: {e}")
        res["log_txt"] = f"Message could not be added to DB. Error: {str(e)}"
        res["message"] = "An error occurred: message failed. Please try again later."
        return res
