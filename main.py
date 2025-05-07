# bookstore_app_with_login/main.py

from app import create_app
from logger import logger  # Import the custom logger

# Create the Flask application instance by calling the factory function
app = create_app()

# Check if the script is executed directly (not imported)
if __name__ == '__main__':
    # Log the start of the Flask application (useful for debugging)
    logger.info("Starting the Flask application in development mode...")
    
    # Run the Flask development server
    # debug=True enables auto-reloading and the Werkzeug debugger.
    # IMPORTANT: Set debug=False for production environments.
    app.run(debug=True)
    
    # Log when the application stops (might not always execute if terminated abruptly)
    logger.info("Flask application has stopped.")