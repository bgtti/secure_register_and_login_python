# import jsonschema
# import pytest
# from app.routes.auth.schemas import sign_up_schema

# def test_signup_schema():
#     """
#     GIVEN an abject with name, email, password, and honeypot
#     CHECK whether it can be validated by the json schema
#     WHILE making it possible for user to use a great range of character choices
#     """
#     # Valid data
#     valid_data_1 = {
#         "name": "John Doe",
#         "email": "john.doe@example.com",
#         "password": "StrongPassword123",
#         "honeypot": "hello honey",
#     }
#     valid_data_2 = {
#         "name": "Sinéad O'Connor",
#         "email": "john.doe@example.com",
#         "password": "StrongPassword123",
#         "honeypot": "",
#     }
#     valid_data_3 = {
#         "name": "François-Marie Arouet",
#         "email": "john.doe@example.com",
#         "password": "StrongPassword123",
#         "honeypot": "",
#     }
#     valid_data_4 = {
#         "name": "Sabiha M. Gökçen",
#         "email": "john.doe@example.com",
#         "password": "StrongPassword123",
#         "honeypot": "",
#     }

#     # Invalid data with missing 'name'
#     invalid_data_missing_name = {
#         "email": "john.doe@example.com",
#         "password": "StrongPassword123",
#         "honeypot": "",
#     }

#     # Invalid data with short 'password'
#     invalid_data_short_password = {
#         "name": "John Doe",
#         "email": "john.doe@example.com",
#         "password": "Weak",
#         "honeypot": "",
#     }

#     # Invalid data not matching pattern
#     invalid_data_pattern = {
#         "name": "<img src=x onerror=alert('XSS')>",
#         "email": "john.doe@example.com",
#         "password": "StrongPassword123",
#         "honeypot": "",
#     }

    

#     # Validate the schema against data
#     jsonschema.validate(instance=valid_data_1, schema=sign_up_schema)  # Should not raise an exception
#     jsonschema.validate(instance=valid_data_2, schema=sign_up_schema)  # Should not raise an exception
#     jsonschema.validate(instance=valid_data_3, schema=sign_up_schema)  # Should not raise an exception
#     jsonschema.validate(instance=valid_data_4, schema=sign_up_schema)  # Should not raise an exception

#     with pytest.raises(jsonschema.exceptions.ValidationError):
#         jsonschema.validate(instance=invalid_data_missing_name, schema=sign_up_schema)

#     with pytest.raises(jsonschema.exceptions.ValidationError):
#         jsonschema.validate(instance=invalid_data_short_password, schema=sign_up_schema)

#     with pytest.raises(jsonschema.exceptions.ValidationError):
#         jsonschema.validate(instance=invalid_data_pattern, schema=sign_up_schema)
