from app.utils.constants.account_constants import INPUT_LENGTH, NAME_PATTERN, EMAIL_PATTERN

contact_form_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string", 
            "minLength": INPUT_LENGTH['name']['minValue'], 
            "maxLength": INPUT_LENGTH['name']['maxValue'],
            "pattern": NAME_PATTERN
            },
        "email": {
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN
            },
        "subject": {
            "type": "string", 
            "minLength":  INPUT_LENGTH['contact_message_subject']['minValue'], 
            "maxLength": INPUT_LENGTH['contact_message_subject']['maxValue'],
        },
        "message": {
            "type": "string", 
            "minLength":  INPUT_LENGTH['contact_message']['minValue'], 
            "maxLength": INPUT_LENGTH['contact_message']['maxValue'],
        },
        "is_user": {
            "description": "Set to true if user is logged in.",
            "type": "boolean",
        },
        "honeypot": {
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
        },
    },
    "additionalProperties": False,
    "required": ["name","email", "message", "is_user", "honeypot"]
}