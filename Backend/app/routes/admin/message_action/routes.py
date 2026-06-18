"""
In this file: routes that provide message-related actions (to be accessed by admin users only) 
  - mark message as spam
  - change message flag
  - answer message
  - edit thread attributes
  - delete message thread
  - add/edit/remove notes from threads

Note: only basic logging implemented here. More robust logging logic may be necessary.
"""

# Python/Flask libraries
from flask import Blueprint, request, jsonify
from datetime import datetime, timezone, timedelta

# Extensions and configurations
from flask_login import login_required, current_user
from app.extensions.extensions import db
import logging

# Constants and common helpers
from app.constants.message_and_thread import MessageDirection, MessageChannel
from app.common.custom_decorators.admin_protected_route import admin_only
from app.common.custom_decorators.json_schema_validator import validate_schema

# Email service
from app.emails.admin.message_answering_email import send_answer_by_email

# Services
from app.services.message.add_message_service import svc_add_message
from app.services.message.delete_thread_service import svc_delete_thread
from app.services.message.edit_message_service import svc_mark_message_read_by_admin
from app.services.message.edit_thread_service import (
    svc_set_thread_is_spam, 
    svc_change_thread_flag, 
    svc_set_thread_status, 
    svc_set_thread_priority,
    svc_set_thread_category,
    svc_assign_thread_to_admin
    )
from app.services.message.get_message_service import svc_get_message_by_id
from app.services.message.get_thread_service import svc_get_thread_by_id
from app.services.message.note_service import (
    svc_add_thread_note,
    svc_get_thread_note_by_id,
    svc_edit_thread_note,
    svc_delete_thread_note
)

# Json Schema
from app.routes.admin.message_action.schemas import( 
    mark_spam_schema, 
    flag_change_schema, 
    answer_message_schema, 
    edit_thread_schema,
    delete_thread_schema, 
    add_note_schema,
    edit_note_schema,
    delete_note_schema
    )

# Blueprint
from . import message_action


# ----- MESSAGES MARK AS -----
@message_action.route("/mark_spam", methods=["POST"])
@login_required
@admin_only
@validate_schema(mark_spam_schema)
def mark_spam():
    """
    Route to mark (or unmark) a message as spam.
    Note that if message is marked as spam, it will change the thread status.
    
    Possible responses: 200, 404, 500.
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get info from JSON payload
    message_thread_id = json_data["message_thread_id"] 
    is_spam = json_data["is_spam"] 

    # Responses
    res_200 = {"response": "Message spam mark changed."}
    res_404 = {"response": "Message or thread not found."}
    res_500 = {"response": "Error prevented answer to be recorded"}

    # Get Thread
    thread = svc_get_thread_by_id(message_thread_id)
    if not thread:
        return jsonify(res_404), 404

    thread_ok = svc_set_thread_is_spam(thread, is_spam=is_spam, commit=True)

    if not thread_ok:
        return jsonify(res_500), 500
        
    return jsonify(res_200), 200

# ----- MESSAGES FLAG CHANGE -----
@message_action.route("/flag_change", methods=["POST"])
@login_required
@admin_only
@validate_schema(flag_change_schema)
def flag_change():
    """
    Route to change a message thread's flag.

    Possible responses: 200, 404, 500.
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get info from JSON payload
    message_thread_id = json_data["message_thread_id"] 
    flag = json_data["flag"] 

    # Responses
    res_200 = {"response": "Flag colour changed."}
    res_404 = {"response": "Message or thread not found."}
    res_500 = {"response": "Error prevented answer to be recorded"}

    # Get Thread
    thread = svc_get_thread_by_id(message_thread_id)
    if not thread:
        return jsonify(res_404), 404

    flag_change_ok = svc_change_thread_flag(thread, flag, True)

    if not flag_change_ok:
        return jsonify(res_500), 500

    return jsonify(res_200), 200

