"""
Services providing messaging-related tables: tables of threads, messages, and notes.
"""
# Python/Flask libraries
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import logging

# Extensions and configurations
from app.extensions.extensions import db
from sqlalchemy import case, func, or_
from sqlalchemy.orm import aliased

# Constants 
from app.constants.message_and_thread import ThreadStatus, ThreadPriority, THREAD_PRIORITY_SCORE

# Utilities
from app.common.enum_helpers import map_string_to_enum

# Models
from app.models.message_thread import MessageThread
from app.models.message import Message
from app.models.message_thread_note import MessageThreadNote

# ----- NOTES TABLE -----
def svc_get_notes_table(
    thread_id: int,
    page_nr: int,
    items_per_page: int = 25,
) -> dict | None:
    """
    Returns paginated notes belonging to a message thread.
    Notes are meant for admin/staff only.

    Notes are ordered:
    - pinned notes first
    - newest first within each group

    :param thread_id (int): ID of the thread.
    :param page_nr (int): requested page number.
    :param items_per_page (int): number of notes per page. Max 25.

    Returns:
        dict | None

    ```python
    {
        "notes": [
            {
                "note_id": 10,
                "created_at": "...",
                "updated_at": "...",
                "staff_id": 2,
                "body": "Need to follow up with billing.",
                "is_pinned": True,
            }
        ],
        "current_page": 1,
        "total_pages": 3,
    }
    ```
    """

    # Validate params
    if not isinstance(thread_id, int) or thread_id < 1:
        logging.error("Invalid thread_id passed to svc_get_thread_notes_table.")
        return None

    if not isinstance(page_nr, int) or page_nr < 1:
        logging.error("Invalid page_nr passed to svc_get_thread_notes_table.")
        return None

    if (
        not isinstance(items_per_page, int)
        or items_per_page < 1
        or items_per_page > 25
    ):
        logging.error("Invalid items_per_page passed to svc_get_thread_notes_table.")
        return None

    try:
        notes = (
            MessageThreadNote.query
            .filter_by(thread_id=thread_id)
            .order_by(
                MessageThreadNote.is_pinned.desc(),
                MessageThreadNote.created_at.desc(),
            )
            .paginate(
                page=page_nr,
                per_page=items_per_page,
                error_out=False,
            )
        )

        if not notes.items:
            return None

        def serialize(note):
            return {
                "note_id": note.id,
                "created_at": note.created_at,
                "updated_at": note.updated_at,
                "staff_id": note.staff_id,
                "body": note.body,
                "is_pinned": note.is_pinned,
            }

        return {
            "notes": [serialize(note) for note in notes.items],
            "current_page": notes.page,
            "total_pages": notes.pages,
        }

    except Exception as e:
        logging.error(
            f"svc_get_thread_notes_table failed to access DB. Error: {e}"
        )

        return None

# ----- MESSAGES TABLE -----
def svc_get_messages_table(
    thread_id: int,
    page_nr: int,
    items_per_page: int = 25,
    internal_use: bool = False,
) -> dict | None:
    """
    Returns paginated messages belonging to a message thread.

    Messages are ordered oldest -> newest.

    :param thread_id (int): ID of the thread.
    :param page_nr (int): requested page number.
    :param items_per_page (int): number of messages per page. Max 25.
    :param internal_use (bool): whether internal/admin-only fields should be included.

    Returns:
        dict | None

    Example:
    {
        "messages": [
            {
                "message_id": 10,
                "created_at": "...",
                "sender_name": "John",
                "sender_email": "john@example.com",
                "subject": "Problem with invoice",
                "body": "Hello...",
                "direction": "inbound",
                "channel": "contact form",
            }
        ],
        "current_page": 1,
        "total_pages": 3,
    }
    """

    # Validate params
    if not isinstance(thread_id, int) or thread_id < 1:
        logging.error("Invalid thread_id passed to svc_get_thread_messages_table.")
        return None

    if not isinstance(page_nr, int) or page_nr < 1:
        logging.error("Invalid page_nr passed to svc_get_thread_messages_table.")
        return None

    if (
        not isinstance(items_per_page, int)
        or items_per_page < 1
        or items_per_page > 25
    ):
        logging.error("Invalid items_per_page passed to svc_get_thread_messages_table.")
        return None

    try:
        messages = (
            Message.query
            .filter_by(thread_id=thread_id)
            .order_by(Message.created_at.asc())
            .paginate(
                page=page_nr,
                per_page=items_per_page,
                error_out=False,
            )
        )

        if not messages.items:
            return None

        def serialize(message):
            public = {
                "message_id": message.id,
                "created_at": message.created_at,
                "sender_name": message.sender_name,
                "sender_email": message.sender_email,
                "subject": message.subject,
                "body": message.body,
                "direction": message.direction.value.lower().replace("_", " "),
                "channel": message.channel.value.lower().replace("_", " "),
            }

            if internal_use:
                private = {
                    "sender_id": message.sender_id,
                    "recipient_id": message.recipient_id,
                    "recipient_email": message.recipient_email,
                    "recipient_name": message.recipient_name,
                    "marked_read_by_admin": message.marked_read_by_admin,
                    "read_by_admin_id": message.read_by_admin_id,
                    "flagged": message.flagged.value.lower().replace("_", " "),
                    "user_agent": message.user_agent,
                    "ip_address": message.ip_address,
                    "geo_location": message.geo_location,
                }

                return public | private

            return public

        return {
            "messages": [
                serialize(message)
                for message in messages.items
            ],
            "current_page": messages.page,
            "total_pages": messages.pages,
        }

    except Exception as e:
        logging.error(
            f"svc_get_thread_messages_table failed to access DB. Error: {e}"
        )

        return None

