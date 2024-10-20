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