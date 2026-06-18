"""
Docstring for Backend.app.services

What is a Service Package?

A service package is a directory (e.g., app/services/) that contains Python modules with functions or classes that:

- operate on your models
- contain application-specific business rules
- orchestrate multi-step operations
- should not be in your SQLAlchemy models
- should not be in the Flask routes

It’s a layer between routes and models.

How file naming is done here:

[name-of-db-model]_[optional:subgrouping name]_service.py

They should:
- use the model
- be consumed (used) by the routes

They should not:
be consumed by the model

*** models should NOT consume services.***

do not call db.session.commit() inside a service!
reasons why:

1. Harder to compose operations

You might want to:
- update the user,
- log an event,
- send an email,
...and only then commit if all succeed.
If one service already committed, you can’t roll everything back anymore.

2. Hidden side effects

A function called register_failed_login(user) sounds like “I just adjust some fields”, but secretly it’s writing to the DB. That’s surprising and makes bugs harder to track.

3. Testing becomes painful: mocking and isolation are harder.

4. Transaction boundaries should be explicit

You generally want one clear place where you say:
“OK, all good, now persist this whole thing.”


So what should services do with the DB?

Typical pattern:

✅ Modify models (user.login_attempts += 1, user.is_blocked = True, etc.)
✅ Optionally call db.session.add(obj) if they create new objects
❌ Do not call db.session.commit() (or rollback()), except in very top-level orchestration functions.



EXAMPLE:

app/
  services/
    auth/
      __init__.py
      login_service.py
      otp_service.py
      password_reset_service.py
    users/
      user_service.py
      profile_service.py
    logging/
      activity_log_service.py
      security_log_service.py
    anti_abuse/
      honeypot_service.py
      rate_limit_service.py
      spam_service.py
    billing/
      invoice_service.py
      payment_service.py
"""