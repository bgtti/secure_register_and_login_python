"""
**ABOUT THIS FILE**

rate_limit_config.py contains the **rate_limit_exceeded** function. It determines what happens when a client exceeds the call limits.

This is used in config_base.py to configure flask-limiter.

"""
from flask import request, jsonify
import logging

def rate_limit_exceeded(rate_limit):
    """
    Function used to configure flask-limiter.
    Defines what happens when client exceed call limits: 429 error.
    See the Flask-Limiter documentation for more information.
    """
    # Log the fact that a request was denied due to rate limiting
    client_ip = request.remote_addr
    logging.warning(f"Rate limit exceeded for client IP: {client_ip}")
    return jsonify({"error": "ratelimit exceeded", "message": str(rate_limit)}), 429