"""
**ABOUT THIS FILE**

login_manager_config.py defines the decorators essential for the `login_manager`'s functionality within the authentication process. 

*Ps: `login_manager` is the `LoginManager` class from Flask-Login that was created in `extensions.py`*

Specifically, it includes:
- **`load_user`**: Decorator for `@login_manager.user_loader` to load users by ID or session ID.
- **`unauthorized`**: Decorator for `@login_manager.unauthorized_handler` to handle unauthorized access attempts.

These decorators are registered automatically with `login_manager` when `init_app(app)` is called, making them active within the Flask app context. 

### Usage
Ensure this file is imported in the module where `create_app` is defined:
```python
from app.extensions import login_manager_config as flask_login_config  # Importing here is enough for registration
```

### More information
Flask-Login documentation:  https://flask-login.readthedocs.io/en/latest/#configuring-your-application
"""
from flask import jsonify
from app.extensions.extensions import login_manager
from app.models.user import User

# TODO review the notes in this file

# Ps: The reason we use session id instead of regular id when user chooses to be remembered is that remembered tokens must be changed to invalidate sessions.

# The reason the session id is not being used all the time is that it is a uuid, and those do not perform very well on db queries.

@login_manager.user_loader
def load_user(user_id):
    """
    Used by flask_login to create sessions. Uses user.get_id() method. 
    If user chose to be remembered, a session uuid will be used. 
    Else, the regular user's id wil be used. 
    TODO: change this: user should be queried by an alternative id
    """
    if user_id.isdigit():
        # If the user_id is a digit, assume it's a regular ID
        return User.query.get(int(user_id))
    else:
        # If the user_id is not a digit, assume it's a session ID
        return User.query.filter_by(session=user_id).first()

@login_manager.unauthorized_handler
def unauthorized():
    error_response = {"response": "Route unauthorized."}
    return jsonify(error_response), 401


"""
**Session organization**

The extensions Flask-Session and Flask-Login, combined with Redis, are used for session management.

When a user logs in, Flask-Session stores the session data in Redis with a key. This session ID is stored in the client’s cookie.
When a session cookie is sent with a request, Flask-Login uses @login_manager.user_loader (defined in the login_manager_config.py file) to load the user. It queries the DB based on the user id or similar identifier (see the beforementioned file for specifics).

There is no mapping capabilities between users and their sessions: Flask-Login only fetches the user from the session ID and Flask-Session does not track which user belongs to which session.

This makes it difficult to log out a user - if the user has many browsers opened at the same time. 
Flask-Login's function will only log out the specific session from where a logout request came from - not others that may be associated with the user.

The docs for this reason suggest that "use an alternative user id instead of the user’s ID" to invalidate all user sessions when that alternative id is changed.

Observations about alternative id creation:
UUIDs are quite unique, but index performance is poor and it's not query-friendy.
Two decent alternative solutions:
- using Snowflake Ids
- using a unique query-friendly identifier in the format like: "user_id-random_number".

TODO: change the session logic to make logging out from all sessions possible
"""