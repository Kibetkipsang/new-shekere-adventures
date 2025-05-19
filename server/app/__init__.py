from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
import os

socketio = SocketIO(cors_allowed_origins="*")


db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
bcrypt = Bcrypt()
ma = Marshmallow()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    CORS(app, supports_credentials=True)
    
    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from .routes.destination_routes import destination_bp
    app.register_blueprint(destination_bp)
    from .routes.package_routes import package_bp
    app.register_blueprint(package_bp)
    from .routes.community_routes import community_trip_bp
    app.register_blueprint(community_trip_bp)
    from .routes.welcome_routes import welcome_bp
    app.register_blueprint(welcome_bp)
    from .routes.user_routes import user_bp
    app.register_blueprint(user_bp)
    from .routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp)



    socketio.init_app(app)
    return app

