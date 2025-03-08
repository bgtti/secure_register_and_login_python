from app.utils.constants.account_constants import INPUT_LENGTH, PASSWORD_PATTERN, OTP_PATTERN

####################################
#         SAFETY SCHEMAS           #
####################################

verify_account_schema = {
    "type": "object",
    "title": "Verifies user's account email address.", 
    "properties": {
        "otp": {
            "description": "Can accept otp.",
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
    "required": ["otp"]
}

set_mfa_schema = {
    "type": "object",
    "title": "Enables or disables multi-factor authentication for the user's account.", 
    "properties": {
        "enable_mfa": {
            "description": "Boolean to signify whether mfa should be enabled (true) or disabled (false). Otp is required only for the case of disabling mfa.",
            "type": "boolean", 
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
    "required": ["enable_mfa", "password"]
}