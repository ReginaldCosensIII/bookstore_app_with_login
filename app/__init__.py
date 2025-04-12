from flask import Flask
from .routes import bp as main_bp
from flask_login import LoginManager
from .services import auth_service  # ✅ <-- import it so user_loader is registered
import os

# Use the existing login_manager
login_manager = auth_service.login_manager
login_manager.login_view = 'main.login'

def create_app():    
    # Create a Flask application instance.
    # Register the main blueprint with the application.
    app = Flask(__name__, template_folder="templates")
    app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_for_local')  # Replace with env var in production
    login_manager.init_app(app)
    app.register_blueprint(main_bp)
    return app
