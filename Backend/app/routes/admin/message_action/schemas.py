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

admin_message_action_mark_answer = {
    "type": "object",
    "properties": {
        "message_id": {
            "description": "Id of message to be marked as",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "answered_by": {
            "description": "Email of the admin who answered message",
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN
            },
        "subject": {
            "description": "Optional subject of answer",
            "type": "string", 
            "minLength":  INPUT_LENGTH['contact_message_subject']['minValue'], 
            "maxLength": INPUT_LENGTH['contact_message_subject']['maxValue'],
        },
        "answer": {
            "description": "Answer message",
            "type": "string", 
            "minLength":  INPUT_LENGTH['contact_message']['minValue'], 
            "maxLength": INPUT_LENGTH['contact_message']['maxValue'],
        },
        "answer_date": {
            "description": "Optiona answer date formatted YYYY-MM-DD",
            "type": "string", 
            "format": "date",
            "minLength":  10, 
            "maxLength": 10,
            "pattern": DATE_PATTERN ,
        },
        "email_answer": {
            "description": "Email answer: set to true. If false, it will record answer but not send it.",
            "type": "boolean",
            },
    },
    "additionalProperties": False,
    "required": ["message_id","answered_by", "answer", "email_answer"]
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