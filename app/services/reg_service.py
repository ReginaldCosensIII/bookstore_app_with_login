# app/services/reg_services.py
import re
from html import escape
from logger import logger 
from flask_login import LoginManager
from app.models.customer import Customer
from app.models.db import get_db_connection
from werkzeug.security import generate_password_hash

def validate_registration(form_data):
    """
    Validate registration form data.
    Returns a list of error messages if validation fails.
    """
    # Initialize an empty list to store error messages
    errors = []

    # Validate each field in the form data

    # First Name and Last Name
    if not is_valid_name(form_data.get('first_name', '')):
        errors.append("Invalid first name.")
    if not is_valid_name(form_data.get('last_name', '')):
        errors.append("Invalid last name.")

    # Email
    email = form_data.get('email', '')
    if not is_valid_email(email):
        errors.append("Invalid email format.")
        
    # Check if email is already taken    
    elif is_email_taken(email):
        errors.append("Email is already registered.")

    # Phone
    if not is_valid_phone(form_data.get('phone_number', '')):
        errors.append("Invalid phone number. Use digits only, 10–15 digits.")

    # Password
    password = form_data.get('password', '')
    confirm_password = form_data.get('confirm_password', '')
    if not is_strong_password(password):
        errors.append("Password must be at least 8 characters with an uppercase letter, number, and special character.")
    elif password != confirm_password:
        errors.append("Passwords do not match.")

    # Address fields
    if len(form_data.get('address_line1', '')) > 100:
        errors.append("Address Line 1 too long.")
    if len(form_data.get('address_line2', '')) > 100:
        errors.append("Address Line 2 too long.")
    if not is_valid_name(form_data.get('city', '')):
        errors.append("Invalid city name.")
    if not is_valid_state(form_data.get('state', '')):
        errors.append("Invalid state. Use 2-letter abbreviation.")
    if not is_valid_zip(form_data.get('zip_code', '')):
        errors.append("Invalid ZIP code format.")

    return errors

def register_user(form_data):
    """
    Register a new user in the database.
    Returns True if registration is successful, False otherwise.
    """
    # Generate a hashed password
    hashed_password = generate_password_hash(form_data['password'])
    
    # Normalize case for specific fields
    lowercase_fields = ['first_name', 'last_name', 'email', 'phone_number', 'address_line1', 'address_line2', 'city', 'state', 'zip_code']
    form_data = normalize_case_fields(form_data, lowercase_fields)
    form_data = {k: v.lower() if isinstance(v, str) else v for k, v in form_data.items()}
    
    # Insert the user into the database   
    try:
        # Get a connection to the database
        with get_db_connection() as conn:
            with conn.cursor() as cur:
        
                # Execute the SQL query to insert the new customer
                cur.execute("""
                    INSERT INTO customers (
                        first_name, last_name, email, phone_number, password,
                        address_line1, address_line2, city, state, zip_code,
                        is_guest, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, false, NOW())
                """, (
                    form_data['first_name'],
                    form_data['last_name'],
                    form_data['email'].lower(),
                    form_data['phone_number'],
                    hashed_password,
                    form_data['address_line1'],
                    form_data['address_line2'],
                    form_data['city'],
                    form_data['state'],
                    form_data['zip_code']
                ))
                
            # Commit the transaction to save changes    
            conn.commit()
        
        return True
    
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        return False

def get_user_by_email(email):
    """
    Fetch a user from the database by email.
    Returns a dictionary with user details if found, None otherwise.
    """
    # Normalize email to lowercase
    email = email.lower()
    
    # Get a connection to the database
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to fetch the user by email
            cur.execute('SELECT customer_id, email, password FROM customers WHERE email = %s', (email))
            
            # Verify by fetching the row returned by the query and return it
            return cur.fetchone()

def get_name_by_id(user_id):
    """
    Fetch the first and last name of a user by their ID.
    Returns the full name as a string if found, None otherwise.
    """
    # Get a connection to the database
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to fetch the user's name by ID
            cur.execute('SELECT first_name, last_name FROM customers WHERE customer_id = %s', (user_id,))
            
            # Verify by fetching the row returned by the query
            row = cur.fetchone()
            
            # If a row returns True, return the full name
            if row:
                return f"{row[0]} {row[1]}"
            
    return None

def sanitize_form_input(form_data):
    """
    Sanitize form input to prevent XSS attacks and SQL injection.
    Returns a dictionary with sanitized values.
    """
    # Escape all fields
    sanitized = {k: escape(v) for k, v in form_data.items()}
    
    # Lowercase only certain keys
    lowercase_keys = ['email', 'first_name', 'last_name', 'city', 'state']
    
    # Lowercase the values of specified keys
    for key in lowercase_keys:
        if key in sanitized and isinstance(sanitized[key], str):
            sanitized[key] = sanitized[key].lower()

    return sanitized

def normalize_case_fields(form_data, lowercase_fields=None):
    """
    Normalize the case of specified fields in the form data.
    Returns a dictionary with normalized values.
    """
    # Normalize the case of specified fields to lowercase
    lowercase_fields = lowercase_fields or []
    
    return {
        k: v.lower() if k in lowercase_fields and isinstance(v, str) else v
        for k, v in form_data.items()
    }

def is_valid_email(email):
    """
    Validate email format using regex and return True or False.
    """
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

def is_email_taken(email):
    """
    Check if the email is already registered in the database.
    Returns True if the email is taken, False otherwise.
    """
    # Normalize email to lowercase
    email = email.lower()
    
    # Get a connection to the database
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to check if the email exists
            cur.execute("SELECT 1 FROM customers WHERE email = %s", (email,))
            
            return cur.fetchone() is not None

def is_strong_password(password):
    """
    Validate password strength using regex.
    Password must be at least 8 characters long, contain at least one uppercase letter,
    one number, and one special character.
    """
    # Check if the password meets the criteria and return True or False
    return re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$', password)

def is_valid_name(name):
    """
    Validate name format using regex.
    Name can contain letters, spaces, hyphens, and apostrophes.
    """
    # Check if the name meets the criteria and return True or False
    return re.match(r"^[A-Za-z\s'-]{1,50}$", name)

def is_valid_phone(phone):
    """
    Validate phone number format using regex.
    Phone number can contain digits, spaces, hyphens, and parentheses.
    """
    # Remove common formatting symbols: hyphens, spaces, parentheses
    cleared_phone = re.sub(r"[-()\s]", "", phone)
    
    # Check if the phone number meets the criteria and return True or False
    return re.match(r"^\d{10,15}$", cleared_phone)

def is_valid_zip(zip_code):
    """
    Validate ZIP code format using regex.
    ZIP code can be 5 digits or 5 digits followed by a hyphen and 4 digits.
    """
    # Check if the ZIP code meets the criteria and return True or False
    return re.match(r"^\d{5}(-\d{4})?$", zip_code)

def is_valid_state(state):
    """
    Validate state format using regex.
    State should be a 2-letter abbreviation.
    """
    # Check if the state meets the criteria and return True or False
    return re.match(r"^[A-Za-z]{2}$", state)
