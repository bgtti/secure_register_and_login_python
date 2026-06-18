# Python/Flask libraries
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import logging
from enum import Enum

# Extensions and configurations
from app.extensions.extensions import db
from sqlalchemy import or_

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

def svc_search_user_message_threads(
        user_id: int, 
        page_nr: int, 
        items_per_page: int = 25,
        marked_spam: bool = False, 
        marked_deleted: bool = False, 
        internal_use: bool = False,
        ) -> dict | None:
    """
    Retrieves paginated message threads involving a given user.

    A user is considered involved if:
    - they started the thread, or
    - is the sender or recipient of at least one message in the thread.

    :param user_id (int): id of user part of a message thread.
    :param page_nr (int): the page number, must be greater than 0.
    :param items_per_page (int): number of thread items, must be greater than 0 and unser 100. Defaults to 25.
    :param marked_spam (bool): False will filter out thread.is_spam, True will only yield threads marked as spam. Will be ignored if internal_use is False.
    :param marked_deleted (bool): False will filter out thread.is_deleted, True will only yield threads marked as deleted. Ps: will be ignored if marked_spam is set to True or internal_use is set to False 
    :param internal_use (bool): if the table is public/user-facing (False) or for internal/admin use (True). Defaults to False.

    Returns:
        dict | None: None if no threads are found, otherwise a dictionary containing: current_page (int), total_pages (int), and threads (list of threads dict)
    
    Example of return data:
    ```python
    {
        "current_page": 1,
        "total_pages": 5,
        "threads": [
            {
            "id": 10,
            "reference": "REF-A7X92Q98",
            "created_at": "Thu, 25 Jan 2024 00:00:00 GMT",
            "last_message_at": "Thu, 25 Jan 2024 00:00:00 GMT",
            "subject": "Problems logging into account.",
            "status": "new",
            "priority": "normal", # only if internal_use == True
            "flagged": "blue", # only if internal_use == True
            "is_spam": False, # only if internal_use == True
            "is_deleted": False, # only if internal_use == True
            "deleted_at": None, # only if internal_use == True
            "purge_date": "Fri, 25 Jan 2025 00:00:00 GMT", # only if internal_use == True
            "originator_id": 105, # only if internal_use == True
            "originator_email": "john@example.com", # only if internal_use == True
            "originator_name": "John", # only if internal_use == True
            "assigned_to_admin_id": None, # only if internal_use == True
            }, 
            #...
        ]
    }
    ```
    """
    # Check params
    if not isinstance(user_id, int) or user_id < 1:
        logging.error("svc_search_user_message_threads received invalid user_id.")
        return None
    
    if page_nr < 1 or items_per_page < 1 or items_per_page > 100:
        logging.error("svc_search_user_message_threads received invalid page_nr or items_per_page.")
        return None
        
    # Get threads
    try:
        # filter user
        query = (
            MessageThread.query
            .outerjoin(Message)
            .filter(
                or_(
                    MessageThread.originator_user_id == user_id,
                    Message.user_id == user_id,
                    Message.recipient_id == user_id
                )
            )
        )
        # filter spam/deleted accordingly
        if internal_use:
            # users should not see that the system or admins marked their message as spam or deleted them
            if marked_spam:
                query = query.filter(MessageThread.is_spam.is_(True))
            elif marked_deleted:
                query = query.filter(MessageThread.is_deleted.is_(True))
            else:
                query = query.filter(
                MessageThread.is_spam.is_(False),
                MessageThread.is_deleted.is_(False),
            )
        
        # order and paginate
        threads = (
            query
            .distinct()
            .order_by(MessageThread.last_message_at.desc())
            .paginate(
                page=page_nr,
                per_page=items_per_page,
                error_out=False
            )
        )

    except Exception as e:
        logging.error(f"Failed to access DB. Error: {e}")
        return None
    
    if not threads.items:
        return None
    
    def serialize(thread):
        public = {
            "id": thread.id,
            "reference": thread.reference,
            "created_at": thread.created_at,
            "last_message_at": thread.last_message_at,
            "subject": thread.subject,
            "status": (thread.status.value).lower().replace("_", " "), # is enum
        }
        # Not public-facing:
        if internal_use:
            private = {
                "priority": (thread.priority.value).lower().replace("_", " "), # is enum
                "flagged": (thread.flagged.value).lower().replace("_", " "), # is enum
                "is_spam": thread.is_spam,
                "is_deleted": thread.is_deleted,
                "deleted_at": thread.deleted_at,
                "purge_date": thread.purge_date,
                "category": thread.category,
                "originator_name": thread.originator_name, 
                "originator_email": thread.originator_email,
                "originator_user_id": thread.originator_user_id,
                "assigned_to_admin_id": thread.assigned_to_admin_id
            }
            return public | private
        return public
    
    return {
        "threads": [serialize(thread) for thread in threads.items],
        "total_pages": threads.pages,
        "current_page": threads.page,
    }

def svc_check_if_user_part_of_thread(
    thread_id: int,
    user_id: int
) -> bool:
    """
    Checks whether a user is part of a message thread.

    A user is considered part of the thread if they appear
    as sender or recipient in at least one message belonging
    to the thread.

    :param thread_id (int): ID of the thread.
    :param user_id (int): ID of the user.

    Returns:
        bool:
            True if user is part of thread, False otherwise.
    """

    if (
        not isinstance(thread_id, int)
        or thread_id < 1
        or not isinstance(user_id, int)
        or user_id < 1
    ):
        logging.error(
            "svc_check_if_user_part_of_thread received invalid parameters."
        )
        return False

    try:
        user_is_in_thread = (
            Message.query
            .filter(
                Message.thread_id == thread_id,
                db.or_(
                    Message.sender_id == user_id,
                    Message.recipient_id == user_id,
                )
            )
            .first()
        )

        return bool(user_is_in_thread)

    except Exception as e:
        logging.error(
            f"svc_check_if_user_part_of_thread failed to access DB. Error: {e}"
        )

        return False
