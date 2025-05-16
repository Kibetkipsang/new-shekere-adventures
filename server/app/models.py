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