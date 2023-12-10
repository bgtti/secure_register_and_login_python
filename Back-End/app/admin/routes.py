from flask import Blueprint, request, jsonify
from app.extensions import flask_bcrypt, db
from app.account.schemas import sign_up_schema, log_in_schema
# from app.account.salt import generate_salt
from app.models.user import User
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper


admin = Blueprint('admin', __name__)

# In this file: routes concerning admin 

# SIGN In
@admin.route("/restricted_login", methods=["POST"])
def admin_login():
    
    return jsonify({'response': 'You logged in!'})

# DASHBOARD
@admin.route("/restricted_dashboard", methods=["POST"])
def admin_dashboard():

    # users = User.query.order_by(_email=email).first()
    
    return jsonify({'response': 'You logged in!'})
