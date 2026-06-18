"""
**ABOUT THIS FILE**

auth/schemas.py contains the json schemas to validate request data in the auth routes.

------------------------
## More information

These schemas are passed in to `validate_schema` (see `app/utils/custom_decorators/json_schema_validator.py`) through the route's decorator to validate client data received in json format by comparing it to the schema rules.

"""
from app.constants.auth_token_purpose import TokenPurpose
from app.constants.auth_methods import AuthMethods
from app.constants.auth_password_change import PasswordChangeReason

from app.constants.validation_input_length import INPUT_LENGTH
from app.constants.validation_patterns import EMAIL_PATTERN, OTP_PATTERN

# Enum to list
token_purpose_values = [purpose.value for purpose in TokenPurpose]
"""purpose can be: 'pw_reset', 'pw_change', 'email_change_old_email', 'email_change_new_email', 'email_verification'"""

pw_change_reason = [reason.value for reason in PasswordChangeReason]
"""reason can be: 'reset', 'change'"""

####################################
#    CREDENTIAL CHANGE SCHEMAS     #
####################################

change_password_schema = {
    "type": "object",
    "title": "Will change a user's password",
    "properties": {
        "new_password": {
            "description": "Can accept passwords only.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], # should be the same as OTP length
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            },
        "old_password": {
            "description": "Can accept passwords only.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], # should be the same as OTP length
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            },
        "otp": {
            "description": "Can only accept otp.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['otp']['minValue'], 
            "maxLength": INPUT_LENGTH['otp']['maxValue'], 
            "pattern": OTP_PATTERN
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. Optional.",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            },
        "honeypot": {
            "description": "Designed for catching bots.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
            }
    },
    "additionalProperties": False,
    "required": ["new_password", "honeypot"]
}


request_password_reset_schema = {
    "type": "object",
    "title": "Will send a token per email so user may reset password", 
    "properties": {
        "email": {
            "description": "Email of user logging in.",
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN},
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            },
        "honeypot": { #TODO: rename
            "description": "Designed for catching bots.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
            },
    },
    "additionalProperties": False,
    "required": ["email", "honeypot"]
}


password_reset_schema = {
    "type": "object",
    "title": "Will send a token per email so user may reset password", 
    "properties": {
        "email": {
            "description": "Email of user resetting password.",
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN},
        "new_password": {
            "description": "Can accept passwords only.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], # should be the same as OTP length
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            },
        "security_code_1": {
            "description": "Can accept security code only.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], # should be the same as OTP length
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            },
        "security_code_2": {
            "description": "Can accept security code only.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], # should be the same as OTP length
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            },
        "honeypot": { #TODO: rename
            "description": "Designed for catching bots.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
            },
    },
    "additionalProperties": False,
    "required": ["email", "new_password", "security_code_1", "honeypot"]
}

request_change_email_schema = {
    "type": "object",
    "title": "Will start the email change process.",
    "properties": {
        "new_email": {
            "description": "The email the user wants to change to.",
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN},
        "password": {
            "description": "Can accept passwords only.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], # should be the same as OTP length
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            # "pattern": PASSWORD_PATTERN
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. Optional.",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            },
        
    },
    "additionalProperties": False,
    "required": ["new_email", "password"]
}

change_email_schema = {
    "type": "object",
    "title": "Will change a user's email or start the process by sending email tokens",
    "properties": {
        "security_code_1": {
            "description": "Can accept security code only.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], # should be the same as OTP length
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            },
        "security_code_2": {
            "description": "Can accept security code only.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], # should be the same as OTP length
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. Optional.",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            },
        
    },
    "additionalProperties": False,
    "required": ["security_code_1"]
}

# change_email_token_validation_schema = {
#     "type": "object",
#     "title": "Will change a user's email or start the process by sending email tokens",
#     "properties": {
#         "signed_token": {
#             "description": "The signed token",
#             "type": "string",
#             "minLength": INPUT_LENGTH['signed_token']['minValue'],
#             "maxLength": INPUT_LENGTH['signed_token']['maxValue'],
#             },
#         "purpose": {
#             "description": "Token purpose can be one of: TokenPurpose enum. This should answer the questions: what is this token validating? ",
#             "type": "string",
#             "enum": token_purpose_values,
#             },
#         "user_agent": {
#             "description": "The HTTP User-Agent request header. Optional.",
#             "type": "string", 
#             "minLength": INPUT_LENGTH['user_agent']['minValue'], 
#             "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
#             },
        
#     },
#     "additionalProperties": False,
#     "required": ["signed_token", "purpose"]
# }