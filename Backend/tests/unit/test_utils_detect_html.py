import pytest
from app.utils.detect_html.detect_html import check_for_html

@pytest.mark.parametrize("data, route, user_email, expected_result", [
    ("<base href='http://example.com/'>", "signup: name field input", "user@example.com", True),
    ("John", "signup: name field input", "user@example.com", False),
    # Add more test cases as needed
])
def test_check_for_html(data, route, user_email, expected_result):
    """
    GIVEN some data and information about the route and user
    CHECK whether the data contains html or possible xss vectors
    WHILE not raising an exception
    """
    result = check_for_html(data, route, user_email)
    assert result == expected_result