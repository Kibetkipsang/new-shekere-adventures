from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..utils.auth import role_required
from ..models import db, User
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError

auth_bp = Blueprint('auth_bp', __name__)

def hash_password(password):
    return generate_password_hash(password)

# Register a new user
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    first_name = data.get('firstName', '').strip()
    middle_name = data.get('middleName', '').strip()
    last_name = data.get('lastName', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    role = data.get('role', 'traveler').strip()

    # Basic validation
    if not first_name or not last_name or not email or not password:
        return jsonify({"error": "First name, last name, email, and password are required."}), 400

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered."}), 409

    new_user = User(
        first_name=first_name,
        middle_name=middle_name if middle_name else None,
        last_name=last_name,
        email=email,
        password=hash_password(password),
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)
    return jsonify({
        "msg": "User created successfully",
        "access_token": access_token
    }), 201

# Login user
@auth_bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 415

    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"token": access_token, "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Admin dashboard route (requires admin role)
@auth_bp.route('/admin/dashboard')
@role_required('admin')
def admin_dashboard():
    return jsonify({'message': 'Welcome, Admin!'})

# Get current user profile
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    print("Profile route hit!")
    try:
        user_id = get_jwt_identity()
        print("JWT Identity:", user_id)
    except Exception as e:
        print("JWT error:", e)
        return jsonify({"error": "Invalid or missing JWT"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    full_name = user.first_name
    if user.middle_name:
        full_name += f" {user.middle_name}"
    full_name += f" {user.last_name}"

    return jsonify({
        'id': user.id,
        'name': full_name,
        'email': user.email,
        'role': user.role
    }), 200
