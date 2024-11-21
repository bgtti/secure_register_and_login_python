import json
import ast
from datetime import datetime, timezone
from flask_login import login_user, logout_user
from config.values import SUPER_USER
from Backend.app.extensions.extensions import flask_bcrypt, db
from Backend.app.extensions.extensions import faker
from app.models.user import User
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper
from app.utils.constants.enum_class import modelBool, UserAccessLevel, UserFlag
from app.utils.constants.enum_class import UserAccessLevel
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper

def test_admin_users_table(client, app_test):
    """
    GIVEN a JSON object with filtering and pagination parameters
    CHECK admin users table response and status
    """
    # Log in the admin user
    with app_test.test_request_context():
        # Create super admin
        ADMIN_NAME = SUPER_USER["name"]
        ADMIN_EMAIL = SUPER_USER["email"]
        ADMIN_PW = SUPER_USER["password"]
        date = datetime.now(timezone.utc)
        salt = generate_salt()
        pepper = get_pepper(date)
        salted_password = salt + ADMIN_PW + pepper
        hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')
        super_admin = User(
            name=ADMIN_NAME, 
            email=ADMIN_EMAIL, 
            password=hashed_password, 
            salt=salt, 
            created_at=date
            )
        db.session.add(super_admin)
        super_admin.make_user_super_admin(ADMIN_PW)
        db.session.commit()

        # Make sure super admin was created
        user_is_admin = User.query.filter_by(email=ADMIN_EMAIL).first()
        assert user_is_admin.access_level == UserAccessLevel.SUPER_ADMIN

        # Prepare JSON data for the request
        json_data = {
            "page_nr": 1,
            "items_per_page": 25,
            "order_by": "last_seen",
            "order_sort": "descending",
            "filter_by": "none",
            "filter_by_flag": "not_blue",
            "filter_by_last_seen":"2024-01-01",
            "search_by": "none",
            "search_word": ""
        }

        # Test 1: no users are found and route is accessed by super admin
        login_user(super_admin)
        response_no_users = client.post("api/admin/restricted_area/users", json=json_data)
        assert response_no_users.status_code == 200
        response_json = response_no_users.get_json()
        assert "response" in response_json
        assert "users" in response_json
        users_list = response_json["users"]
        assert len(users_list) == 0
        logout_user()

        # Test 2: users are found and route is accessed by admin
        # Create a test admin user
        user_name = "John Test"
        user_email = "test@apptest.com"
        user_password = "joeTesting067!"

        date = datetime.now(timezone.utc)
        salt = generate_salt()
        pepper = get_pepper(date)
        salted_password = salt + user_password + pepper
        hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode("utf-8")
        admin_user = User(name=user_name, email=user_email, password=hashed_password, salt=salt, created_at=date)
        db.session.add(admin_user)
        admin_user.make_user_admin()
        db.session.commit()
        login_user(admin_user)

        # Create some users
        for _ in range(25):
            faker.ascii_email()
            user = User(name=faker.name(), email=faker.ascii_email(), password=hashed_password, salt=salt, created_at=date)
            db.session.add(user)
            db.session.commit()

        user_count = User.query.count()
        assert user_count > 25

        response = client.post("api/admin/restricted_area/users", json=json_data)

        # Check the response status code
        assert response.status_code == 200

        # Parse the JSON response and check its content
        response_data = json.loads(response.data)
        assert response_data["response"] == "success"
        assert "users" in response_data
        assert "total_pages" in response_data
        assert "current_page" in response_data
        assert "query" in response_data

        logout_user()

        # Test 3: search for specfic user
        json_data_copy = json_data.copy()
        json_data_copy["search_word"] = user_name
                
        login_user(admin_user)
        response = client.post("api/admin/restricted_area/users", json=json_data_copy)
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert any(user["name"] == user_name for user in response_data["users"])
        logout_user()

        # Test 4: order by name, ascending
        json_data_copy = json_data.copy()
        json_data_copy["order_by"] = "name"
        json_data_copy["order_sort"] = "ascending"
                
        login_user(admin_user)
        response = client.post("api/admin/restricted_area/users", json=json_data_copy)
        assert response.status_code == 200
        response_data = json.loads(response.data)
        users_ascending = response_data["users"]
        assert all(users_ascending[i]["name"] <= users_ascending[i + 1]["name"] for i in range(len(users_ascending) - 1))
        logout_user()

        # Test 5: filter by is_blocked
        admin_user.block_access()
        db.session.commit()

        json_data_copy = json_data.copy()
        json_data_copy["filter_by"] = "is_blocked"

        login_user(super_admin)
        response = client.post("api/admin/restricted_area/users", json=json_data_copy)
        assert response.status_code == 200
        response_data = json.loads(response.data)
        users_blocked = response_data["users"]
        assert len(users_blocked) == 1
        assert users_blocked[0]["name"] == user_name

