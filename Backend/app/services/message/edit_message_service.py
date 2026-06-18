# Extensions and configurations
from app.extensions.extensions import db

# Python/Flask libraries
import logging
from app.constants.message_and_thread import ThreadStatus, ThreadPriority
from app.models.message import Message

def svc_mark_message_read_by_admin(message: Message, marked_read_by_admin: bool, admin_id: int, commit: bool = True) -> bool:
    """
    Will mark message.marked_read_by_admin to True or False. Optionally, commits changes to the DB.
    Requires the id of the admin who read/responded to the message.
    Obs: if message has already been marked as read (or unread), request will be ignored and return True.
    Admin id will not be cleared if marking unread.

    :param message (Message): member of Message model.
    :param marked_read_by_admin (bool): True if the message is to be marked as read, False otherwise.
    :param admin_id (int): Id of the admin user who read/responded to message.
    :param commit (bool): True if want the changes to be committed to DB (select False if the caller is another service).
    """
    if not message or not getattr(message, "id", None):
        logging.error(f"svc_mark_message_read_by_admin received no or invalid message.")
        return False
    if not isinstance(marked_read_by_admin, bool) or not isinstance(admin_id, int):
        logging.error("svc_mark_message_read_by_admin received invalid parameters.")
        return False
    if message.marked_read_by_admin == marked_read_by_admin:
        return True
    try:
        message.marked_read_by_admin = marked_read_by_admin
        message.marked_read_by_admin_id = admin_id
        if commit:
            db.session.commit()
        return True
    except Exception as e:
        if commit:
            db.session.rollback()
        logging.error(f"svc_mark_message_read_by_admin was unable to mark message as read. Error: {e}")
        return False