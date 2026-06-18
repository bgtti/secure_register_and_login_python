# Python/Flask libraries
import logging
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError

# Extensions and configurations
from app.extensions.extensions import db

# Models
from app.models.message import Message

def svc_get_message_by_id(message_id:int)-> Optional[Message]:
    """
    Retrieve a message from the database by its id, or return `None` if no message exists.

    :param message_id (int): The id of the message.
    
    Returns:
        Message | None:
            Message object as and if retrieved from the db or `None` if message not found.
    """
    if not isinstance(message_id, int) or message_id < 1:
        logging.error("Invalid parameters passed to `svc_get_message_by_id`.")
        return None
    try:
        return db.session.get(Message, message_id)

    except SQLAlchemyError:
        logging.exception("`svc_get_message_by_id` failed to access DB.")
        return None