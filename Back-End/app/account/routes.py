from flask import Blueprint, request, jsonify
from app.account.salt import generate_salt

account = Blueprint('account', __name__)

# SIGN UP
@account.route("/signup", methods=["POST"])
def signup_user():
    return jsonify("hello")

