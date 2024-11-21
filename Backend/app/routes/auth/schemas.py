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
    "properties": {
        "new_name": {
            "type": "string", 
            "minLength": INPUT_LENGTH['name']['minValue'], 
            "maxLength": INPUT_LENGTH['name']['maxValue'],
            "pattern": NAME_PATTERN
            },
    },
    "additionalProperties": False,
    "required": ["new_name"]
}