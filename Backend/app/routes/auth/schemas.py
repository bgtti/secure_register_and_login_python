"""
**ABOUT THIS FILE**

auth/schemas.py contains the following schemas to validate request data:

- **signup_schema** 
- **login_schema** 

------------------------
## More information

These schemas are passed in to `validate_schema` (see `app/utils/custom_decorators/json_schema_validator.py`) through the route's decorator to validate client data received in json format by comparing it to the schema rules.

"""
from app.utils.constants.account_constants import INPUT_LENGTH, NAME_PATTERN, EMAIL_PATTERN, PASSWORD_PATTERN, OTP_PATTERN
from app.utils.constants.enum_class import TokenPurpose, LoginMethods

token_purpose_values = [purpose.value for purpose in TokenPurpose]
"""purpose can be: 'pw_change', 'email_change_old_email', 'email_change_new_email', 'email_verification'"""

login_method_values = [method.value for method in LoginMethods]
"""method can be: 'otp', 'password'"""

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
            "pattern": PASSWORD_PATTERN},
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

req_email_verification_schema = {
    "type": "object",
    "title": "Request a token be sent per email to verify account.", 
    "properties": {
        "user_agent": {
            "type": "string", 
            "minLength": 0, 
            "maxLength": 255 #TODO get regex pattern
            }
    },
    "additionalProperties": False,
    "required": ["user_agent"]
}

verify_acct_email_schema = {
    "type": "object",
    "title": "Validates token that leads to account/email verification.", 
    "properties": {
        "signed_token": {
            "description": "The signed token",
            "type": "string",
            "minLength": INPUT_LENGTH['signed_token']['minValue'],
            "maxLength": INPUT_LENGTH['signed_token']['maxValue'],
            },
    },
    "additionalProperties": False,
    "required": ["signed_token"]
}

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




#when verifying token use:
# name_of_schema = {
#     "properties": {
#         "token": {
#             "description": "Token ",
#             "type": "string",
#             "minLength": 20,
#         "maxLength": 100,
#         "pattern": "^[a-zA-Z0-9_-]+$"
#             },
#     },
# }

#when verifying token use if token is signed:
# name_of_schema = {
#     "properties": {
#         "token": {
#             "description": "Token ",
#             "type": "string",
#             "minLength": 20,
#         "maxLength": 200,
#         "pattern":  "^[a-zA-Z0-9_-]+\\.[a-zA-Z0-9_-]+$"
#             },
#     },
# }