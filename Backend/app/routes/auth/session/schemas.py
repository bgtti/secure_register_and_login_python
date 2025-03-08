from app.utils.constants.account_constants import INPUT_LENGTH,  EMAIL_PATTERN, PASSWORD_PATTERN
from app.utils.constants.enum_class import TokenPurpose, AuthMethods, PasswordChangeReason


login_method_values = [method.value for method in AuthMethods]
"""method can be: 'otp', 'password'"""


####################################
#         SESSION SCHEMAS          #
####################################

get_otp_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN},
        "honeypot": {
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
            },
    },
    "additionalProperties": False,
    "required": ["email", "honeypot"]
}

login_schema = {
    "type": "object",
    "title": "Will log a user in.",
    "properties": {
        "email": {
            "description": "Email of user logging in.",
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN},
        "password": {
            "description": "Can accept passwords and otp.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], # should be the same as OTP length
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        "method": {
            "description": "Whether user wants to log in with otp or password",
            "type": "string", 
            "enum": login_method_values
        },
        "is_first_factor": {
            "description": "Indicates whether this is the first (true) or second (false) authentication factor",
            "type": "boolean", 
        },
        "honeypot": {
            "description": "Designed for catching bots.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. Optional.",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },
    "additionalProperties": False,
    "required": ["email", "password","method", "is_first_factor", "honeypot"]
}