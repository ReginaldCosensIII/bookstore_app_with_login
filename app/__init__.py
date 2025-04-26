#app/__init__.py
import os
from flask import Flask
from logger import logger
from .routes import bp as main_bp
from .services import auth_service
from app.models.customer import Customer
from .extensions import db, login_manager
from .services.auth_service import login_manager

def create_app():
    """
    Create and configure the Flask application.
    """
    # Initialize the Flask application
    logger.info("Initializing Flask application...")

    # Set up the Flask application with a template folder and secret key
    app = Flask(__name__, template_folder="templates")
    app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_for_local')
    
    logger.debug("Setting up configuration and extensions...")

    # Load configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    logger.debug("SQLAlchemy and LoginManager initialized.")
    
    # Initialize login manager
    login_manager.init_app(app)  # ✅ this line is crucial
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Register the main blueprint
    app.register_blueprint(main_bp)
    logger.debug("Blueprint 'main_bp' registered.")

    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        logger.debug("Database tables created.")

    logger.info("Flask application initialized successfully.")
    return app
