from flask import Blueprint, request, jsonify
from app.models import db, CommunityTrip, trip_participants, User
from app.schemas import CommunityTripSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

community_trip_bp = Blueprint('community_trip_bp', __name__)
trip_schema = CommunityTripSchema()
trips_schema = CommunityTripSchema(many=True)

@community_trip_bp.route('/community-trips', methods=['POST'])
@jwt_required()
def create_trip():
    data = request.get_json()
    user_id = get_jwt_identity()

    new_trip = CommunityTrip(
        title=data['title'],
        description=data['description'],
        location=data['location'],
        date=data['date'],
        time=data.get('time'),
        creator_id=user_id
    )
    db.session.add(new_trip)
    db.session.commit()
    return trip_schema.jsonify(new_trip), 201

@community_trip_bp.route('/community-trips', methods=['GET'])
def list_trips():
    trips = CommunityTrip.query.all()
    return trips_schema.jsonify(trips)

@community_trip_bp.route('/community-trips/<int:id>/join', methods=['POST'])
@jwt_required()
def join_trip(id):
    trip = CommunityTrip.query.get_or_404(id)
    user = User.query.get(get_jwt_identity())
    if user in trip.participants:
        return jsonify({"message": "Already joined"}), 400
    trip.participants.append(user)
    db.session.commit()
    return jsonify({"message": "Joined trip"}), 200
#view single trip
@community_trip_bp.route('/community-trips/<int:id>', methods=['GET'])
def get_trip(id):
    trip = CommunityTrip.query.get_or_404(id)
    return trip_schema.jsonify(trip)

#leave atrip
@community_trip_bp.route('/community-trips/<int:id>/leave', methods=['POST'])
@jwt_required()
def leave_trip(id):
    trip = CommunityTrip.query.get_or_404(id)
    user = User.query.get(get_jwt_identity())
    if user not in trip.participants:
        return jsonify({"message": "You are not part of this trip"}), 400
    trip.participants.remove(user)
    db.session.commit()
    return jsonify({"message": "Left trip"}), 200

#Trip creator delete trip
@community_trip_bp.route('/community-trips/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_trip(id):
    trip = CommunityTrip.query.get_or_404(id)
    user_id = get_jwt_identity()
    if trip.creator_id != user_id:
        return jsonify({"message": "Unauthorized"}), 403
    db.session.delete(trip)
    db.session.commit()
    return jsonify({"message": "Trip deleted"}), 200

#get trips created by logged in users
@community_trip_bp.route('/my-community-trips', methods=['GET'])
@jwt_required()
def get_my_trips():
    user_id = get_jwt_identity()
    trips = CommunityTrip.query.filter_by(creator_id=user_id).all()
    return trips_schema.jsonify(trips)

#get trips user has joined
@community_trip_bp.route('/joined-community-trips', methods=['GET'])
@jwt_required()
def get_joined_trips():
    user = User.query.get(get_jwt_identity())
    return trips_schema.jsonify(user.community_trips_joined)


