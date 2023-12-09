import json
from app.models.user import User

def test_signup_user(client, app_test):
    """
    GIVEN a JSON object with name, email, and password
    CHECK user registration
    """
    data = {"name": "Test Joe", "email": "test@apptest.com", "password": "joeTesting067!"}
    
    with app_test.app_context():
        response = client.post("/api/account/signup", json=data)

        assert response.status_code == 200
        user = User.query.filter_by(email=data["email"]).first()
        assert user.name == "Test Joe"

        # Add more assertions based on your requirements

        # You can also check the response data
        response_data = json.loads(response.data)
        assert response_data["response"] == "success"
        assert "user_id" in response_data
        assert "user" in response_data
        assert response_data["user"]["name"] == "Test Joe"
        assert response_data["user"]["email"] == "test@apptest.com"
