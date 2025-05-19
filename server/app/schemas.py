from app import ma
from .models import User, CommunityTrip

class UserBasicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    id = ma.auto_field()
    full_name = ma.auto_field()

user_schema = UserBasicSchema()
users_schema = UserBasicSchema(many=True)

class CommunityTripSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CommunityTrip
        load_instance = True

    id = ma.auto_field()
    title = ma.auto_field()
    description = ma.auto_field()
    location = ma.auto_field()
    date = ma.auto_field()
    time = ma.auto_field()
    creator_id = ma.auto_field()
    participants = ma.Nested(UserBasicSchema, many=True)

trip_schema = CommunityTripSchema()
trips_schema = CommunityTripSchema(many=True)
