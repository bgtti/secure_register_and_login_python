import json
from unittest.mock import patch
from flask import url_for
from app.models.message import Message

def test_contact_form(client, app_test):
    """
    GIVEN a JSON object matching a message payload
    CHECK that the message is saved in the db
    """
    with app_test.test_request_context():
        # Test case 1: Valid form submission
        valid_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "message": "Hello, this is a test message.",
            "is_user": False,
            "honeypot": ""
        }

        response = client.post(
            url_for("contact.contactForm"),
            data=json.dumps(valid_data),
            content_type="application/json"
        )

        assert response.status_code == 200
        assert response.json["response"] == "success"

        saved_message = Message.query.filter_by(sender_email=valid_data["email"]).first()
        assert saved_message.sender_name == valid_data["name"]

        # Test case 2: Form submission with honeypot field filled (expecting 418 status code)
        honeypot_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "message": "Hello, this is a test message.",
            "is_user": False,
            "honeypot": "filled"
        }

        response = client.post(
            url_for("contact.contactForm"),
            data=json.dumps(honeypot_data),
            content_type="application/json"
        )

        assert response.status_code == 418
        assert response.json["response"] == "There was an error submitting form."

        # Test case 3: Form submission with HTML in fields
        html_data = {
            "name": "<script>alert('XSS')</script>",
            "email": "<a href='https://example.com'>Click me</a>",
            "message": "<p>This is an HTML message</p>",
            "is_user": False,
            "honeypot": ""
        }

        response = client.post(
            url_for("contact.contactForm"),
            data=json.dumps(html_data),
            content_type="application/json"
        )

        assert response.status_code == 400 # Should lead to Json Schema validation error (decorator will return 400)