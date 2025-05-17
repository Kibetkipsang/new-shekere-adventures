from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), default='traveler')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Destination(db.Model):  
    __tablename__ = 'destinations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    image_url = db.Column(db.String(250))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

class TourPackage(db.Model):
    __tablename__ = 'tourpackages'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    details = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50))
    image_url = db.Column(db.String(250))

    destintion_id = db.Column(db.Integer, db.ForeignKey('destination_id'), nullable = False)
    guide_id = db.Column(db.Integer, db.ForeignKey('user_id'))
    destination = db.relationship('Destination', backref='packages')
    guide = db.relationship('User', backref='guided_packages')