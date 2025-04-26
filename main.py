from app import create_app
from logger import logger  # Custom logger

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # This will only run in development, Gunicorn will handle in production
    logger.info("Starting the Flask application...")
    app.run(debug=True)  # Set debug=True only for local testing
    logger.info("Flask application has stopped.")