# ----- ANSWER MESSAGE ----- 
@message_action.route("/answer_message", methods=["POST"])
@login_required
@admin_only
@validate_schema(answer_message_schema)
def answer_message():
    """
    Route used by admins to answer a message from a user.
    Answer can optionally also be sent by email.
    Original message will be marked as read.
    
    Possible responses: 200, 201, 404, 500.
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get required info from JSON payload
    message_id = json_data["message_id"]
    subject = json_data["subject"]
    answer = json_data["answer"]
    send_per_email = json_data["send_per_email"]

    # Responses
    res_200 = {"response": "Message sent."} if send_per_email else {"response": "Message recorded."}
    res_201 = {"response": "Message recorded, but email could not be sent."}
    res_404 = {"response": "Message not found."}
    res_500 = {"response": "Error prevented answer from being recorded."}

    # Get original message
    orig_msg = svc_get_message_by_id(message_id)
    if not orig_msg:
        return jsonify(res_404), 404

    # Mark original message as read by admin
    if not orig_msg.marked_read_by_admin:
        svc_mark_message_read_by_admin(orig_msg, True, current_user.id, False) # add message should commit both
    
    # Add Message to Thread
    msg = svc_add_message(
        thread= orig_msg.thread, 
        sender_name = current_user.name, 
        sender_email = current_user.email,
        sender_id = current_user.id,
        subject = subject,
        message_body = answer,
        direction = MessageDirection.OUTBOUND,
        channel = MessageChannel.STAFF_TO_USER,
        user_agent = None,
        ip_address = None,
        geo_location = None,
        recipient_id = orig_msg.sender_id,
        recipient_email = orig_msg.sender_email,
        recipient_name = orig_msg.sender_name,
    )

    if not msg["success"]:
        logging.error(msg["log_txt"])
        return jsonify(res_500), 500

    # Done if admin does not want to send it by email
    if not send_per_email:
        return jsonify(res_200), 200

    email_data = {
        "recipient": orig_msg.sender_email,
        "message": answer,
        "subject": subject,
        "sender_name": f"{current_user.name} - Admin Team",
        "thread_ref": orig_msg.thread.reference,
        "original_message":orig_msg.body,
        "original_message_date":orig_msg.created_at,
    }
    email_sent = send_answer_by_email(email_data)

    if not email_sent:
        logging.error(f"Email could not be sent.")
        return jsonify(res_201), 201
    
    return jsonify(res_200), 200

# ----- ANSWER MESSAGE -----
@message_action.route("/edit_thread", methods=["POST"])
@login_required
@admin_only
@validate_schema(edit_thread_schema)
def edit_thread():
    """
    Route to change a thread's:
    - status
    - priority
    - category
    - admin id assignment
    
    Possible responses: 200, 404, 500.
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    thread_id = json_data["thread_id"]
    thread_status = json_data["thread_status"]
    thread_priority = json_data["thread_priority"]
    thread_category = json_data["thread_category"]
    thread_assined_to = json_data["thread_assined_to"]

    # Responses
    res_200 = {"response": "Thread edited successfully."}
    res_404 = {"response": "Thread not found."}
    res_500 = {"response": "Error prevented thread from being changed."}

    # Get Thread
    thread = svc_get_thread_by_id(thread_id)
    if not thread:
        return jsonify(res_404), 404
    
    # Check changes
    status_changed = priority_changed = category_changed = assignment_changed = False

    if thread.status.value != thread_status:
        status_changed = svc_set_thread_status(thread, thread_status, False)
    if thread.priority.value != thread_priority:
        priority_changed = svc_set_thread_priority(thread, thread_priority, False)
    if thread.category != thread_category:
        category_changed = svc_set_thread_category(thread, thread_category, False)
    if thread.assigned_to_admin_id != thread_assined_to:
        assignment_changed = svc_assign_thread_to_admin(thread, thread_assined_to, False)

    # Commit to db if changed
        
    if status_changed or priority_changed or category_changed or assignment_changed:
        try:
            db.session.commit()
        except Exception as e:
            logging.error(f"Changes to thread could not be saved. Error: {e}")
            return jsonify(res_500), 500
    
    return jsonify(res_200), 200

