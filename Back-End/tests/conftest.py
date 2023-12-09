import pytest
from app import create_app
from app.extensions import db 
from app.config import TestConfig

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

# Run tests in terminal with the command: pytest