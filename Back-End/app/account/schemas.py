# Sign up
sign_up_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 1, "maxLength": 30},
        "email": {"type": "string", "minLength": 1, "maxLength": 30},
        "password": {"type": "string", "minLength": 1, "maxLength": 30},
    },
    "additionalProperties": False,
    "required": ["username", "email", "password"]
}