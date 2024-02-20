import jsonschema
import pytest
from app.routes.account.schemas import sign_up_schema

# TODO:
# test schema against following names:
# Antonín Dvořák
# Judit Polgár
# François-Marie Arouet
# Sabiha Gökçen
# Zlatan Ibrahimović
# Paul Erdős
# Jürg M. Stauffer
# Sinéad O'Connor
# <script>window.location.href="https://evil.com"</script>
# <img src=x onerror=alert("XSS")>


def test_signup_schema():
    # Valid data
    valid_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "StrongPassword123"
    }

    # Invalid data with missing 'name'
    invalid_data_missing_name = {
        "email": "john.doe@example.com",
        "password": "StrongPassword123"
    }

    # Invalid data with short 'password'
    invalid_data_short_password = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "Weak"
    }

    # Validate the schema against data
    jsonschema.validate(instance=valid_data, schema=sign_up_schema)  # Should not raise an exception

    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(instance=invalid_data_missing_name, schema=sign_up_schema)

    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(instance=invalid_data_short_password, schema=sign_up_schema)
