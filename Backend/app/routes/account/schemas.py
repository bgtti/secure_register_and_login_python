from app.utils.constants.account_constants import INPUT_LENGTH, NAME_PATTERN, EMAIL_PATTERN, PASSWORD_PATTERN

sign_up_schema = {
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
        "password": {
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], 
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        "honeypot": {
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
            },
    },
    "additionalProperties": False,
    "required": ["name", "email", "password", "honeypot"]
}

log_in_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN},
        "password": {
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], 
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN},
        "honeypot": {
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
            },
    },
    "additionalProperties": False,
    "required": ["email", "password", "honeypot"]
}