# ----- THREADS TABLE: ADMIN -----

def svc_get_admin_threads_table(
    page_nr: int,
    items_per_page: int = 25,
    status: str | ThreadStatus | None = None,
    priority: str | ThreadPriority | None = None,
    order_by_priority: bool = True,
    show_deleted: bool = False,
    show_spam: bool = False,
    admin_id: int | None = None,
    not_assigned_only: bool = False,
) -> dict | None:
    """
    Returns a paginated admin table of message threads (not meant for user/public use).

    Threads are always ordered by last_message_at descending.

    :param page_nr (int): requested page number.
    :param items_per_page (int): number of messages per page. Max 100.
    :param status (str | ThreadStatus | None): Filter. If None, CLOSED threads are excluded. If provided, only that status is shown.
    :param priority (str | ThreadPriority | None): Filter. If None, no priority filter is applied. If provided, only that priority is shown.
    :param order_by_priority (bool): if set to True will order table by highest level of priority first if no priority filter is in use. If False, table will be ordered by last_message_at.
    :param show_deleted (bool): False excludes deleted threads. True shows only deleted threads.
    :param show_spam (bool): False excludes spam threads. True shows only spam threads.
    :param admin_id (int | None): If provided, shows only threads assigned to that admin.
    :param not_assigned_only (bool): If True, shows only threads with no assigned admin. This overrides admin_id.

    Returns:
        dict | None:
            {
                "threads": [...],
                "current_page": int,
                "total_pages": int
            }
    """
    # Check params
    if not isinstance(page_nr, int) or page_nr < 1:
        logging.error("svc_get_message_threads_table received invalid page_nr.")
        return None

    if (
        not isinstance(items_per_page, int)
        or items_per_page < 1
        or items_per_page > 100
    ):
        logging.error("svc_get_message_threads_table received invalid items_per_page.")
        return None

    if (
        not isinstance(order_by_priority, bool)
        or not isinstance(show_deleted, bool)
        or not isinstance(show_spam, bool)
    ):
        logging.error("svc_get_message_threads_table received invalid filter parameters.")
        return None

    if not isinstance(not_assigned_only, bool):
        logging.error("svc_get_message_threads_table received invalid not_assigned_only.")
        return None

    if admin_id is not None and (
        not isinstance(admin_id, int) or admin_id < 1
    ):
        logging.error("svc_get_message_threads_table received invalid admin_id.")
        return None

    status_enum = None
    priority_enum = None

    if status is not None:
        status_enum = map_string_to_enum(status, ThreadStatus)

        if not status_enum: 
            logging.error("svc_get_message_threads_table received invalid status.")
            return None

    if priority is not None:
        priority_enum = map_string_to_enum(priority, ThreadPriority)

        if not priority_enum:
            logging.error("svc_get_message_threads_table received invalid priority.")
            return None

    try:
        query = db.session.query(MessageThread)

        # Status filter
        if status_enum:
            query = query.filter(MessageThread.status == status_enum)
        else:
            query = query.filter(MessageThread.status != ThreadStatus.CLOSED)

        # Priority filter
        if priority_enum:  
            query = query.filter(MessageThread.priority == priority_enum)

        # Deleted filter
        query = query.filter(
            MessageThread.is_deleted.is_(True)
            if show_deleted
            else MessageThread.is_deleted.is_(False)
        )

        # Spam filter
        query = query.filter(
            MessageThread.is_spam.is_(True)
            if show_spam
            else MessageThread.is_spam.is_(False)
        )

        # Assignment filter
        if not_assigned_only:
            query = query.filter(
                db.or_(
                    MessageThread.assigned_to_admin_id.is_(None),
                    MessageThread.assigned_to_admin_id == 0,
                )
            )
        elif admin_id is not None:
            query = query.filter(
                MessageThread.assigned_to_admin_id == admin_id
            )

        # Table ordering: either prioritize or by lattest message
        if not priority_enum and order_by_priority:# order table with highest priority first
                priority_order = case(
                    THREAD_PRIORITY_SCORE,
                    value=MessageThread.priority
                )
                query = query.order_by(
                    priority_order.desc(),
                    MessageThread.last_message_at.desc()
                )
        else:
            query = query.order_by(MessageThread.last_message_at.desc())
        
        # Pagination
        threads = (
            query.paginate(
                page=page_nr,
                per_page=items_per_page,
                error_out=False
            )
        )

        if not threads.items:
            return None
        
        # Count messages and notes attached to threads
        thread_ids = [thread.id for thread in threads.items]

        # count how many messages are in thread
        message_counts = dict(
            db.session.query(
                Message.thread_id,
                func.count(Message.id)
            )
            .filter(Message.thread_id.in_(thread_ids))
            .group_by(Message.thread_id)
            .all()
        )
        # count how many notes are in thread
        note_counts = dict(
            db.session.query(
                MessageThreadNote.thread_id,
                func.count(MessageThreadNote.id)
            )
            .filter(MessageThreadNote.thread_id.in_(thread_ids))
            .group_by(MessageThreadNote.thread_id)
            .all()
        )

        def enum_to_label(value):
            return value.value.lower().replace("_", " ") if value else None

        def serialize(thread):

            return {
                "id": thread.id,
                "last_message_at": thread.last_message_at,
                "updated_at": thread.updated_at,
                "created_at": thread.created_at,
                "subject": thread.subject,
                "reference": thread.reference,
                "status": enum_to_label(thread.status),
                "priority": enum_to_label(thread.priority),
                "flagged": enum_to_label(thread.flagged),
                "is_spam": thread.is_spam,
                "is_deleted": thread.is_deleted,
                "deleted_at": thread.deleted_at,
                "purge_date": thread.purge_date,
                "category": thread.category,
                "assigned_to_admin_id": thread.assigned_to_admin_id,
                "originator_name": thread.originator_name,
                "originator_email": thread.originator_email,
                "message_count": message_counts.get(thread.id, 0),
                "note_count": note_counts.get(thread.id, 0),
            }

        return {
            "threads": [serialize(row) for row in threads.items],
            "current_page": threads.page,
            "total_pages": threads.pages,
        }

    except Exception as e:
        logging.error(
            f"svc_get_message_threads_table failed to access DB. Error: {e}"
        )
        return None


