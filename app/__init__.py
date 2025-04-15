from flask import Flask
from .routes import bp as main_bp
from flask_login import LoginManager
from .services import auth_service  # ✅ <-- import it so user_loader is registered
import os
from logger import logger  # ✅ <-- import your custom logger

# Use the existing login_manager
login_manager = auth_service.login_manager
login_manager.login_view = 'main.login'

def create_app():
    logger.info("Initializing Flask application...")

    app = Flask(__name__, template_folder="templates")
    app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_for_local')
    logger.debug("Flask app created. Registering login manager and blueprints...")

    login_manager.init_app(app)
    logger.debug("Login manager initialized.")

    app.register_blueprint(main_bp)
    logger.debug("Blueprint 'main_bp' registered.")

    logger.info("Flask application initialized successfully.")
    return app
