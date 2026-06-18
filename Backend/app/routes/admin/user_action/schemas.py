from app.constants.flags import Flag

user_flag_values = [flag.value for flag in Flag]

change_user_flag_schema = {
    "type": "object",
    "title": "Change a user's flag colour.", 
    "properties": {
        "user_id": {
            "description": "Id of user to change flag.",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "new_flag_colour": {
            "description": "Flag colour to flag user.",
            "type": "string",
            "enum": user_flag_values,
            },
    },
    "additionalProperties": False,
    "required": ["user_id", "new_flag_colour"]
}

user_role_change_schema = {
    "type": "object",
    "title": "Change a user's role to admin or regular user.", 
    "properties": {
        "user_id": {
            "description": "Id of user whose type needs changing.",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "new_role": {
            "description": "A user's type can be either 'user' or 'admin'.",
            "type": "string",
            "enum": ["user", "admin"],
            },
    },
    "additionalProperties": False,
    "required": ["user_id", "new_role"]
}

block_and_unblock_user_schema = {
    "type": "object",
    "title": "Block or unblock user's access to their accounts.", 
    "properties": {
        "user_id": {
            "description": "Id of user to block/unblock.",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "block": {
            "description": "Set to true if user should be blocked or false to unblock.",
            "type": "boolean",
            }
    },
    "additionalProperties": False,
    "required": ["user_id", "block"]
}

admin_delete_user_schema = {
    "type": "object",
    "title": "Delete a user's account.", 
    "properties": {
        "user_id": {
            "description": "Id of user to delete.",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "reason": {
            "description": "Reason given by admin to delete a user's account.",
            "type": "string",
            "minLength":  1, 
            "maxLength": 200, 
            },
    },
    "additionalProperties": False,
    "required": ["user_id", "reason"]
}