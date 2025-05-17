from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Destination, User
from ..utils.auth import role_required

destination_bp = Blueprint('destination_bp', __name__)

#admin can create destinations
@destination_bp.route('/destinations', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_destinations():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    location = data.get('location')
    image_url = data.get('image_url')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not all([name, description, location]):
        return jsonify({'error' : "Name, Description and Location are required!"}), 400
    
    destination = Destination(
        name=name,
        description=description,
        location=location,
        image_url=image_url,
        latitude=latitude,
        longitude=longitude
    )

    db.session.add(destination)
    db.session.commit()

    return jsonify({'message': 'Destination added successfully'}), 201


#anyone can view the destinations
@destination_bp.route('/destinations', methods=['GET'])
def get_destinations():
    destinations = Destination.query.all()
    result = []
    for dest in destinations:
        result.append({
            'id': dest.id,
            'name': dest.name,
            'description': dest.description,
            'location': dest.location,
            'image_url': dest.image_url,
            'coordinates': {'lat': dest.latitude, 'lng': dest.longitude}
        })
    return jsonify(result), 200