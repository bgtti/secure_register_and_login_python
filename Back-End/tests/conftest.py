import pytest

from app import create_app
# from app import create_app, db
from app.extensions import db 
from app.config import TestConfig

# Simulate DB
@pytest.fixture()
def app_test():
    app_test = create_app(TestConfig)

    with app_test.app_context():
        db.create_all()

    yield app_test

# Clean up db after testing
# @pytest.fixture(scope='function')
# def clean_db(app_test):
#     with app_test.app_context():
#         db.drop_all()
#         db.create_all()
#     yield

# Simulate requests
@pytest.fixture()
def client(app_test):
    return app_test.test_client()

# Run tests in terminal with the command: pytest