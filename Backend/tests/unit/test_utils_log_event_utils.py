import pytest
from app.utils.log_event_utils.log import log_event
from app.models.log_event import LogEvent

def test_log_event(app_test):
    """
    GIVEN the name of an action and event
    CHECK whether the log function saves the log to the database appropriately
    """
    # Mock user_id and extra_info
    user_id = 123456789
    extra_info = "Additional information"

    with app_test.app_context():
        # Test with valid parameters
        log_event("ACCOUNT_SIGNUP", "signup successful", user_id=user_id, extra_info=extra_info)

        # Retrieve the last added log event
        last_log_event = LogEvent.query.filter_by(user_id=user_id).first()

        # Check that the log event matches the expected values
        assert last_log_event is not None  # Ensure last_log_event is not None
        assert last_log_event.activity == "signup"
        assert last_log_event.message == "successful signup. Additional information"

        # Test with invalid event activity
        with pytest.raises(ValueError):
            log_event("INVALID_ACTIVITY", "signup successful")

        # Test with invalid event code
        with pytest.raises(ValueError):
            log_event("ACCOUNT_SIGNUP", "invalid event code")

        # Test with missing user_id for a required event
        with pytest.raises(ValueError):
            log_event("ACCOUNT_SIGNUP", "signup successful")

        # Test with missing user_id for a non-required event
        log_event("ACCOUNT_SIGNUP", "user exists")  # Should not raise an exception

        # Test with empty extra_info
        log_event("ACCOUNT_LOGIN", "login successful", user_id=user_id, extra_info="")  # Should not raise an exception