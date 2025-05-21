from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import logging
import os

logging.basicConfig(level=logging.DEBUG)

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

    CORS(app, origins=["http://127.0.0.1:5173", "http://localhost:5173"], supports_credentials=True)

    # JWT error handlers must be added AFTER jwt.init_app(app)
    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        print("Invalid token error:", reason)
        return jsonify({"error": "Invalid token", "message": reason}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        print("Missing token error:", reason)
        return jsonify({"error": "Missing token", "message": reason}), 401

    # Register blueprints
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
