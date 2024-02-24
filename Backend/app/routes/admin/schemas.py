from app.utils.constants.account_constants import INPUT_LENGTH
from app.utils.constants.enum_class import UserFlag

user_flag_values = [flag.value for flag in UserFlag]

admin_users_table_schema = {
    "type": "object",
    "title": "Users table pagination", 
    "properties": {
        "page_nr": {
            "description": "Page number as int > 0",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "items_per_page": {
            "description": "Number of items per page. Defaults to 25 if not specified.",
            "type": "integer",
            "exclusiveMinimum": 0,
            "multipleOf" : 5,
            "maximum": 50, 
            },
        "order_by": {
            "description": "What items are ordered by. Defaults to 'last_seen' if not specified.",
            "type": "string",
            "enum": ["last_seen", "name", "email", "created_at"],
            },
        "order_sort": {
            "description": "How items are ordered. Defaults to 'descending' if not specified.",
            "type": "string",
            "enum": ["descending", "ascending"],
            },
        "filter_by": {
            "description": "Filter items according to this criteria. Defaults to 'none' if not specified.",
            "type": "string",
            "enum": ["none", "is_blocked", "is_unblocked","flag", "flag_not_blue","is_admin", "is_user", "last_seen"],
            },
        "filter_by_flag": {
            "description": "If filter_by == 'flag', specify flag color. Defaults to 'blue' if not specified.",
            "type": "string",
            "enum": user_flag_values,
            },
        "filter_by_last_seen": {
            "description": "If filter_by == 'last_seen', specify date in the past. Defaults to today - 1 month if not specified. Format: YYYY-MM-DD",
            "type": "string",
            "minLength": 8, 
            "maxLength": 10, 
            "pattern": "^\d{4}-\d{1,2}-\d{1,2}$"
            },
        "search_by": {
            "description": "The parameter to use when searching a user. If no user is searched, use 'none'. Deafults to 'none'.",
            "type": "string",
            "enum": ["none", "name", "email"],
            },
        "search_word": {
            "description": "User's search input.",
            "type": "string",
            "maxLength": INPUT_LENGTH['email']['maxValue'], # because email longer than name
            }
    },
    "additionalProperties": False,
    "required": ["page_nr"]
}

admin_user_logs_schema = {
    "type": "object",
    "title": "Users table pagination", 
    "properties": {
        "user_id": {
            "description": "Id of user to delete.",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
        "page_nr": {
            "description": "Page number as int > 0",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
    },
    "additionalProperties": False,
    "required": ["user_id", "page_nr"]
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


