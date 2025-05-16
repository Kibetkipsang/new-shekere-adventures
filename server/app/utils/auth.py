# app/utils/auth.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from ..models import User

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            from flask_jwt_extended import verify_jwt_in_request
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or user.role != required_role:
                return jsonify({'error': 'Access forbidden: insufficient role'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

