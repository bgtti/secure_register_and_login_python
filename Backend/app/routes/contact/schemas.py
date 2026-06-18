from app.constants.validation_input_length import INPUT_LENGTH
from app.constants.validation_patterns import NAME_PATTERN, EMAIL_PATTERN

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
        "honeypot": { #TODO rename
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
        },
    },
    "additionalProperties": False,
    "required": ["name","email", "message", "honeypot"]
}