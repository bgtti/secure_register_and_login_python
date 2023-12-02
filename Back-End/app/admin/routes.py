from flask import Blueprint, request, jsonify


admin = Blueprint('admin', __name__)

# In this file: routes concerning admin 

# SIGN UP
@admin.route("/restricted_login", methods=["POST"])
def admin_login():
    
    return jsonify({'response': 'You logged in!'})
