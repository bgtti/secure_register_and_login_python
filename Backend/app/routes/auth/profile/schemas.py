from app.constants.validation_input_length import INPUT_LENGTH
from app.constants.validation_patterns import NAME_PATTERN

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