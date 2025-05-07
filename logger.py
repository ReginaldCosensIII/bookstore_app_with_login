# bookstore_app_with_login/logger.py

import logging
import os

# --- Configuration ---
LOG_FOLDER = "logs"  # Define the folder name for log files
LOG_LEVEL = logging.INFO  # Set the minimum logging level (e.g., DEBUG, INFO, WARNING)
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Define the log message format
LOG_FILENAME = f"{LOG_FOLDER}/app.log"  # Define the full path for the log file

# --- Initialization ---

# Ensure the log directory exists; create it if it doesn't.
if not os.path.exists(LOG_FOLDER):
    try:
        os.makedirs(LOG_FOLDER)
    except OSError as e:
        # Handle potential errors during directory creation (e.g., permission issues)
        print(f"Error creating log directory '{LOG_FOLDER}': {e}")
        # Optionally, raise the exception or exit if logging to file is critical
        # raise

# Configure the root logger
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        # Handler for writing logs to a file
        logging.FileHandler(LOG_FILENAME),
        # Handler for printing logs to the console (standard output/error)
        logging.StreamHandler()
    ]
)

# Get a logger instance specifically for this module (best practice)
logger = logging.getLogger(__name__)

# --- Initial Log Messages ---
logger.info("Logger initialized.")
# Example debug message (will only show if LOG_LEVEL is set to DEBUG)
logger.debug("Debug mode enabled for logger.")