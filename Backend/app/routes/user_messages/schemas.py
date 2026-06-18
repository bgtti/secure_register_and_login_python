user_thread_table_schema = {
    "type": "object",
    "title": "Table of threads relevant to the user.", 
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
            "maximum": 25, 
            }
    },
    "additionalProperties": False,
    "required": ["page_nr", "items_per_page"]
}

user_messages_table_schema = {
    "type": "object",
    "title": "Table of messages belonging to a message thread.", 
    "properties": {
        "thread_id": {
            "description": "Page number as int > 0",
            "type": "integer",
            "exclusiveMinimum": 0 
            },
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
            "maximum": 25, 
            }
    },
    "additionalProperties": False,
    "required": ["thread_id", "page_nr", "items_per_page"]
}