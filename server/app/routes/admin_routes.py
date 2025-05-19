from flask import Blueprint, jsonify, request
from app.models import User, CommunityTrip
from app import db
from app.schemas import users_schema, user_schema, trips_schema
from app.utils.auth import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# GET all users
@admin_bp.route('/users', methods=['GET'])
@role_required('admin')
def get_all_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200

# PATCH user role
@admin_bp.route('/users/<int:user_id>/role', methods=['PATCH'])
def update_user_role(user_id):
    data = request.get_json()
    role = data.get("role")

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.role = role
    db.session.commit()
    return jsonify({"message": f"Updated role to '{role}' for user {user.username}"}), 200

# GET all trips
@admin_bp.route('/trips', methods=['GET'])
def get_all_trips():
    trips = CommunityTrip.query.all()
    return jsonify(trips_schema.dump(trips)), 200

# DELETE a user
@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

# DELETE a trip
@admin_bp.route('/trips/<int:trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    trip = CommunityTrip.query.get(trip_id)
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404

    db.session.delete(trip)
    db.session.commit()
    return jsonify({'message': 'Trip deleted successfully'}), 200
