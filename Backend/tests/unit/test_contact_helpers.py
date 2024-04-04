from app.routes.contact.helpers import contact_form_email_forwarding
from unittest.mock import patch

def test_contact_form_email_forwarding():
    """
    GIVEN a name, email, message and whether the message was sent by a registered user
    CHECK that the message is forwarded to the email set up in the configuration files
    """
    # Test case 1: Email credentials not set up
    with patch("app.routes.contact.helpers.EMAIL_CREDENTIALS", {"email_set": False}):
        result = contact_form_email_forwarding("John Doe", "john@example.com", "Hello", is_user=True, email_in_db="john@example.com")
        assert result == False

    # Test case 2: Successful email forwarding
    with patch("app.routes.contact.helpers.EMAIL_CREDENTIALS", {"email_set": True, "email_address": "admin@example.com"}), \
        patch("app.routes.contact.helpers.mail.send") as mock_send:
        result = contact_form_email_forwarding("John Doe", "john@example.com", "Hello", is_user=True, email_in_db="john@example.com")
        assert result == True
        mock_send.assert_called_once()

    # Test case 3: Email forwarding failure
    with patch("app.routes.contact.helpers.EMAIL_CREDENTIALS", {"email_set": True, "email_address": "admin@example.com"}), \
        patch("app.routes.contact.helpers.mail.send") as mock_send:
        mock_send.side_effect = Exception("Email send error")
        result = contact_form_email_forwarding("John Doe", "john@example.com", "Hello", is_user=True, email_in_db="john@example.com")
        assert result == False