"""
**ABOUT THIS FILE**

user_settings/schemas.py contains the json schemas to validate request data in the user_settings routes.

------------------------
## More information

These schemas are passed in to `validate_schema` (see `app/utils/custom_decorators/json_schema_validator.py`) through the route's decorator to validate client data received in json format by comparing it to the schema rules.

"""
from app.utils.constants.account_constants import INPUT_LENGTH

set_mailing_list_schema = {
    "type": "object",
    "title": "Enters or removes user from mailing list", 
    "properties": {
        "mailing_list": {
            "description": "Boolean to signify whether user should be in mailing list (true) or not (false).",
            "type": "boolean", 
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },
    "additionalProperties": False,
    "required": ["mailing_list"]
}

set_night_mode_schema = {
    "type": "object",
    "title": "Set user nightmode preferences.", 
    "properties": {
        "night_mode": {
            "description": "Boolean to signify whether user wants night mode (true) or not (false).",
            "type": "boolean", 
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },
    "additionalProperties": False,
    "required": ["night_mode"]
}