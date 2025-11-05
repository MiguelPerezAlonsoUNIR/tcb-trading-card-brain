"""
One Piece TCG Deck Builder Web Application
Refactored with modular architecture for better maintainability
"""
from flask import Flask, render_template
from flask_cors import CORS
from flask_login import LoginManager
import os
import logging

from src.models import db, User
from src.config import get_config
from src.api.routes import register_blueprints

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config_class=None):
    """
    Application factory pattern
    Creates and configures the Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, supports_credentials=True)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'index'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user for Flask-Login"""
        return User.query.get(int(user_id))
    
    # Register blueprints for API routes
    register_blueprints(app)
    
    # Register view routes
    register_view_routes(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def register_view_routes(app):
    """Register routes for serving HTML pages"""
    
    @app.route('/')
    def index():
        """Serve the landing page with TCG selection"""
        return render_template('landing.html')
    
    @app.route('/onepiece')
    def onepiece():
        """Serve the One Piece TCG deck builder page"""
        return render_template('onepiece.html')


# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Only enable debug mode in development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
