from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, TourPackage, Destination, User
from ..utils.auth import role_required

package_bp = Blueprint('package_bp', __name__)

#create package
@package_bp.route('/packages', methods=['POST'])
@jwt_required()
@role_required(['admin, guide'])
def create_package():
    data = request.get_json()
    title = data.get('data')
    price =data.get('price')
    details =data.get('details')
    duration = data.get('duration')
    destination_id = data.get('destination_id')
    image_url = data.get('image_url')

    guide_id = get_jwt_identity()

    #validation
    if not all([title, price, details, destination_id]):
        return jsonify({'error': "Missing fields required!"}), 400
    
    destination = Destination.query.get(destination_id)
    if not destination:
        return jsonify({'error': "Destination not found!"})
    
    new_package = TourPackage(
        title=title,
        price=price,
        details=details,
        duration=duration,
        image_url=image_url,
        destination_id=destination_id,
        guide_id=guide_id
    )

    db.session.add(new_package)
    db.session.commit()

    return jsonify({'message': 'Package created successfully'}), 201

#admin update package
@package_bp.route('/packages/<int:id>', methods=['PUT'])
@role_required('admin') 
def update_package(id):
    pkg = TourPackage.query.get_or_404(id)
    data = request.get_json()

    pkg.title = data.get('title', pkg.title)
    pkg.price = data.get('price', pkg.price)
    pkg.details = data.get('details', pkg.details)
    pkg.duration = data.get('duration', pkg.duration)
    pkg.image_url = data.get('image_url', pkg.image_url)
    pkg.destination_id = data.get('destination_id', pkg.destination_id)
    pkg.guide_id = data.get('guide_id', pkg.guide_id)

    db.session.commit()

    return jsonify({'message': 'Package updated successfully'}), 200

#admin delete package
@package_bp.route('/packages/<int:id>', methods=['DELETE'])
@role_required('admin')  
def delete_package(id):
    pkg = TourPackage.query.get_or_404(id)
    db.session.delete(pkg)
    db.session.commit()
    return jsonify({'message': 'Package deleted successfully'}), 200

#View all packages
@package_bp.route('/packages', methods=['GET'])
def get_all_packages():
    packages = TourPackage.query.all()
    result = []
    for pkg in packages:
        result.append({
            'id': pkg.id,
            'title': pkg.title,
            'price': pkg.price,
            'details': pkg.details,
            'duration': pkg.duration,
            'image_url': pkg.image_url,
            'destination': pkg.destination.name,
            'guide': pkg.guide.full_name if pkg.guide else None
        })
    return jsonify(result), 200


#View single package
@package_bp.route('/packages/<int:id>', methods=['GET'])
def get_package(id):
    pkg = TourPackage.query.get_or_404(id)
    return jsonify({
        'id': pkg.id,
        'title': pkg.title,
        'price': pkg.price,
        'details': pkg.details,
        'duration': pkg.duration,
        'image_url': pkg.image_url,
        'destination': pkg.destination.name,
        'guide': pkg.guide.full_name if pkg.guide else None
    }), 200
