from flask import Blueprint

welcome_bp = Blueprint('welcome', __name__)

@welcome_bp.route('/')
def home():
    return "Welcome to Shekere Adventures!"
