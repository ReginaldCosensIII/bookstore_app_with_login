from flask_login import LoginManager
from app.models.customer import Customer
from app.models.db import get_db_connection
from logger import logger  # Importing customer logger here
from werkzeug.security import generate_password_hash
import re
import re
from html import escape

login_manager = LoginManager()
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT customer_id, email, password FROM customers WHERE customer_id = %s',
                    (user_id,)
                )
                row = cur.fetchone()

        if row:
            logger.info(f"User {user_id} loaded from session.")
            return Customer(id=row["customer_id"], email=row["email"], password=row["password"])
        else:
            logger.warning(f"User {user_id} not found in database.")
            return None
    except Exception as e:
        logger.error(f"Error loading user {user_id}: {e}")
        return None
from html import escape

def sanitize_form_input(form_data):
    return {k: escape(v) for k, v in form_data.items()}

def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

def is_email_taken(email):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM customers WHERE email = %s", (email,))
            return cur.fetchone() is not None

def is_strong_password(password):
    return re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$', password)

def is_valid_name(name):
    return re.match(r"^[A-Za-z\s'-]{1,50}$", name)

def is_valid_phone(phone):
    return re.match(r"^\d{10,15}$", phone)

def is_valid_zip(zip_code):
    return re.match(r"^\d{5}(-\d{4})?$", zip_code)

def is_valid_state(state):
    return re.match(r"^[A-Za-z]{2}$", state)

def validate_registration(form_data):
    errors = []

    # Names
    if not is_valid_name(form_data.get('first_name', '')):
        errors.append("Invalid first name.")
    if not is_valid_name(form_data.get('last_name', '')):
        errors.append("Invalid last name.")

    # Email
    email = form_data.get('email', '')
    if not is_valid_email(email):
        errors.append("Invalid email format.")
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

