"""
In this file: admin routes that provides tables for messages, threads, and notes.

Messages are organized the following way:

A Thread is comprised of messages, like a conversation flow.
A Message must belong to a Thread, and a Thread must have at least one Message to exist.
This way, message conversations are kept together orderly.

Admins may also add Notes to a Thread. A Thread may or may not have Notes belonging to them.
In Notes, admins can keep track of the status of a problem or conversation.
"""
# Python/Flask libraries
from flask import Blueprint, request, jsonify
from datetime import datetime, timezone, timedelta

# Extensions and configurations
from flask_login import login_required
from app.extensions.extensions import limiter
import logging

# Common
from app.common.custom_decorators.admin_protected_route import admin_only
from app.common.custom_decorators.json_schema_validator import validate_schema

# Services
from app.services.message.table_service import svc_get_notes_table, svc_get_messages_table, svc_get_admin_threads_table

# JSON Schema
from app.routes.admin.messages.schemas import (
    thread_notes_table_schema,
    thread_messages_table_schema,
    threads_table_schema
)

# Blueprint
from . import messages

# ----- NOTES TABLE -----
@messages.route("/thread_notes_table", methods=["POST"])
@login_required
@admin_only
@validate_schema(thread_notes_table_schema)
def thread_notes_table():
    """
    Route returns paginated notes belonging to a message thread.

    Notes are ordered:
    - pinned notes first
    - newest first within each group

    Possible responses: 200, 404.
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get info from JSON payload
    thread_id = json_data["thread_id"]
    page_nr = json_data["page_nr"] # > 0
    items_per_page = json_data["items_per_page"] # >= 5 and <=25, multiple of 5
    
    # Get notes table
    notes_data = svc_get_notes_table(
        thread_id=thread_id,
        page_nr=page_nr,
        items_per_page=items_per_page,
    )

    if not notes_data:
        return jsonify({
            "response": "No notes found."
        }), 404

    response_data = {
        "response": "success",
        "notes": notes_data["notes"],
        "current_page": notes_data["current_page"],
        "total_pages": notes_data["total_pages"],
        "query": {
            "thread_id": thread_id,
            "page_nr": page_nr,
            "items_per_page": items_per_page,
            "ordered_by": [
                "is_pinned descending",
                "created_at descending",
            ]
        }
    }

    return jsonify(response_data), 200

# ----- MESSAGES TABLE -----
@messages.route.route("/thread_messages_table", methods=["POST"])
@login_required
@admin_only
@validate_schema(thread_messages_table_schema)
def thread_messages_table():
    """
    Route returns paginated messages belonging to a thread.

    Accepts page number and desired number of items per page (maximum of 25).

    Messages are ordered oldest -> newest.

    Possible responses: 200, 404.
    """

    # Get JSON payload
    json_data = request.get_json()

    # Get payload data
    thread_id = json_data["thread_id"]
    page_nr = json_data.get("page_nr", 1)
    items_per_page = json_data.get("items_per_page", 25)

    # Get messages table
    messages_data = svc_get_messages_table(
        thread_id=thread_id,
        page_nr=page_nr,
        items_per_page=items_per_page,
        internal_use=True,
    )

    if not messages_data:
        return jsonify({
            "response": "No messages found."
        }), 404

    response_data = {
        "response": "success",
        "messages": messages_data["messages"],
        "current_page": messages_data["current_page"],
        "total_pages": messages_data["total_pages"],
        "query": {
            "thread_id": thread_id,
            "page_nr": page_nr,
            "items_per_page": items_per_page,
            "ordered_by": "created_at ascending",
        }
    }

    return jsonify(response_data), 200

# ----- MESSAGE THREADS TABLE -----
@messages.route.route("/threads_table", methods=["POST"])
@login_required
@admin_only
@validate_schema(threads_table_schema)
def threads_table():
    """
    Route returns paginated table of message threads.

    Accepts page number and desired number of items per page (maximum of 100).

    Messages are ordered oldest -> newest.

    Possible responses: 200, 404.
    """

    # Get JSON payload
    json_data = request.get_json()

    # Get payload data
    page_nr = json_data.get("page_nr", 1)
    items_per_page = json_data.get("items_per_page", 25)

    status = json_data.get("thread_status")
    priority = json_data.get("thread_priority")
    order_by_priority = json_data.get("order_by_priority", True)

    show_deleted = json_data.get("show_deleted", False)
    show_spam = json_data.get("show_spam", False)

    admin_id = json_data.get("admin_id")
    not_assigned_only = json_data.get("not_assigned_only", False)

    threads_data = svc_get_admin_threads_table(
        page_nr=page_nr,
        items_per_page=items_per_page,
        status=status,
        priority=priority,
        order_by_priority=order_by_priority,
        show_deleted=show_deleted,
        show_spam=show_spam,
        admin_id=admin_id,
        not_assigned_only=not_assigned_only,
    )

    if not threads_data:
        return jsonify({"response": "No threads found."}), 404

    response_data = {
        "response": "success",
        "threads": threads_data["threads"],
        "current_page": threads_data["current_page"],
        "total_pages": threads_data["total_pages"],
        "query": {
            "page_nr": page_nr,
            "items_per_page": items_per_page,
            "status": status,
            "priority": priority,
            "order_by_priority": order_by_priority,
            "show_deleted": show_deleted,
            "show_spam": show_spam,
            "admin_id": admin_id,
            "not_assigned_only": not_assigned_only,
            "ordered_by": (
                "priority, last_message_at"
                if order_by_priority and not priority
                else "last_message_at"
            ),
            "order_sort": "descending",
        }
    }

    return jsonify(response_data), 200