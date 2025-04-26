# app/models/db.py
import os
import psycopg2
from logger import logger
from psycopg2.extras import DictCursor

def get_db_connection():
    """
    Establish and return a connection to the PostgreSQL database
    using the DATABASE_URL environment variable.
    """
    try:
        # Check if the DATABASE_URL environment variable is set
        database_url = os.getenv("DATABASE_URL")
        
        if not database_url:
            raise ValueError("DATABASE_URL is not set")

        conn = psycopg2.connect(database_url, cursor_factory=DictCursor)
        logger.debug("Database connection established successfully.")
        
        return conn
    
    except Exception as e:
        logger.exception("Failed to establish a database connection.")
        raise
    
    finally:
        logger.debug("Database connection attempt finished.")
