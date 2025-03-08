from app.utils.constants.account_constants import INPUT_LENGTH, NAME_PATTERN, EMAIL_PATTERN, PASSWORD_PATTERN, OTP_PATTERN

####################################
#         RECOVERY SCHEMAS         #
####################################

set_recovery_email_schema = {
    "type": "object",
    "title": "Will set user's recovery email.",
    "properties": {
        "recovery_email": {
            "description": "User's recovery email.",
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN
            },
        "password": {
            "description": "Can only accept password.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'],
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        "otp": {
            "description": "Can only accept otp.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['otp']['minValue'], 
            "maxLength": INPUT_LENGTH['otp']['maxValue'], 
            "pattern": OTP_PATTERN
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },

    "additionalProperties": False,
    "required": ["recovery_email", "password","otp"]
}

get_recovery_email_schema = {
    "type": "object",
    "title": "Will send the recovery email of the user.",
    "properties": {
        "password": {
            "description": "Can only accept password.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'],
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },

    "additionalProperties": False,
    "required": ["password"]
}

delete_recovery_email_schema = {
    "type": "object",
    "title": "Will delete the user's recovery email.",
    "properties": {
        "password": {
            "description": "Can only accept password.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'],
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },

    "additionalProperties": False,
    "required": ["password"]
}
