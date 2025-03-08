from app.utils.constants.account_constants import INPUT_LENGTH, NAME_PATTERN
from app.utils.constants.enum_class import TokenPurpose, AuthMethods, PasswordChangeReason

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