from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, CommunityTrip, Poll, PollOption, Vote, TripParticipant

poll_bp = Blueprint("polls", __name__)

# lets first check the participants role
def get_user_role(trip_id, user_id):
    participant = TripParticipant.query.filter_by(trip_id=trip_id, user_id=user_id).first()
    return participant.role.value if participant else None

# create poll
@poll_bp.route("/community-trips/<int:trip_id>/polls", methods=["POST"])
@jwt_required()
def create_poll(trip_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    role = str(get_user_role(trip_id, user_id)).strip().lower()
    print("User ID:", user_id)
    print("Role for trip:", role)
    if role not in ["creator", "admin"]:
        return jsonify({"error" : "Only admin and creator can create polls"}), 403
    
    question = data.get("question")
    options = data.get("options", [])

    if not question or len(options) < 2:
        return jsonify({"error": "Poll must include a question and at least two options."}), 400
    
    poll = Poll(community_trip_id=trip_id, question=question, created_by=user_id)
    db.session.add(poll)
    db.session.flush()

    for opt in options:
        db.session.add(PollOption(poll_id=poll.id, name=opt))

    db.session.commit()
    return jsonify({"message": "Poll created successfully"}), 201

# delete poll
@poll_bp.route("/polls/<int:poll_id>", methods=["DELETE"])
@jwt_required()
def delete_poll(poll_id):
    user_id = get_jwt_identity()
    poll = Poll.query.get_or_404(poll_id)

    role = get_user_role(poll.community_trip_id, user_id)
    if role != "creator":
        return jsonify({"error": "Only the creator can delete polls"}), 403

    db.session.delete(poll)
    db.session.commit()
    return jsonify({"message": "Poll deleted"}), 200

# vote on a poll
@poll_bp.route("/polls/<int:poll_id>/vote", methods=["POST"])
@jwt_required()
def vote(poll_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    option_id = data.get("option_id")

# ensure that the option belongs to the poll
    option = PollOption.query.filter_by(id=option_id, poll_id=poll_id).first()
    if not option:
        return jsonify({"error" : "Invalid poll option!"}), 400
    
    existing_vote = Vote.query.filter_by(user_id=user_id, poll_id=poll_id).first()
    if existing_vote:
        return jsonify({"error" : "You have already voted on this poll!"}), 400
    
    vote = Vote(user_id=user_id, poll_id=poll_id, poll_option_id=option_id)
    db.session.add(vote)
    db.session.commit()
    return jsonify({"success" : "Vote submitted!"}), 200

# Get all polls for a trip
@poll_bp.route("/community-trips/<int:trip_id>/polls", methods=["GET"])
@jwt_required()
def get_polls(trip_id):
    user_id = get_jwt_identity()
    polls = Poll.query.filter_by(community_trip_id=trip_id).all()
    response = []

    for poll in polls:
        has_voted = Vote.query.filter_by(user_id=user_id, poll_id=poll.id).first() is not None
        poll_data = {
            "id": poll.id,
            "question": poll.question,
            "has_voted": has_voted,
            "options": []
        }

        for opt in poll.options:
            vote_count = Vote.query.filter_by(poll_option_id=opt.id).count()
            poll_data["options"].append({
                "id": opt.id,
                "name": opt.name,
                "votes": vote_count
            })

        response.append(poll_data)

    return jsonify(response), 200

@poll_bp.route("/polls/<int:poll_id>", methods=["PATCH"])
@jwt_required()
def edit_poll(poll_id):
    user_id = get_jwt_identity()
    poll = Poll.query.get_or_404(poll_id)

    role = get_user_role(poll.community_trip_id, user_id)
    if role != "creator":
        return jsonify({"error": "Only the creator can edit polls"}), 403

    data = request.get_json()
    new_question = data.get("question")
    new_options = data.get("options", [])

    if new_question:
        poll.question = new_question

    if not new_options or not isinstance(new_options, list) or len(new_options) < 2:
        return jsonify({"error": "Poll must have at least 2 options."}), 400

    # Build a map of current options: name -> PollOption
    existing_options = {opt.name: opt for opt in poll.options}
    incoming_set = set(new_options)
    existing_set = set(existing_options.keys())

    # Delete removed options and their votes
    to_delete = existing_set - incoming_set
    for name in to_delete:
        opt = existing_options[name]
        Vote.query.filter_by(poll_option_id=opt.id).delete()
        db.session.delete(opt)

    # Add new options
    to_add = incoming_set - existing_set
    for name in to_add:
        db.session.add(PollOption(poll_id=poll.id, name=name))

    # No action needed for options that are unchanged

    db.session.commit()
    return jsonify({"message": "Poll updated successfully"}), 200
