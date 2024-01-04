# Note on analytics_schema:
# screen_size should be formatted as: (num1 x num2)
# where num1 is the value for window.screen.height and num2 is the value for window.screen.width, both in pixels
# regex: 
# \(: Matches the opening parenthesis.
# \d+: Matches one or more digits.
# x: Matches the letter "x".
# \d+: Matches one or more digits again.
# \): Matches the closing parenthesis.

SCREEN_SIZE_PATTERN = r'\(\d+ x \d+\)'

analytics_schema = {
    "type": "object",
    "properties": {
        "page": {
            "type": "string", 
            "minLength": 0, 
            "maxLength": 50
            },
        "referrer": {
            "type": "string", 
            "minLength": 0, 
            "maxLength": 200
            },
        "screen_size": {
            "type": "string", 
            "minLength": 5, 
            "maxLength": 50,
            "pattern": SCREEN_SIZE_PATTERN
            },
        "operating_system": {
            "type": "string", 
            "minLength": 1, 
            "maxLength": 50
            },
        "user_agent": {
            "type": "string", 
            "minLength": 0, 
            "maxLength": 200
            }
    },
    "additionalProperties": False,
    "required": ["page", "referrer", "screen_size", "operating_system", "user_agent"]
}