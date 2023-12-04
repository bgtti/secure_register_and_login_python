from flask import Blueprint, request, jsonify
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import jsonschema
import os
import ast
from dotenv import load_dotenv  # getting .env variables
from app.extensions import flask_bcrypt, db
from app.account.schemas import sign_up_schema
from app.account.salt import generate_salt
from app.models.user import User
from app.account.helpers import is_good_password
from datetime import datetime

account = Blueprint('account', __name__)

PEPPER_STRING_ARRAY = os.getenv('PEPPER') 
PEPPER_ARRAY = ast.literal_eval(PEPPER_STRING_ARRAY)

# SIGN UP
@account.route("/signup", methods=["POST"])
def signup_user():
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=json_data, schema=sign_up_schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({'response': 'Invalid JSON data.', 'error': str(e)}), 400
    
    name = json_data["name"]
    email = json_data["email"]
    password = json_data["password"]

    # Check if user already exists
    user_exists = User.query.filter_by(_email=email).first() is not None
    if user_exists:
        return jsonify({'response':'user already exists'}), 409
    
    # Check if password meets safe password criteria
    if not is_good_password(password):
        return jsonify({'response': 'Weak password.'}), 400

    # Not to use same pepper for every user, pepper array has 6 values, and pepper will rotate according to the month the user created the account. If pepper array does not contain 6 values, this will fail.
    date = datetime.utcnow()
    pepper = PEPPER_ARRAY[(date.month -1) % len(PEPPER_ARRAY)] 

    salt = generate_salt()
    salted_password = salt + password + pepper

    #create user
    try:
        hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')
        new_user = User(name=name, email=email, password=hashed_password, salt=salt, )
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({'response': 'There was an error registering user', 'error': str(e)}), 500

    access_token = create_access_token(identity=email, expires_delta=timedelta(days=7))
    
    response_data ={
            'response':'success', 
            'access_token':access_token,
            'user': {'name': new_user.name, 'email': new_user.email},
        }
    return jsonify(response_data)
