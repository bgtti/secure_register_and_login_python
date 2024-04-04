from flask import Flask, request, jsonify
from app.utils.bot_detection.bot_detection import bot_caught
from app.extensions import db
from app.models.bot_catch import BotCatch
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.ip_utils.ip_geolocation import geolocate_ip 

def test_bot_capture(app_test):
    """
    GIVEN a request object and form name
    CHECK whether a bot is added to the database
    WHILE not raising an error
    """
    # Example data
    request_data = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    form_targeted = "login"

    # Simulate an IP address in the Flask request context
    with app_test.test_request_context(json=request_data):
        request.environ["REMOTE_ADDR"] = "172.217.30.9"  # Simulated IP address

        # Call the bot_caught function
        result = bot_caught(request, form_targeted)

    # Check if the function returns None (as it always does)
    assert result is None

    # Check if the bot information is stored in the database
    with app_test.app_context():
        bot = BotCatch.query.first()
        assert bot is not None
        assert bot.ip_address == "unknown"  # Update with the expected IP address
        assert bot.country == "unknown"  # Update with the expected values
        assert bot.user_agent == request_data["user_agent"]
        assert bot.form_targeted == form_targeted