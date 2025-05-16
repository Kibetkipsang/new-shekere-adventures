from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..utils.auth import role_required
from ..models import db, User

auth_bp = Blueprint('auth_bp', __name__)

#register a new user
@auth_bp.route('/register', methods = ['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error' : 'Name, Email and password are requires!'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error' : 'Email has already been registered!'}), 409
    
    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'User created successfully!'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and Password required!'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error' : 'Invalid Credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token' : access_token, 'user' : {'id' : user.id, 'name' : user.name, 'role': user.role}}), 200

@auth_bp.route('/admin/dashboard')
@role_required('admin')
def admin_dashboard():
    return jsonify({'message': 'Welcome, Admin!'})

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({'id': user.id, 'name' : user.name, 'email' : user.email}), 200