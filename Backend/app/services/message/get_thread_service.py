# Python/Flask libraries
import logging
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError

# Extensions and configurations
from app.extensions.extensions import db

# Models
from app.models.message_thread import MessageThread

def svc_get_thread_by_id(thread_id:int)-> Optional[MessageThread]:
    """
    Retrieve a thread from the database by its id, or return `None` if no thread exists.

    :param thread_id (int): The id of the thread.
    
    Returns:
        MessageThread | None:
            MessageThread object as and if retrieved from the db or `None` if thread not found.
    """
    if not isinstance(thread_id, int) or thread_id < 1:
        logging.error("Invalid parameters passed to `svc_get_thread_by_id`.")
        return None
    try:
        return db.session.get(MessageThread, thread_id)

    except SQLAlchemyError:
        logging.exception("`svc_get_thread_by_id` failed to access DB.")
        return None