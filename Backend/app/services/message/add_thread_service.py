"""
Messages and Threads:
A message must belong to a Thread.
Thread Notes must belong to a Thread.

Flow: 
1) create Thread
2) create Message and link to that Thread.
3) [optional] create Note and link to that Thread.
"""
# Python/Flask libraries
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import logging
from enum import Enum

# Extensions and configurations
from app.extensions.extensions import db

# Constants 
from app.constants.flags import Flag
from app.constants.message_and_thread import MessageDirection, MessageChannel, ThreadStatus

# Utilities
from app.common.generators.reference_code import generate_thread_reference
from app.common.enum_helpers import map_string_to_enum
from app.common.detect_spam.spam_filter import looks_like_spam

# Models
from app.models.message_thread import MessageThread
from app.models.message import Message
from app.models.message_thread_note import MessageThreadNote

# Other Services
from app.services.message.add_message_service import svc_add_message

def svc_start_message_thread(
    originator_user_id: int, 
    originator_email: str, 
    originator_name: str, 
    subject: str, 
    message_body: str,
    direction:str | Enum = MessageDirection.INBOUND,
    channel:str | Enum = MessageChannel.CONTACT_FORM,
    user_agent: str | None = None,
    ip_address: str | None = None,
    geo_location: str | None = None,
    recipient_id: int = 1,
    recipient_email: str | None = None,
    recipient_name: str | None = None,
    note_about_thread: str | None = None
) -> dict:
    """
        Creates starts a MessageThread and the first Message linked to it.

        The function:
        - generates a unique public thread reference
        - creates a MessageThread
        - creates the first Message using svc_add_message()
        - applies the message flag to the thread if needed
        - commits both objects in one transaction

        Returns:
            dict:
                {
                    "success": bool,
                    "flag": str | None,
                    "log_code": int,
                    "log_txt": str | None,
                    "message": str | None
                }
        """  
    # Prepare return
    res = {
        "success": False,
        "flag": None,
        "log_code": 500, # private
        "log_txt": "", # private
        "http_code": 500, # public
        "message": "" # public
    }

    # get a unique reference
    def get_unique_ref(attempts=0):
        """
        Attempts to generate a unique thread reference up to 4 times.
        """
        ref = generate_thread_reference()
        ref_exists = MessageThread.query.filter_by(reference=ref).first()
        if ref_exists:
            logging.debug("Generating unique thread ref: re-trying after collision encountered.")
            if attempts >= 3:
                return None
            return get_unique_ref(attempts=attempts + 1)
        return ref

    ref = get_unique_ref()

    if not ref:
        total_threads = MessageThread.query.count()
        logging.critical(
                f"svc_start_message_thread was unable to generate a unique message thread reference after 4 attempts. Check thread reference generation logic. Number of threads counted in the DB = {total_threads}."
            )
        res["log_txt"] = "Error prevented Thread creation: unable to generate unique message thread reference after 4 attempts."
        res["message"] = "An error occurred: message failed. Please try again later."
        return res

    try:
        # initiate thread
        thread = MessageThread(
            originator_user_id=originator_user_id,
            originator_email=originator_email,
            originator_name=originator_name,
            subject=subject,
            reference=ref
        )

        db.session.add(thread)
        db.session.flush()  # gives thread.id before commit

        # add note, if available
        if note_about_thread and note_about_thread.strip():
            note = MessageThreadNote(
            staff_id=0,
            body=note_about_thread,
            thread_id=thread.id,
            is_pinned=True,
            )
            db.session.add(note)

        # add message --> thread will be committed by this function
        msg_res = svc_add_message(
            thread=thread,
            sender_name=originator_name,
            sender_email=originator_email,
            user_id=originator_user_id,
            subject=subject,
            message_body=message_body,
            direction=direction,
            channel=channel,
            user_agent=user_agent,
            ip_address=ip_address,
            geo_location=geo_location,
            recipient_id=recipient_id,
            recipient_email=recipient_email,
            recipient_name=recipient_name
        )

        if not msg_res["success"]:
            db.session.rollback()
            return msg_res
        
        log_txt = "Thread successfully created. "

        res["success"] = msg_res["success"]
        res["flag"] = msg_res["flag"]
        res["log_code"] = msg_res["log_code"]
        res["log_txt"] = (log_txt + (msg_res["log_txt"] or "")).strip()
        res["message"] = msg_res["message"]
        res["http_code"] = 200

    except Exception as e:
        db.session.rollback()
        logging.exception("svc_start_message_thread failed.")

        res["log_txt"] = f"System error prevented thread + message to be created. Error: {str(e)}"
        res["message"] = "An error occurred: message failed. Please try again later."

    return res