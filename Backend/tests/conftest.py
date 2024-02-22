import pytest
from app import create_app
from app.extensions import db 
from app.config import TestConfig

## Running tests
# Pytest is being used for unit testing.
# To run the tests use the following command in the terminal: python -m pytest
# Understand the basics of testing here: https://testdriven.io/blog/flask-pytest/


# Simulate DB
@pytest.fixture()
def app_test():
    app_test = create_app(TestConfig)

    with app_test.app_context():
        db.create_all()

    yield app_test

# Simulate requests
@pytest.fixture()
def client(app_test):
    return app_test.test_client()