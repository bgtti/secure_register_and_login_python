from app.constants.message_and_thread import ThreadStatus, ThreadPriority

thread_status_values = [status.value for status in ThreadStatus]
thread_priority_values = [priority.value for priority in ThreadPriority]

thread_notes_table_schema = {
    "type": "object",
    "title": "Table of notes belonging to a message thread.", 
    "properties": {
        "thread_id": {
            "description": "Page number as int > 0",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "page_nr": {
            "description": "Page number as int > 0",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "items_per_page": {
            "description": "Number of items per page. Defaults to 25 if not specified.",
            "type": "integer",
            "exclusiveMinimum": 0,
            "multipleOf" : 5,
            "maximum": 25, 
            }
    },
    "additionalProperties": False,
    "required": ["thread_id", "page_nr", "items_per_page"]
}

thread_messages_table_schema = {
    "type": "object",
    "title": "Table of messages belonging to a message thread.", 
    "properties": {
        "thread_id": {
            "description": "ID of the thread.",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "page_nr": {
            "description": "Page number as int > 0",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "items_per_page": {
            "description": "Number of items per page. Defaults to 25 if not specified.",
            "type": "integer",
            "exclusiveMinimum": 0,
            "multipleOf" : 5,
            "maximum": 25, 
            }
    },
    "additionalProperties": False,
    "required": ["thread_id", "page_nr", "items_per_page"]
}

threads_table_schema = {
    "type": "object",
    "title": "Table of message threads.", 
    "properties": {
        "page_nr": {
            "description": "Page number as int > 0",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "items_per_page": {
            "description": "Number of items per page. Defaults to 25 if not specified.",
            "type": "integer",
            "exclusiveMinimum": 0,
            "multipleOf" : 5,
            "maximum": 100, 
            },
        "thread_status": {
            "description": "Thread status: enum selection or None.",
            "type": ["string", "null"],
            "enum": thread_status_values + [None],
            },
        "thread_priority": {
            "description": "Thread priority: enum selection or None.",
            "type": ["string", "null"],
            "enum": thread_priority_values + [None],
            },
        "order_by_priority": {
            "description": "Whether threads should be ordered by priority or last message date.",
            "type": "boolean"
            },
        "show_deleted": {
            "description": "Whether to show only deleted threads or non-deleted threads.",
            "type": "boolean"
            },
        "show_spam": {
            "description": "Whether to show only threads marked as spam or non-spam threads.",
            "type": "boolean"
            },
        "admin_id": {
            "description": "Only show threads assigned to a particular admin id.",
            "type": ["integer", "null"],
            },
        "not_assigned_only": {
            "description": "Whether to show only threads not assigned to anyone.",
            "type": "boolean"
            },
    },
    "additionalProperties": False,
    "required": ["page_nr", "items_per_page","thread_status", "thread_priority", "order_by_priority", "show_deleted", "show_spam", "admin_id", "not_assigned_only"]
}