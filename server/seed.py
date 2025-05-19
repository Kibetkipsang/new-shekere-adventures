# seed.py
from app import create_app, db
from app.models import User, CommunityTrip
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()
app.app_context().push()

# Clear existing data
db.drop_all()
db.create_all()

admin_user = User(full_name='admin', email='admin@shekere.com',password=generate_password_hash('Admin123!'), role='admin') 
db.session.add(admin_user)
db.session.commit()

# Sample users 
dennis = User(
    full_name="dennis kibet",
    email="kibet@example.com",
    phone="0712345678",
    password=generate_password_hash("password123"),
    role="traveler",
    created_at=datetime.utcnow()
)

wema = User(
    full_name="wema sepetu",
    email="wema@example.com",
    phone="0711122233",
    password=generate_password_hash("password456"),
    role="traveler",
    created_at=datetime.utcnow()
)

db.session.add_all([dennis, wema])
db.session.commit()

# Sample community trip
trip1 = CommunityTrip(
    title="Lake Naivasha Adventure",
    description="Join us for a boat ride and wildlife spotting!",
    location="Naivasha, Kenya",
    date="2025-06-10",
    time="10:00",
    creator_id=dennis.id
)

# Add participants
trip1.participants.append(wema)

db.session.add(trip1)
db.session.commit()

print("✅ Seed data inserted!")
