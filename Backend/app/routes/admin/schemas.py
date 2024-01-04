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
            "description": "What items are ordered by. Defaults to 'last seen' if not specified.",
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
            "enum": ["none", "is_blocked"],
            },
    },
    "additionalProperties": False,
    "required": ["page_nr"]
}