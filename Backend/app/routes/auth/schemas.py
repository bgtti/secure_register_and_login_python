"""
**ABOUT THIS FILE**

auth/schemas.py contains the following schemas to validate request data:

- **signup_schema** 
- **login_schema** 

------------------------
## More information

These schemas are passed in to `validate_schema` (see `app/utils/custom_decorators/json_schema_validator.py`) through the route's decorator to validate client data received in json format by comparing it to the schema rules.

"""
from app.utils.constants.account_constants import INPUT_LENGTH, NAME_PATTERN, EMAIL_PATTERN, PASSWORD_PATTERN

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

login_schema = {
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

auth_change_req_schema = {
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