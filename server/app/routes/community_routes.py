from flask import Blueprint, request, jsonify
from app.models import db, CommunityTrip, TripParticipant, User, TripRole, Plan
from app.schemas import CommunityTripSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, time
from flask_cors import cross_origin

community_trip_bp = Blueprint('community_trip_bp', __name__)
trip_schema = CommunityTripSchema()
trips_schema = CommunityTripSchema(many=True)

def get_user_role(trip_id, user_id):
    participant = TripParticipant.query.filter_by(trip_id=trip_id, user_id=user_id).first()
    return participant.role.value if participant else None

# Create a new trip and auto-register creator in TripParticipant table
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
    db.session.flush()  # needed to get new_trip.id before commit

    creator_link = TripParticipant(user_id=user_id, trip_id=new_trip.id, role='creator')
    db.session.add(creator_link)
    db.session.commit()

    return trip_schema.jsonify(new_trip), 201

# List all trips
@community_trip_bp.route('/community-trips', methods=['GET'])
def list_trips():
    trips = CommunityTrip.query.all()
    return trips_schema.jsonify(trips)

# Join a trip
@community_trip_bp.route('/community-trips/<int:id>/join', methods=['POST'])
@jwt_required()
def join_trip(id):
    trip = CommunityTrip.query.get_or_404(id)
    user = User.query.get(get_jwt_identity())

    existing = TripParticipant.query.filter_by(user_id=user.id, trip_id=trip.id).first()
    if existing:
        return jsonify({"message": "Already joined"}), 400

    participant = TripParticipant(user_id=user.id, trip_id=trip.id, role='member')
    db.session.add(participant)
    db.session.commit()
    return jsonify({"message": "Joined trip"}), 200

# View a single trip
@community_trip_bp.route('/community-trips/<int:id>', methods=['GET'])
@jwt_required(optional=True)
def get_trip(id):
    trip = CommunityTrip.query.get_or_404(id)

    # Get all participant records (with role)
    participants = TripParticipant.query.filter_by(trip_id=id).all()
    members = [{
        "id": p.user.id,
        "name": f"{p.user.first_name} {p.user.last_name}",
        "role": p.role
    } for p in participants]

    return jsonify({
        "id": trip.id,
        "title": trip.title,
        "description": trip.description,
        "location": trip.location,
        "date": trip.date.isoformat(),
        "time": str(trip.time) if trip.time else None,
        "image_url": trip.image_url,
        "creator_id": trip.creator_id,
        "creator": f"{trip.creator.first_name} {trip.creator.last_name}",
        "members": members,
        "plans": [
            {
                "id": p.id,
                "title": p.title,
                "time": p.time,
                "location": p.location
            } for p in trip.plans
        ],
        "chat": []
    })

# Leave a trip
@community_trip_bp.route('/community-trips/<int:id>/leave', methods=['POST'])
@jwt_required()
def leave_trip(id):
    trip = CommunityTrip.query.get_or_404(id)
    user = User.query.get(get_jwt_identity())

    link = TripParticipant.query.filter_by(user_id=user.id, trip_id=trip.id).first()
    if not link:
        return jsonify({"message": "You are not part of this trip"}), 400

    db.session.delete(link)
    db.session.commit()
    return jsonify({"message": "Left trip"}), 200

# Delete a trip (creator only)
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

# Get trips created by the logged in user
@community_trip_bp.route('/my-community-trips', methods=['GET'])
@jwt_required()
def get_my_trips():
    user_id = get_jwt_identity()
    trips = CommunityTrip.query.filter_by(creator_id=user_id).all()
    return trips_schema.jsonify(trips)

# Get trips user has joined
@community_trip_bp.route('/joined-community-trips', methods=['GET'])
@jwt_required()
def get_joined_trips():
    user_id = get_jwt_identity()

    # Trips where the user is a participant
    participant_trip_ids = [
        link.trip_id for link in TripParticipant.query.filter_by(user_id=user_id).all()
    ]

    # Trips where the user is the creator
    created_trip_ids = [
        trip.id for trip in CommunityTrip.query.filter_by(creator_id=user_id).all()
    ]

    # Merge both (avoiding duplicates)
    all_trip_ids = list(set(participant_trip_ids + created_trip_ids))

    # Fetch full trip details
    trips = CommunityTrip.query.filter(CommunityTrip.id.in_(all_trip_ids)).all()

    result = []
    for trip in trips:
        result.append({
            "id": trip.id,
            "title": trip.title,
            "location": trip.location,
            "date": trip.date.isoformat(),
            "time": str(trip.time) if trip.time else None,
        })

    return jsonify(result), 200



