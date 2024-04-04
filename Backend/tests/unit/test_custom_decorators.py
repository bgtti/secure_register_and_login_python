from flask import Flask, jsonify
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.utils.custom_decorators.admin_protected_route import admin_only
from flask_login import UserMixin, login_user, logout_user, login_required
from app.extensions import login_manager
from app.utils.constants.enum_class import UserAccessLevel

def test_validate_schema():
    """
    GIVEN an object
    CHECK whether it passes through the json schema validation
    WHILE using the json schema validation decorator
    """
    app = Flask(__name__)

    @app.route("/test_route", methods=["POST"])
    @validate_schema({"type": "object", "properties": {"key": {"type": "string"}}})
    def test_route():
        return jsonify({"response": "Success"})

    with app.test_client() as client:
        # Test with a valid payload
        response = client.post("/test_route", json={"key": "value"})
        assert response.status_code == 200

        # Test with an invalid payload
        response = client.post("/test_route", json={"key": 123})
        assert response.status_code == 400

def test_admin_protected_route(client, app_test):
    """
    GIVEN a user
    CHECK whether it passes through the admin requirement validation
    WHILE using the admin validation decorator
    """
    
    app = app_test

    class MockUser(UserMixin):
        def __init__(self, access_level, id):
            self.id = id
            self.access_level = access_level
        def get_id(self):
            return str(self.id)
    user_super_admin = MockUser(UserAccessLevel.SUPER_ADMIN, 1)
    user_admin = MockUser(UserAccessLevel.ADMIN, 2)
    user_regular = MockUser(UserAccessLevel.USER, 3)

    @login_manager.user_loader
    def load_user(user_id):
        return MockUser.query.get(int(user_id))

    @app.route("/test_route", methods=["GET"])
    @login_required
    @admin_only
    def test_route():
        return jsonify({"response": "Success"})
    
    # Test the decorator with a user who has SUPER_ADMIN access
    with app.test_request_context():
        login_user(user_super_admin)
        with client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 'super_admin_user_id'
            current_user = user_super_admin
            response = c.get("/test_route")
            assert response.status_code == 200
        logout_user()

    # Test the decorator with a user who has ADMIN access
    with app.test_request_context():
        login_user(user_admin)
        with client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 'admin_user_id'
            current_user = user_admin
            response = c.get("/test_route")
            assert response.status_code == 200
        logout_user()

    # Test the decorator with a user who doesn't have required access level
    with app.test_request_context():
        login_user(user_regular)
        with client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 'regular_user_id'
            current_user = user_regular  # Regular user
            response = c.get("/test_route")
            assert response.status_code == 401
        logout_user()
