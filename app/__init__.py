# bookstore_app_with_login/app/__init__.py

import os
from flask import Flask
from logger import logger # Import the custom logger
from app.routes import bp as main_bp # Import the main blueprint from routes.py
from app.services.auth_service import login_manager # Ensure load_user is imported

def create_app():
    """
    Application Factory Function.

    Creates and configures an instance of the Flask application.
    This pattern helps in creating multiple instances for testing
    or different configurations.
    """
    logger.info("Initializing Flask application...")

    # Create the Flask app instance
    app = Flask(__name__, template_folder="templates") # Specifies the template folder relative to this file

    # --- Configuration ---
    # Load configuration settings. Prioritize environment variables.
    # Use a default secret key for development ONLY. Replace in production.
    app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key_for_local_testing_only')

    # Database configuration
    app.config['DATABASE_URI'] = os.getenv('DATABASE_URL')

    logger.debug("Configuration loaded.")

    # --- Initialize Extensions ---
    login_manager.init_app(app) # Initialize Flask-Login with the app
    logger.debug("LoginManager initialized.")

    # --- Configure Flask-Login ---
    login_manager.login_view = 'main.login' # The route name for the login page
    login_manager.login_message = 'Please log in to access this page.' # Message flashed to users
    login_manager.login_message_category = 'info' # Bootstrap category for the flash message

    # --- Register Blueprints ---
    app.register_blueprint(main_bp) # Register the main blueprint containing routes
    logger.debug("Blueprint 'main_bp' registered.")
    logger.info("Flask application initialization complete.")
    return app
