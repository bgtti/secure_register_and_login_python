"""
**ABOUT THIS FILE**

sqlalchemy_config.py defines custom type decorators to be used in db models:
-**UTCDateTime**: forces all retrieved datetimes to be timezone-aware and in UTC.
-**EncryptedType**: forces encryption in the designated columns (using the extension cryptography) upon data saved to the db and decrypts it when retrieving from the db.


## About the UTCDateTime custom type:

This was implemented because the database or driver was returning naive datetime objects despite using `timezone=True`in db models, like: `db.Column(db.DateTime(timezone=True))`. This caused type errors and inconsistencies in datetime handling. Thus, the need to enforce timezone-awareness at runtime.

"""
import os
from datetime import timezone
from sqlalchemy.types import TypeDecorator, DateTime, String
from app.extensions.extensions import cipher

class UTCDateTime(TypeDecorator):
    """A custom DateTime type that enforces timezone awareness in UTC.

    Usage:
    Make sure to add datetime in db models with `datetime.now(timezone.utc)`.
    Replace the usual `db.DateTime` with `UTCDateTime` (custom type defined in this file)

    Example:
    ```python
    class ModelExample(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        updated_date = db.Column(UTCDateTime, nullable=True)
    ```

    With this approach:
    - All stored datetimes must be timezone-aware (validated during storage).
    - All retrieved datetimes will always be timezone-aware in UTC.
    """
    impl = DateTime(timezone=True)

    def process_result_value(self, value, dialect):
        """
        This method is called when retrieving data from the database.
        """
        if value is None:
            return value

        # Ensure the datetime is timezone-aware
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        else:
            # Convert to UTC if it has a timezone
            value = value.astimezone(timezone.utc)

        return value
    
class EncryptedType(TypeDecorator):
    """
    A custom SQLAlchemy type that encrypts data when saving to the database
    and decrypts it when loading from the database.

    Example:
    ```python

    # in the model:
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        recovery_email = Column(EncryptedType, nullable=True)

    # the code:
    user = User(recovery_email="example@example.com")
    db.session.add(user)
    db.session.commit()

    # Retrieving the user
    retrieved_user = User.query.first()
    print(retrieved_user.recovery_email)  # Output: example@example.com
    ```
    """
    impl = String  # Base type to store encrypted data as a string

    def process_bind_param(self, value, dialect):
        """
        Encrypt the value before saving to the database.
        """
        if value is None:
            return None
        # Encrypt and return as a base64-encoded string
        return cipher.encrypt(value.encode()).decode()

    def process_result_value(self, value, dialect):
        """
        Decrypt the value when retrieving from the database.
        """
        if value is None:
            return None
        # Decode and decrypt the value
        return cipher.decrypt(value.encode()).decode()