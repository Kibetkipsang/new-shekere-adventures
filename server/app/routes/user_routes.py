from flask import Blueprint, jsonify
from app.models import User
from app import db
from app.schemas import users_schema

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200
