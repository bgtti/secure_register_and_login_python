"""
**ABOUT THIS FILE**

auth/schemas.py contains the json schemas to validate request data in the auth routes.

------------------------
## More information

These schemas are passed in to `validate_schema` (see `app/utils/custom_decorators/json_schema_validator.py`) through the route's decorator to validate client data received in json format by comparing it to the schema rules.

"""
from app.utils.constants.account_constants import INPUT_LENGTH, NAME_PATTERN, EMAIL_PATTERN, PASSWORD_PATTERN, OTP_PATTERN


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
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },
    "additionalProperties": False,
    "required": ["name", "email", "password", "honeypot"]
}

delete_user_schema = {
    "type": "object",
    "title": "Warning: route used to delete a user",
    "properties": {
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
    "required": ["password"]
}