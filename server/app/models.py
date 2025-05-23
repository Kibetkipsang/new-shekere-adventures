from . import db
from datetime import datetime

# Association table for many-to-many relationship between User and CommunityTrip

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    middle_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(50), default='traveler')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    guided_packages = db.relationship('TourPackage', back_populates='guide', lazy=True)
    bookings = db.relationship('Booking', back_populates='booked_by', lazy=True)
    reviews = db.relationship('Review', back_populates='reviewed_by', lazy=True)
    created_trips = db.relationship('CommunityTrip', back_populates='creator', lazy=True)
    sent_trip_messages = db.relationship('TripMessage', back_populates='user', lazy=True)

    # New relationships using TripParticipant model
    trip_participations = db.relationship('TripParticipant', back_populates='user', cascade='all, delete-orphan')
    community_trips_joined = db.relationship(
        'CommunityTrip',
        secondary='trip_participants',
        viewonly=True,
        back_populates='members'
    )


class Destination(db.Model):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    image_url = db.Column(db.String(250))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    # Relationships
    packages = db.relationship('TourPackage', back_populates='destination', lazy=True)


class TourPackage(db.Model):
    __tablename__ = 'tour_packages'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    details = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50))
    image_url = db.Column(db.String(250))

    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    guide_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relationships
    destination = db.relationship('Destination', back_populates='packages')
    guide = db.relationship('User', back_populates='guided_packages')
    bookings = db.relationship('Booking', back_populates='package', lazy=True)
    reviews = db.relationship('Review', back_populates='package', lazy=True)


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('tour_packages.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    travelers = db.Column(db.Integer, default=1)
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, cancelled

    # Relationships
    booked_by = db.relationship('User', back_populates='bookings')
    package = db.relationship('TourPackage', back_populates='bookings')


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # e.g., 1 to 5
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('tour_packages.id'), nullable=False)

    # Relationships
    reviewed_by = db.relationship('User', back_populates='reviews')
    package = db.relationship('TourPackage', back_populates='reviews')


class CommunityTrip(db.Model):
    __tablename__ = 'community_trip'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=True)
    max_participants = db.Column(db.Integer)
    image_url = db.Column(db.String(250))
    status = db.Column(db.String(50), default='upcoming')

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    creator = db.relationship('User', back_populates='created_trips')
    messages = db.relationship('TripMessage', back_populates='trip', lazy=True)

    # New relationships using TripParticipant model
    participant_links = db.relationship('TripParticipant', back_populates='trip', cascade='all, delete-orphan')
    members = db.relationship(
        'User',
        secondary='trip_participants',
        viewonly=True,
        back_populates='community_trips_joined'
    )

class TripMessage(db.Model):
    __tablename__ = 'trip_messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('community_trip.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='sent_trip_messages')
    trip = db.relationship('CommunityTrip', back_populates='messages')

class TripParticipant(db.Model):
    __tablename__ = 'trip_participants'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('community_trip.id'), primary_key=True)
    role = db.Column(db.String(50), default='member')  # member/admin/creator

    user = db.relationship('User', back_populates='trip_participations')
    trip = db.relationship('CommunityTrip', back_populates='participant_links')
