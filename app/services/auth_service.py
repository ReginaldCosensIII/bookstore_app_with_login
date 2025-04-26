# app/services/auth_service.py
import re
from html import escape
from flask_login import LoginManager
from app.models.customer import Customer
from app.models.db import get_db_connection
from logger import logger  # Importing customer logger here
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    """
    Load a user from the database using the user_id.
    This function is called by Flask-Login to load the user object from the session.
    """ 
    try:
        # Get a database connection
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                
                # Execute the SQL query to fetch the user by user_id
                cur.execute(
                    'SELECT customer_id, email, password FROM customers WHERE customer_id = %s',
                    (user_id,)
                )
                
                # Fetch the user row from the database
                row = cur.fetchone()

        # Verify if the row is not None (i.e., user exists)
        if row:
            logger.info(f"User {user_id} loaded from session.")
            return Customer(id=row["customer_id"], email=row["email"], password=row["password"])
        
        else:
            logger.warning(f"User {user_id} not found in database.")
            return None
        
    except Exception as e:
        logger.error(f"Error loading user {user_id}: {e}")
        return None
    
def authenticate_user(email, password):
    """
    Authenticate a user by checking the email and password against the database.
    If the user is found and the password matches, return the user object.
    """
    try:
        # Sanitize the email to prevent SQL injection and convert it to lowercase
        email = email.strip()
        email = email.lower()
        email = escape(email)
        
        # Get a database connection
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                
                # Execute the SQL query to fetch the user by email
                cur.execute('SELECT customer_id, email, password FROM customers WHERE email = %s', (email,))
                user = cur.fetchone()
        
        # Verify if the user exists and the password matches        
        if user and user["password"] and check_password_hash(user["password"], password):
            return Customer(id=user["customer_id"], email=user["email"], password=user["password"])
        
        else:
            return None
        
    except Exception as e:
        logger.exception("Error during user authentication.")
        raise e
    
def login_user(user, password):
    """
    Log in a user by checking the email and password against the database.
    If the user is found and the password matches, return True.
    Otherwise, return False.
    """
    # Check user and check if the password matches using the check_password_hash function
    if user and check_password_hash(user.password, password):
        logger.info(f"User {user.email} logged in successfully.")
        return True
    
    else:
        logger.warning(f"Login failed for user {user.email}.")
        return False
    
def get_user_by_email(email):
    """
    Fetch a user from the database using the email address.
    This function is used to check if the email already exists in the database during registration.
    """
    # Convert the email to lowercase and escape it to prevent SQL injection
    email = email.strip()
    email = email.lower()
    email = escape(email)
    
    # Get a database connection
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to fetch the user by email
            cur.execute('SELECT customer_id, email, password FROM customers WHERE email = %s', (email))
            
            # Fetch the user row from the database
            row = cur.fetchone()
            
            return row

def get_name_by_id(user_id):
    """
    Fetch the first and last name of a user from the database using the user_id.
    This function is used to display the user's name in the application.
    """ 
    # Get a database connection
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to fetch the user's first and last name by user_id
            cur.execute('SELECT first_name, last_name FROM customers WHERE customer_id = %s', (user_id,))
            
            # Fetch the user row from the database
            row = cur.fetchone()
            
            # Verify if the row is not None (i.e., user exists)
            if row:
                return f"{row[0]} {row[1]}"
            
    return None