# ----- ACTION: DELETE Thread and Messages ----- 
@message_action.route("/delete_thread", methods=["POST"])
@login_required
@admin_only
@validate_schema(delete_thread_schema) 
def delete_thread():
    """
    Route can be used to:
    - soft-delete thread
    - remove thread's "is_deleted" mark
    - purge thread (actually delete from DB)

    Possible responses: 200, 404, 500.
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get id from JSON payload
    thread_id = json_data["thread_id"]
    delete = json_data["delete"]

    # Responses
    res_200 = {"response": "Thread deleted successfully."} if delete else {"response": "Thread moved to inbox."}
    res_404 = {"response": "Thread not found."}
    res_500 = {"response": "Error prevented thread from being (un)deleted."}

    # Get Thread
    thread = svc_get_thread_by_id(thread_id)
    if not thread:
        return jsonify(res_404), 404
    
    # Mark deletion
    del_ok = svc_delete_thread(thread, delete, True)

    if not del_ok:
        return jsonify(res_500), 500
    
    return jsonify(res_200), 200

# ----- ACTION: ADD Note ----- 
@message_action.route("/add_note", methods=["POST"])
@login_required
@admin_only
@validate_schema(add_note_schema) 
def add_note():
    """
    Route adds an internal admin/staff note to a message thread.

    Possible responses: 200, 404, 500.
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get id from JSON payload
    thread_id = json_data["thread_id"]
    note = json_data["note"]
    is_pinned = json_data["is_pinned"]

    # Responses
    res_200 = {"response": "Note added successfully."} 
    res_404 = {"response": "Thread not found."}
    res_500 = {"response": "Error prevented note from being added."}

    # Get Thread
    thread = svc_get_thread_by_id(thread_id)
    if not thread:
        return jsonify(res_404), 404
    
    # Add note
    note_ok = svc_add_thread_note(
        thread=thread, 
        staff_id=current_user.id, 
        body=note,
        is_pinned=is_pinned,
        commit=True)

    if not note_ok:
        return jsonify(res_500), 500
    
    return jsonify(res_200), 200

# ----- ACTION: EDIT Note ----- 
@message_action.route("/edit_note", methods=["POST"])
@login_required
@admin_only
@validate_schema(edit_note_schema) 
def edit_note():
    """
    Route edits an internal thread note.

    Allows changing:
    - note body
    - pinned status

    Possible responses: 200, 404, 500.
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get id from JSON payload
    note_id = json_data["note_id"]
    note = json_data["note"]
    is_pinned = json_data["is_pinned"]

    # Responses
    res_200 = {"response": "Note edited successfully."}
    res_404 = {"response": "Note not found."}
    res_500 = {"response": "Error prevented note from being edited."}

    # Get note
    note = svc_get_thread_note_by_id(note_id)

    if not note:
        return jsonify(res_404), 404

    # Edit note
    note_ok = svc_edit_thread_note(
        note=note,
        body=note_body,
        is_pinned=is_pinned,
        commit=True,
    )

    if not note_ok:
        return jsonify(res_500), 500

    return jsonify(res_200), 200

# ----- ACTION: DELETE Note ----- 
@message_action.route("/delete_note", methods=["POST"])
@login_required
@admin_only
@validate_schema(delete_note_schema) 
def delete_note():
    """
    Route deletes an internal thread note.

    Allows changing:
    - note body
    - pinned status

    Possible responses: 200, 404, 500.
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get id from JSON payload
    note_id = json_data["note_id"]

    # Responses
    res_200 = {"response": "Note deleted successfully."}
    res_404 = {"response": "Note not found."}
    res_500 = {"response": "Error prevented note from being deleted."}

    # Get note
    note = svc_get_thread_note_by_id(note_id)

    if not note:
        return jsonify(res_404), 404

    # Edit note
    note_ok = svc_delete_thread_note(
        note=note,
        commit=True,
    )

    if not note_ok:
        return jsonify(res_500), 500

    return jsonify(res_200), 200
