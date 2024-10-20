from flask import request, jsonify
import logging
# defines what happens when client exceed call limits
# used in config.py to configure flask-limiter
def rate_limit_exceeded(rate_limit):
    """
    Function used in config.py to configure flask-limiter.
    Defines what happens when client exceed call limits.
    """
    # Log the fact that a request was denied due to rate limiting
    client_ip = request.remote_addr
    logging.warning(f"Rate limit exceeded for client IP: {client_ip}")
    return jsonify({"error": "ratelimit exceeded", "message": str(rate_limit)}), 429