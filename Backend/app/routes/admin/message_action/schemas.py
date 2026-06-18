from app.constants.validation_input_length import INPUT_LENGTH
from app.constants.flags import Flag
from app.constants.message_and_thread import ThreadStatus, ThreadPriority

message_flag_values = [flag.value for flag in Flag]
thread_status_values = [status.value for status in ThreadStatus]
thread_priority_values = [priority.value for priority in ThreadPriority]

mark_spam_schema = {
    "type": "object",
    "title": "Mark or unmark message thread as spam.", 
    "properties": {
        "message_id": {
            "description": "Id of message to be marked as",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "is_spam": {
            "description": "Mark as spam: set to true.",
            "type": "boolean",
            },
    },
    "additionalProperties": False,
    "required": ["message_id","is_spam"]
}

flag_change_schema = {
    "type": "object",
    "title": "Flag message thread.", 
    "properties": {
        "message_thread_id": {
            "description": "Id of message thread to be flagged",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "flag": {
            "description": "Flag colour to flag message thread.",
            "type": "string",
            "enum": message_flag_values,
            },
    },
    "additionalProperties": False,
    "required": ["message_id","message_flag"]
}

answer_message_schema = {
    "type": "object",
    "properties": {
        "message_id": {
            "description": "Id of original message.",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "subject": {
            "description": "Subject of email answer.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['contact_message_subject']['minValue'], 
            "maxLength": INPUT_LENGTH['contact_message_subject']['maxValue'],
        },
        "answer": {
            "description": "Body of the answer to message.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['contact_message']['minValue'], 
            "maxLength": INPUT_LENGTH['contact_message']['maxValue'],
        },
        "send_per_email": {
            "description": "If True will also send the answer per email to the original sender.",
            "type": "boolean",
            }
    },
    "additionalProperties": False,
    "required": ["message_id", "subject", "answer", "send_per_email"]
}

edit_thread_schema = {
    "type": "object",
    "properties": {
        "thread_id": {
            "description": "Id of thread that should be edited.",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "thread_status": {
            "description": "Thread status: enum selection.",
            "type": "string",
            "enum": thread_status_values,
            },
        "thread_priority": {
            "description": "Thread priority: enum selection.",
            "type": "string",
            "enum": thread_priority_values,
            },
        "thread_category": {
            "description": "Thread category: free text string. Empty string possible.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['thread_category']['minValue'], 
            "maxLength": INPUT_LENGTH['thread_category']['maxValue'],
            },
        "thread_assined_to": {
            "description": "Id of admin that should be responsible for the thread. None if no responsible person assigned.",
            "type": ["integer", "null"],
            },
    },
    "additionalProperties": False,
    "required": ["thread_id", "thread_status", "thread_priority", "thread_category", "thread_assined_to"]
}

delete_thread_schema = {
    "type": "object",
    "title": "Delete thread", 
    "properties": {
        "thread_id": {
            "description": "Id of thread to delete.",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "delete": {
            "description": "To delete thread: set to true.",
            "type": "boolean",
            },
    },
    "additionalProperties": False,
    "required": ["thread_id", "delete"]
}

add_note_schema = {
    "type": "object",
    "title": "Add note to thread.", 
    "properties": {
        "thread_id": {
            "description": "Id of thread to which the note should be added.",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "note": {
            "description": "Body of the note.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['thread_note']['minValue'], 
            "maxLength": INPUT_LENGTH['thread_note']['maxValue'],
        },
        "is_pinned": {
            "description": "To pin a note to the top: set to true.",
            "type": "boolean",
            },
    },
    "additionalProperties": False,
    "required": ["thread_id", "note", "is_pinned"]
}

edit_note_schema = {
    "type": "object",
    "title": "Edit a thread note.", 
    "properties": {
        "note_id": {
            "description": "Id of note to edit.",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "note": {
            "description": "Body of the note.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['thread_note']['minValue'], 
            "maxLength": INPUT_LENGTH['thread_note']['maxValue'],
        },
        "is_pinned": {
            "description": "To pin a note to the top: set to true.",
            "type": "boolean",
            },
    },
    "additionalProperties": False,
    "required": ["note_id", "note", "is_pinned"]
}

delete_note_schema = {
    "type": "object",
    "title": "Delete a thread note.", 
    "properties": {
        "note_id": {
            "description": "Id of note to delete.",
            "type": "integer",
            "exclusiveMinimum": 0 
            }
    },
    "additionalProperties": False,
    "required": ["note_id"]
}