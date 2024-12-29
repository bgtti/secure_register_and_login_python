"""
**ABOUT THIS FILE**

auth/schemas.py contains the json schemas to validate request data in the auth routes.

------------------------
## More information

These schemas are passed in to `validate_schema` (see `app/utils/custom_decorators/json_schema_validator.py`) through the route's decorator to validate client data received in json format by comparing it to the schema rules.

"""
from app.utils.constants.account_constants import INPUT_LENGTH, NAME_PATTERN, EMAIL_PATTERN, PASSWORD_PATTERN, OTP_PATTERN
from app.utils.constants.enum_class import TokenPurpose, LoginMethods

# Enum to list
token_purpose_values = [purpose.value for purpose in TokenPurpose]
"""purpose can be: 'pw_change', 'email_change_old_email', 'email_change_new_email', 'email_verification'"""

login_method_values = [method.value for method in LoginMethods]
"""method can be: 'otp', 'password'"""

####################################
#      REGISTRATION SCHEMAS        #
####################################

signup_schema = {
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
        "honeypot": {
            "description": "Designed for catching bots.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
            },
    },
    "additionalProperties": False,
    "required": ["email", "password","method", "honeypot"]
}

####################################
#         PROFILE SCHEMAS          #
####################################

change_name_schema = {
    "type": "object",
    "title": "Will change a user's name.", 
    "properties": {
        "new_name": {
            "description": "The name the user wishes to have. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['name']['minValue'], 
            "maxLength": INPUT_LENGTH['name']['maxValue'],
            "pattern": NAME_PATTERN
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },
    "additionalProperties": False,
    "required": ["new_name"]
}

req_auth_change_schema = {
    "type": "object",
    "title": "Request a change of user password or email. First step of 2-step process.", 
    "properties": {
        "type": {
            "description": "Request type can be either 'email' or 'password'. ",
            "type": "string",
            "enum": ["email", "password"],
            },
        "new_email": {
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'],
            "pattern": EMAIL_PATTERN
            },
        "user_agent": {
            "type": "string", 
            "minLength": 0, 
            "maxLength": 255 #TODO get regex pattern
            }
        # "new_password": {
        #     "type": "string", 
        #     "minLength":  INPUT_LENGTH['password']['minValue'], 
        #     "maxLength": INPUT_LENGTH['password']['maxValue'], 
        #     "pattern": PASSWORD_PATTERN
        #     },
    },
    "additionalProperties": False,
    "required": ["type"]
}

req_token_validation_schema = {
    "type": "object",
    "title": "Validate a token that leads to password or email change.", 
    "properties": {
        "signed_token": {
            "description": "The signed token",
            "type": "string",
            "minLength": INPUT_LENGTH['signed_token']['minValue'],
            "maxLength": INPUT_LENGTH['signed_token']['maxValue'],
            },
        "purpose": {
            "description": "Token purpose can be one of: TokenPurpose enum. This should answer the questions: what is this token validating? ",
            "type": "string",
            "enum": token_purpose_values,
            },
        "new_password": {
            "description": "New password only required if the purpose is to change passwords",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], 
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        # "user_agent": {
        #     "type": "string", 
        #     "minLength": 0, 
        #     "maxLength": 255 #TODO get regex pattern
        #     },
    },
    "additionalProperties": False,
    "required": ["signed_token", "purpose"]
}

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
    },

    "additionalProperties": False,
    "required": ["email", "password","otp"]
}