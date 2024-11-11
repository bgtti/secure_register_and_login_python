"""
**The config package**

Contains the files necessary to configure the application.

--------------------------------------
This application can be configured for different environments, with each environment’s configuration class defined in separate files:

- **BaseConfig**: The base class for all configuration classes, located in *config_base.py*.
- **DevelopmentConfig**: Configures the application for "local" and "development" environments, found in *config_dev.py*.
- **ProductionConfig**: Configures the application for the "production" environment, located in *config_prod.py*.
- **TestingConfig**: Configures the application for running tests, located in *config_test.py*.

`LOGGING_CONFIG` is a dictionary in *logging_config.py* that defines log management and can be imported into other configuration classes.

Configuration relies on constants that should be set by the developer in an .env file. If these values are undefined or incorrectly formatted, default values are applied. Functions in *value_setter.py* validate and define these critical constants, with final values imported into *values.py*.

*values.py* serves as the central source for **configuration constants**, used by configuration classes, manage.py, and other parts of the project.
"""

