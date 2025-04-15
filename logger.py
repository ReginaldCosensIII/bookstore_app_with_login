# logger.py
import logging
import os

# Ensure the log folder exists
log_folder = "logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Configure the logger
logging.basicConfig(
    level=logging.INFO,  # Can be DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{log_folder}/app.log"),  # File logs
        logging.StreamHandler()                       # Console logs
    ]
)

logger = logging.getLogger(__name__)
logger.info("Logger initialized.")
logger.debug("Debugging information for logger initialization.")