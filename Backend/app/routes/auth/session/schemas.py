# from app.common.constants.account_constants import INPUT_LENGTH,  EMAIL_PATTERN, PASSWORD_PATTERN
# from app.common.constants.enum_class import TokenPurpose, AuthMethods, PasswordChangeReason

from app.constants.validation_input_length import INPUT_LENGTH
from app.constants.validation_patterns import EMAIL_PATTERN
# from app.constants.auth_token_purpose import TokenPurpose
from app.constants.auth_methods import AuthMethods
# from app.constants.auth_password_change import PasswordChangeReason


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
        "honeypot": { #TODO: rename 'honeypot' to something else!
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], 
            },
        "form_name": {
            "description": "Name of the form (if any) that triggered the call ",
            "type": "string", 
            "minLength": INPUT_LENGTH['form_name']['minValue'], 
            "maxLength": INPUT_LENGTH['form_name']['maxValue'], 
            }
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
        "honeypot": { #TODO: rename 'honeypot' to something else!
            "description": "Designed for catching bots.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. Optional.",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], 
            }
    },
    "additionalProperties": False,
    "required": ["email", "password","method", "is_first_factor", "honeypot"]
}