# ----- THREADS TABLE: USERS -----

def svc_get_user_threads_table(
    user_id: int,
    page_nr: int,
    items_per_page: int = 25,
) -> dict | None:
    """
    Returns a paginated user-facing table of message threads.

    A thread is included if the user appears as sender or recipient
    in at least one message in that thread.

    Threads are ordered by last_message_at descending.

    :param user_id (int): threads relevant to the particular user.
    :param page_nr (int): requested page number.
    :param items_per_page (int): number of messages per page. Max 100.

    Returns:
        dict | None:
            {
                "threads": [...],
                "current_page": int,
                "total_pages": int
            }
    """

    if not isinstance(user_id, int) or user_id < 1:
        logging.error("svc_get_user_threads_table received invalid user_id.")
        return None

    if (
        not isinstance(page_nr, int)
        or page_nr < 1
        or not isinstance(items_per_page, int)
        or items_per_page < 1
        or items_per_page > 100
    ):
        logging.error("svc_get_user_threads_table received invalid pagination params.")
        return None

    try:
        query = (
            MessageThread.query
            .join(Message)
            .filter(
                or_(
                    Message.sender_id == user_id,
                    Message.recipient_id == user_id,
                )
            )
            .distinct()
            .order_by(MessageThread.last_message_at.desc())
        )

        threads = query.paginate(
            page=page_nr,
            per_page=items_per_page,
            error_out=False
        )

        if not threads.items:
            return None

        thread_ids = [thread.id for thread in threads.items]

        message_counts = dict(
            db.session.query(
                Message.thread_id,
                func.count(Message.id)
            )
            .filter(Message.thread_id.in_(thread_ids))
            .group_by(Message.thread_id)
            .all()
        )

        def enum_to_label(value):
            return value.value.lower().replace("_", " ") if value else None

        def serialize(thread):
            return {
                "id": thread.id,
                "last_message_at": thread.last_message_at,
                "created_at": thread.created_at,
                "status": enum_to_label(thread.status),
                "subject": thread.subject,
                "reference": thread.reference,
                "category": thread.category,
                "originator_name": thread.originator_name,
                "message_count": message_counts.get(thread.id, 0),
            }

        return {
            "threads": [serialize(thread) for thread in threads.items],
            "current_page": threads.page,
            "total_pages": threads.pages,
        }

    except Exception as e:
        logging.error(
            f"svc_get_user_threads_table failed to access DB. Error: {e}"
        )
        return None