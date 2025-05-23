from flask import Blueprint, jsonify
from app import db
from app.models import User, Booking, TourPackage, CommunityTrip, TripMessage
from app.schemas import users_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user_bp', __name__)


#  Return all users (admin/testing utility)
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200


#  Return trips booked by the authenticated user
@user_bp.route("/plans/my-plans", methods=["GET"])
@jwt_required()
def get_user_plans():
    current_user_id = get_jwt_identity()
    bookings = Booking.query.filter_by(user_id=current_user_id).all()

    trips = []
    for booking in bookings:
        package = TourPackage.query.get(booking.package_id)
        trips.append({
            "title": package.title,
            "date": booking.booking_date.isoformat()
        })

    return jsonify(trips), 200


#  Return groups the authenticated user has joined
@user_bp.route("/groups/my-groups", methods=["GET"])
@jwt_required()
def get_user_groups():
    current_user_id = get_jwt_identity()  
    user = User.query.get(current_user_id)

    groups = [
        {
            "id": group.id,
            "name": group.title,
            "date": group.date.isoformat()
        }
        for group in user.community_trips_joined
    ]

    return jsonify(groups), 200


#  Return the most recent message from each group the user has joined
@user_bp.route("/groups/recent-messages", methods=["GET"])
@jwt_required()
def get_recent_messages():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    groups = user.community_trips_joined

    recent_messages = []

    for group in groups:
        latest = (
            TripMessage.query
            .filter_by(trip_id=group.id)
            .order_by(TripMessage.timestamp.desc())
            .first()
        )
        if latest:
            recent_messages.append({
                "groupName": group.title,
                "content": latest.content,
                "timestamp": latest.timestamp.isoformat()
            })

    return jsonify(recent_messages), 200
