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