# bookstore_app_with_login/app/models/db.py

import os
import psycopg2 # PostgreSQL adapter for Python
from psycopg2.extras import DictCursor # Allows accessing columns by name (like dictionaries)
from logger import logger # Import the custom logger

def get_db_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.

    Reads the connection string from the DATABASE_URL environment variable.
    Uses DictCursor to return rows as dictionary-like objects.

    Raises:
        ValueError: If the DATABASE_URL environment variable is not set.
        psycopg2.Error: If any database connection error occurs.

    Returns:
        psycopg2.connection: A database connection object, or raises an error.
    """
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        logger.error("DATABASE_URL environment variable is not set.")
        raise ValueError("Database connection configuration is missing (DATABASE_URL not set).")

    try:
        # Establish the connection using the URL and specify DictCursor
        conn = psycopg2.connect(dsn=database_url, cursor_factory=DictCursor)
        logger.debug("Database connection established successfully.")
        return conn

    except psycopg2.OperationalError as e:
        # Handle specific connection errors (e.g., bad hostname, database doesn't exist)
        logger.exception(f"Failed to establish database connection: {e}")
        # Re-raise the specific psycopg2 error for potentially more specific handling upstream
        raise
    except Exception as e:
        # Catch any other unexpected exceptions during connection
        logger.exception("An unexpected error occurred while connecting to the database.")
        raise # Re-raise the generic exception

# Note: It's the responsibility of the calling function to close the connection
# when done, typically using a 'with' statement or explicit 'conn.close()'.
# The 'with get_db_connection() as conn:' pattern handles this automatically.