@community_trip_bp.route('/community-trips/<int:trip_id>/participants/<int:user_id>/role', methods=['PATCH'])
@jwt_required()
def update_participant_role(trip_id, user_id):
    current_user_id = get_jwt_identity()

    trip = CommunityTrip.query.get_or_404(trip_id)
    requester_link = TripParticipant.query.filter_by(trip_id=trip_id, user_id=current_user_id).first()
    target_link = TripParticipant.query.filter_by(trip_id=trip_id, user_id=user_id).first()

    # Permission checks
    if not requester_link or requester_link.role not in [TripRole.CREATOR, TripRole.ADMIN]:
        return jsonify({"error": "Unauthorized"}), 403

    if not target_link:
        return jsonify({"error": "User is not part of this trip"}), 404

    if requester_link.role == TripRole.ADMIN and target_link.role == TripRole.CREATOR:
        return jsonify({"error": "Admins cannot change the creator's role"}), 403

    data = request.get_json()
    new_role = data.get("role")

    # Validate role
    if new_role not in TripRole._value2member_map_:
        return jsonify({"error": f"Invalid role. Must be one of: {list(TripRole._value2member_map_.keys())}"}), 400

    target_link.role = TripRole(new_role)
    db.session.commit()

    return jsonify({
        "message": "Role updated successfully",
        "user_id": user_id,
        "new_role": new_role
    }), 200

@community_trip_bp.route('/community-trips/<int:trip_id>/plans', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required()
def create_plan(trip_id):
    # Verify trip exists
    trip = CommunityTrip.query.get_or_404(trip_id)

    user_id = get_jwt_identity()
    link = TripParticipant.query.filter_by(user_id=user_id, trip_id=trip_id).first()
    if not link or link.role not in [TripRole.CREATOR, TripRole.ADMIN]:
        return jsonify({"error": "Not authorized to add plans"}), 403

    data = request.get_json()
    print("Incoming plan data:", data)

    title = data.get('title')
    raw_time = data.get('time')
    location = data.get('location')

    if not title or not raw_time or not location:
        return jsonify({"error": "All fields (title, time, location) are required."}), 400

    plan = Plan(
        title=title,
        time=raw_time,
        location=location,
        trip_id=trip_id
    )

    db.session.add(plan)
    db.session.commit()

    return jsonify({
        "id": plan.id,
        "title": plan.title,
        "time": plan.time,
        "location": plan.location
    }), 201

@community_trip_bp.route("/community-trips/<int:trip_id>/plans/<int:plan_id>", methods=["PATCH"])
@jwt_required()
def update_plan(trip_id, plan_id):
    user_id = get_jwt_identity()

    # Ensure user is part of the trip
    participant = TripParticipant.query.filter_by(user_id=user_id, trip_id=trip_id).first()
    if not participant or participant.role.value not in ["creator", "admin"]:
        return jsonify({"error": "Unauthorized"}), 403

    plan = Plan.query.get(plan_id)
    if not plan:
        return jsonify({"error": "Plan not found"}), 404

    data = request.get_json()
    plan.title = data.get("title", plan.title)
    plan.time = data.get("time", plan.time)
    plan.location = data.get("location", plan.location)

    db.session.commit()
    return jsonify({"message": "Plan updated successfully"}), 200

@community_trip_bp.route("/community-trips/<int:trip_id>/plans/<int:plan_id>", methods=["DELETE"])
@jwt_required()
def delete_plan(trip_id, plan_id):
    user_id = get_jwt_identity()
    user_role = get_user_role(trip_id, user_id)


    if user_role not in ["creator", "admin"]:
        return jsonify({"error": "Only creator or admin can delete plans"}), 403

    plan = Plan.query.get_or_404(plan_id)
    db.session.delete(plan)
    db.session.commit()

    return jsonify({"message": "Plan deleted"}), 200
