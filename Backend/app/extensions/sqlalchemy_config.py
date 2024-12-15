"""
**ABOUT THIS FILE**

sqlalchemy_config.py defines a custom type decorator that forces all retrieved datetimes to be timezone-aware and in UTC.

This was implemented because the database or driver was returning naive datetime objects despite using `timezone=True`in db models, like: `db.Column(db.DateTime(timezone=True))`. This caused type errors and inconsistencies in datetime handling. Thus, the need to enforce timezone-awareness at runtime.


### Usage
Make sure add datetime in db models with `datetime.now(timezone.utc)`.
Replace the usual `db.DateTime` with `UTCDateTime` (custom type defined in this file)

Example:
```python
class ModelExample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    updated_date = db.Column(UTCDateTime, nullable=True)
```

### More information
With this approach:
- All stored datetimes must be timezone-aware (validated during storage).
- All retrieved datetimes will always be timezone-aware in UTC.
"""
from sqlalchemy.types import TypeDecorator, DateTime
from datetime import timezone

class UTCDateTime(TypeDecorator):
    """A custom DateTime type that enforces timezone awareness in UTC."""
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