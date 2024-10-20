admin_messages_table_schema = {
    "type": "object",
    "title": "All messages table", 
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
        "order_sort": {
            "description": "How items are ordered.",
            "type": "string",
            "enum": ["descending", "ascending"],
            },
        "filter_by": {
            "description": "What items are filtered by.",
            "type": "string",
            "enum": ["answer_needed", "answer_not_needed", "all"],
            },
        "include_spam": {
            "description": "Whether messages marked as spam should be included in the response.",
            "type": "boolean"
            },
    },
    "additionalProperties": False,
    "required": ["page_nr", "items_per_page","order_sort", "filter_by", "include_spam"]
}