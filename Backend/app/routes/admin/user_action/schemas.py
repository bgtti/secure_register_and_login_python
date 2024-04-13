from app.utils.constants.enum_class import UserFlag

user_flag_values = [flag.value for flag in UserFlag]

admin_user_flag_change = {
    "type": "object",
    "title": "Change a user's flag colour", 
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

admin_user_access_type_change = {
    "type": "object",
    "title": "Change a user's access type to admin or regular user.", 
    "properties": {
        "user_id": {
            "description": "Id of user whose type needs changing.",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "new_type": {
            "description": "A user's type can be either 'user' or 'admin'.",
            "type": "string",
            "enum": ["user", "admin"],
            },
    },
    "additionalProperties": False,
    "required": ["user_id", "new_type"]
}

admin_block_and_unblock_user_schema = {
    "type": "object",
    "title": "Users table pagination", 
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
    "title": "Users table pagination", 
    "properties": {
        "user_id": {
            "description": "Id of user to delete.",
            "type": "integer",
            "exclusiveMinimum": 0 
            }
    },
    "additionalProperties": False,
    "required": ["user_id"]
}