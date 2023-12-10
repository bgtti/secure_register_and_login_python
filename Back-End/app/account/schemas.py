from app.account.constants import INPUT_LENGTH 

EMAIL_PATTERN = r'^[^@\s]+@[^@\s]+$'
PASSWORD_PATTERN = r'^[\s\S]{%d,%d}$' % (INPUT_LENGTH['password']['minValue'], INPUT_LENGTH['password']['maxValue'])

# Explanation of the EMAIL_PATTERN:
# ^: Asserts the start of the string.
# [^@\s]+: Matches one or more characters that are not '@' or whitespace.
# @: Matches the '@' character.
# [^@\s]+: Matches one or more characters that are not '@' or whitespace.
# $: Asserts the end of the string.

# Explanation of the PASSWORD_PATTERN:
# ^: Asserts the start of the string.
# [\s\S]: Matches any character, including whitespace (ASCII and Unicode).
# {%d,%d}: Specifies the minimum and maximum length based on your constants.
# $: Asserts the end of the string.

sign_up_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string", 
            "minLength": INPUT_LENGTH['name']['minValue'], 
            "maxLength": INPUT_LENGTH['name']['maxValue']
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
    },
    "additionalProperties": False,
    "required": ["name", "email", "password"]
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
    },
    "additionalProperties": False,
    "required": ["email", "password"]
}