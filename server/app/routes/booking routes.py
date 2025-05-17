from flask import Blueprint, request, jsonify
from app.models import Booking, TourPackage, User
from app import db
from app.utils.auth import role_required, current_user

booking_bp = Blueprint('booking_bp', __name__)

@booking_bp.route('/booking', methods=['POST'])
@role_required(['user'])
def create_booking():
    data = request.get_json()
    package_id = data.get('package_id')
    date = data.get('date') 
    user = current_user()
#check if package exists
    pkg = TourPackage.query.get_or_404(package_id)

    new_booking = Booking(user_id=user.id, package_id=package_id, date=date)
    db.session.add(new_booking)
    db.session.commit()

    return jsonify({'message': 'Booking created successfully', 'booking_id': new_booking.id}), 201

#view booking
@booking_bp.route('/bookings', methods=['GET'])
@role_required('user')
def get_user_bookings():
    user = current_user()
    bookings = Booking.query.filter_by(user_id=user.id).all()
    bookings_list = []
    for b in bookings:
        bookings_list.append({
            'id': b.id,
            'package': {
                'id': b.package.id,
                'title': b.package.title,
                'price': b.package.price
            },
            'date': b.date.isoformat()
        })
    return jsonify(bookings_list), 200

#delete bookings
@booking_bp.route('/bookings/<int:id>', methods=['DELETE'])
@role_required('user')
def cancel_booking(id):
    user = current_user()
    booking = Booking.query.get_or_404(id)
    if booking.user_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking cancelled'}), 200
