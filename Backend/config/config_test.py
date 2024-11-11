"""
**ABOUT THIS FILE**

config_test.py contains the **TestingConfig** class, used to set up the test environment. 

Check the *tests* directory to see the test files and check out how the class is used.

"""
from config.config_dev import DevelopmentConfig

class TestingConfig(DevelopmentConfig):
    # Flask Config
    TESTING = True

    # Database Config
    # SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    # Flask-Limiter Config
    RATELIMIT_ENABLED = False # Only makes sense if testing this specific functionality.
    RATELIMIT_STORAGE_OPTIONS = {}  # Empty storage options for testing
    RATELIMIT_DEFAULT = "10/day"  # Adjust this rate limit as needed for your tests
    #RATELIMIT_STORAGE_URI = "redis://localhost:6379/2"