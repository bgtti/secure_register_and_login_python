# Python/Flask libraries
import logging

# Extensions and configurations
from app.extensions.extensions import db

# Models
from app.models.message_thread import MessageThread
from app.models.message_thread_note import MessageThreadNote

def svc_add_thread_note(
    thread: MessageThread,
    staff_id: int,
    body: str,
    is_pinned: bool = False,
    commit: bool = True,
) -> bool:
    """
    Adds an internal note to a message thread.

    Notes are staff/system-facing only and are not visible to users.

    :param thread (MessageThread): member of MessageThread model.
    :param staff_id (int): ID of the staff member authoring the note.
                            Use 0 for automatic/system notes.
    :param body (str): note body text.
    :param is_pinned (bool): whether the note should be pinned.
    :param commit (bool): whether changes should be committed to DB.
                          Set False if caller handles transaction.

    Returns:
        bool:
            True if successful, False otherwise.
    """

    if not thread or not getattr(thread, "id", None):
        logging.error("Invalid or no thread passed to svc_add_thread_note.")
        return False

    if not isinstance(staff_id, int) or staff_id < 0:
        logging.error("Invalid staff_id passed to svc_add_thread_note.")
        return False

    if not isinstance(body, str) or not body.strip():
        logging.error("Invalid body passed to svc_add_thread_note.")
        return False

    if not isinstance(is_pinned, bool):
        logging.error("Invalid is_pinned parameter passed to svc_add_thread_note.")
        return False

    try:
        note = MessageThreadNote(
            staff_id=staff_id,
            body=body.strip(),
            thread_id=thread.id,
            is_pinned=is_pinned,
        )

        db.session.add(note)

        if commit:
            db.session.commit()

        return True

    except Exception as e:
        if commit:
            db.session.rollback()

        logging.error(f"svc_add_thread_note was unable to add note. Error: {e}")

        return False

def svc_get_thread_note_by_id(note_id: int) -> MessageThreadNote | None:
    """
    Retrieves a thread note by ID.
    """

    if not isinstance(note_id, int) or note_id < 1:
        logging.error("Invalid note_id passed to svc_get_thread_note_by_id.")
        return None

    try:
        return db.session.get(MessageThreadNote, note_id)

    except Exception as e:
        logging.error(f"svc_get_thread_note_by_id failed to access DB. Error: {e}")
        return None

def svc_edit_thread_note(
    note: MessageThreadNote,
    body: str | None = None,
    is_pinned: bool | None = None,
    commit: bool = True,
) -> bool:
    """
    Edits an internal thread note.

    Allows changing:
    - note body
    - pinned status

    Pass None for a field if it should not be changed.

    :param note (MessageThreadNote): member of MessageThreadNote model.
    :param body (str | None): new note body. If None, body is unchanged.
    :param is_pinned (bool | None): new pinned status. If None, pinned status is unchanged.
    :param commit (bool): True if changes should be committed to DB.

    Returns:
        bool:
            True if successful, False otherwise.
    """

    if not note or not getattr(note, "id", None):
        logging.error("Invalid or no note passed to svc_edit_thread_note.")
        return False

    if body is not None:
        if not isinstance(body, str) or not body.strip():
            logging.error("Invalid body passed to svc_edit_thread_note.")
            return False

        body = body.strip()

    if is_pinned is not None and not isinstance(is_pinned, bool):
        logging.error("Invalid is_pinned passed to svc_edit_thread_note.")
        return False

    try:
        changed = False

        if body is not None and note.body != body:
            note.body = body
            changed = True

        if is_pinned is not None and note.is_pinned != is_pinned:
            note.is_pinned = is_pinned
            changed = True

        if not changed:
            return True

        if commit:
            db.session.commit()

        return True

    except Exception as e:
        if commit:
            db.session.rollback()

        logging.error(f"svc_edit_thread_note was unable to edit note. Error: {e}")

        return False

def svc_delete_thread_note(
    note: MessageThreadNote,
    commit: bool = True,
) -> bool:
    """
    Deletes a thread note from the database.

    :param note (MessageThreadNote): member of MessageThreadNote model.
    :param commit (bool): True if changes should be committed to DB.

    Returns:
        bool:
            True if successful, False otherwise.
    """

    if not note or not getattr(note, "id", None):
        logging.error("Invalid or no note passed to svc_delete_thread_note.")
        return False

    try:
        db.session.delete(note)

        if commit:
            db.session.commit()

        return True

    except Exception as e:
        if commit:
            db.session.rollback()

        logging.error(
            f"svc_delete_thread_note was unable to delete note. Error: {e}"
        )

        return False