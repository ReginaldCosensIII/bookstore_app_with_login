from app import create_app
from logger import logger  # Import your custom logger

app = create_app()

if __name__ == '__main__':
    # Run the Flask application
    # with debug mode enabled for development.
    logger.info("Starting the Flask application...")
    app.run(debug=True)
    logger.info("Flask application has stopped.")
    # Note: In production, you would typically use a WSGI server like Gunicorn or uWSGI.
    # The debug=True option is not recommended for production use.