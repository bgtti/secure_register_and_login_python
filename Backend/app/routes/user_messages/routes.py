"""
In this file: routes that provides tables for messages, and threads for users.

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
from flask_login import (
    current_user,
    login_required,
)
from app.extensions.extensions import limiter
import logging

# Common
from app.common.custom_decorators.json_schema_validator import validate_schema

# Services
from app.services.message.table_service import svc_get_messages_table, svc_get_user_threads_table
from app.services.message.search_service import svc_check_if_user_part_of_thread

# JSON Schema
from app.routes.user_messages import (
    user_thread_table_schema,
    user_messages_table_schema
)

# Blueprint
from . import user_messages

# ----- GET THREADS TABLE -----
@user_messages.route("/get_user_threads", methods=["POST"])
@login_required
@validate_schema(user_thread_table_schema)
def get_user_threads():
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


    threads_data = svc_get_user_threads_table(
        user_id=current_user.id,
        page_nr=page_nr,
        items_per_page=items_per_page
    )

    if not threads_data:
        return jsonify({"response": "No threads found."}), 404

    response_data = {
        "response": "success",
        "threads": threads_data["threads"],
        "current_page": threads_data["current_page"],
        "total_pages": threads_data["total_pages"],
    }

    return jsonify(response_data), 200

# ----- GET MESSAGE TABLE -----
@user_messages.route("/get_user_messages", methods=["POST"])
@login_required
@validate_schema(user_messages_table_schema)
def get_user_messages():
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

    # Make sure the user has righful access to this thread, else anyone could access a any thread from anyone.
    if not svc_check_if_user_part_of_thread(
            thread_id=thread_id,
            user_id=current_user.id
        ):
        # Use 404, not 403, so you do not reveal whether the thread exists.
        logging.info(f"User id={current_user.id} tried to request a message thread to which they had no access.")
        return jsonify({"response": "Thread not found."}), 404

    # Get messages table
    messages_data = svc_get_messages_table(
        thread_id=thread_id,
        page_nr=page_nr,
        items_per_page=items_per_page,
        internal_use=False, # Important!
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
    }

    return jsonify(response_data), 200