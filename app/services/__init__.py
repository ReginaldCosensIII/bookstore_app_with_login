from flask import Flask
from app.services.auth_service import login_manager

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_for_local')
    
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # optional: redirect route name if user not logged in
    
    # Register blueprints here
    return app
