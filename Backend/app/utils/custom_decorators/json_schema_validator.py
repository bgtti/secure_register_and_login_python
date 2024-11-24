from functools import wraps
from flask import jsonify, request
import jsonschema
import logging

def validate_schema(schema_name):
    """
    validate_schema(schema_name: JsonType) -> None
    ---------------------------------------------------------------
    Route decorator used to validate payloads against a json schema.
    Returns error 400 if request payload incorrect.
    ---------------------------------------------------------------
    Example usage:
    @blueprint_name.route("/some_route", methods=["POST"])
    @validate_schema(some_schema)
    def route_name():
    # ...
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                json_data = request.get_json()
                jsonschema.validate(instance=json_data, schema=schema_name)
            except jsonschema.exceptions.ValidationError as e:
                logging.info(f"Json schema validation error: {e}")
                return jsonify({"response": "Invalid JSON data.", "error": str(e)}), 400
            except Exception as e:
                logging.info(f"Request rejected by schema validation: {e}")
                return jsonify({"response": "Request should be a valid JSON.", "error": "An internal error has occurred."}), 400
            return f(*args, **kw)
        return wrapper
    return decorator