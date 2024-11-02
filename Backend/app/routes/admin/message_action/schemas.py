from app.utils.constants.account_constants import INPUT_LENGTH, EMAIL_PATTERN, DATE_PATTERN 
from app.utils.constants.enum_class import UserFlag
message_flag_values = [flag.value for flag in UserFlag]

admin_message_action_mark_as = {
    "type": "object",
    "title": "Mark message as", 
    "properties": {
        "message_id": {
            "description": "Id of message to be marked as",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "answer_needed": {
            "description": "Mark as answer is needed: set to true.",
            "type": "boolean" 
            },
        "is_spam": {
            "description": "Mark as spam: set to true.",
            "type": "boolean",
            },
        "sender_is_spammer": {
            "description": "Mark sender as spammer: set to true.",
            "type": "boolean",
            },
    },
    "additionalProperties": False,
    "required": ["message_id","answer_needed", "is_spam", "sender_is_spammer"]
}

admin_message_action_flag_change = {
    "type": "object",
    "title": "Mark message as", 
    "properties": {
        "message_id": {
            "description": "Id of message to be marked as",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "message_flag": {
            "description": "Flag colour to flag user.",
            "type": "string",
            "enum": message_flag_values,
            },
    },
    "additionalProperties": False,
    "required": ["message_id","message_flag"]
}

admin_message_action_answer_message = {
    "type": "object",
    "properties": {
        "message_id": {
            "description": "Id of message to be marked as",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "email_answer": {
            "description": "Email answer: set to true. If false, it will record answer but not send it.",
            "type": "boolean",
            },
        "answer": {
            "description": "Text of answer to message",
            "type": "string", 
            "minLength":  INPUT_LENGTH['contact_message']['minValue'], 
            "maxLength": INPUT_LENGTH['contact_message']['maxValue'],
        },
        "subject": {
            "description": "Optional: subject of email answer (if answer is emailed)",
            "type": "string", 
            "minLength":  INPUT_LENGTH['contact_message_subject']['minValue'], 
            "maxLength": INPUT_LENGTH['contact_message_subject']['maxValue'],
        },
        "answered_by": {
            "description": "Optional: Email of the admin who answered message (if answer is recorded)",
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN
            },
        "answer_date": {
            "description": "Optional: answer date formatted YYYY-MM-DD (if answer is recorded)",
            "type": "string", 
            "format": "date",
            "minLength":  10, 
            "maxLength": 10,
            "pattern": DATE_PATTERN ,
        }
    },
    "additionalProperties": False,
    "required": ["message_id","email_answer", "answer"]
}

admin_message_delete_schema = {
    "type": "object",
    "title": "Delete message", 
    "properties": {
        "message_id": {
            "description": "Id of message to delete.",
            "type": "integer",
            "exclusiveMinimum": 0 
            }
    },
    "additionalProperties": False,
    "required": ["message_id"]
}