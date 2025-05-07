# bookstore_app_with_login/app/services/reg_service.py

import re # Regular expression module for validation
from html import escape # For basic XSS prevention on string inputs
from logger import logger
from app.models.customer import Customer # Customer database model
from app.models.db import get_db_connection # Database connection utility
from werkzeug.security import generate_password_hash # For hashing passwords
# Import custom exceptions if needed for specific registration errors
# from app.auth_exceptions import RegistrationError, UserAlreadyExists

# --- Constants for Validation ---
# Regex patterns can be adjusted based on specific requirements
# Basic email regex (adjust for stricter validation if needed)
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
# Example password strength: min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]:;\"'<>,.?/~`]).{8,}$"
# Basic name validation (letters, spaces, hyphens, apostrophes, limited length)
NAME_REGEX = r"^[A-Za-z\s'-]{1,50}$"
# Phone validation (allows digits, optional hyphens/spaces/parentheses, specific length range)
PHONE_DIGITS_REGEX = r"^\d{10,15}$" # Matches 10 to 15 digits after stripping formatting
# ZIP code validation (allows 5 digits or 5+4 format)
ZIP_CODE_REGEX = r"^\d{5}(-\d{4})?$"
# State validation (exactly 2 letters)
STATE_REGEX = r"^[A-Za-z]{2}$"
# Basic address line validation (limit length, allow common characters)
ADDRESS_REGEX = r"^[A-Za-z0-9\s.,#'\-\/]{1,100}$"


def register_user(form_data):
    """
    Handles the user registration process including validation and database insertion.

    Args:
        form_data (dict): A dictionary containing the user's registration details
                          (e.g., from request.form).

    Returns:
        dict: A dictionary indicating success or failure:
              {'success': True, 'message': 'Registration successful.'} on success.
              {'success': False, 'messages': ['Error message 1', ...]} on failure.
    """
    logger.info(f"Starting registration process for email: {form_data.get('email')}")

    # 1. Sanitize input first to prevent injection issues before validation/processing
    # Note: sanitize_form_input might be better placed in the route before calling this service
    safe_data = sanitize_form_input(form_data) # Ensure data is escaped

    # 2. Validate the sanitized data
    validation_errors = validate_registration(safe_data)
    if validation_errors:
        logger.warning(f"Registration validation failed for {safe_data.get('email')}: {validation_errors}")
        # Return specific validation errors
        return {'success': False, 'messages': validation_errors}

    # 3. Hash the password securely
    try:
        hashed_password = generate_password_hash(safe_data['password'])
    except Exception as e:
        logger.exception(f"Password hashing failed for {safe_data.get('email')}: {e}")
        # Return a generic internal error message
        return {'success': False, 'messages': ['An internal error occurred during registration.']}

    # 4. Prepare Customer object data
    # Combine first and last names for the 'name' field if it's still used in the DB schema
    full_name = f"{safe_data.get('first_name', '')} {safe_data.get('last_name', '')}".strip()

    # 5. Attempt to save the new customer to the database
    try:
        # Create a Customer instance (without an ID initially)
        new_customer = Customer(
            customer_id=None, # Will be set by DB upon insertion
            name=full_name,
            email=safe_data['email'], # Already normalized (lowercase, stripped) by sanitize
            phone_number=re.sub(r"[-()\s]", "", safe_data.get('phone_number', '')), # Store cleaned phone number
            password=hashed_password, # Store the hashed password
            is_guest=False, # New registrations are not guests
            created_at=None, # Let DB handle timestamp
            first_name=safe_data.get('first_name'),
            last_name=safe_data.get('last_name'),
            address_line1=safe_data.get('address_line1'),
            address_line2=safe_data.get('address_line2'), # Will be None if not present
            city=safe_data.get('city'),
            state=safe_data.get('state'),     # Already normalized (lowercase) by sanitize
            zip_code=safe_data.get('zip_code')
        )

        # Use the Customer model's save method
        new_customer.save_to_db() # This handles the DB connection and commit

        logger.info(f"Successfully registered new customer: {new_customer.email} with ID: {new_customer.customer_id}")
        return {'success': True, 'message': 'Registration successful. Please log in.'}

    except Exception as e:
        # Catch potential database errors (e.g., unique constraint violation if email check failed somehow, connection issues)
        logger.exception(f"Database error during registration for {safe_data.get('email')}: {e}")
        # Check for specific DB errors if possible (e.g., unique violation)
        # For now, return a generic error
        return {'success': False, 'messages': ['Registration failed due to a database error. Please try again later.']}


def validate_registration(data):
    """
    Validates the provided registration data dictionary.

    Args:
        data (dict): The sanitized registration data.

    Returns:
        list[str]: A list of error messages. An empty list indicates success.
    """
    errors = []
    required_fields = [
        'first_name', 'last_name', 'email', 'phone_number',
        'password', 'confirm_password', 'address_line1',
        'city', 'state', 'zip_code'
    ]

    # Check for missing required fields
    for field in required_fields:
        if not data.get(field):
            errors.append(f"{field.replace('_', ' ').title()} is required.")

    # If required fields are missing, return early
    if errors:
        return errors

    # --- Field-specific Validations ---
    if not re.match(NAME_REGEX, data['first_name']):
        errors.append("Invalid first name format (letters, spaces, hyphens, apostrophes allowed, max 50 chars).")
    if not re.match(NAME_REGEX, data['last_name']):
        errors.append("Invalid last name format (letters, spaces, hyphens, apostrophes allowed, max 50 chars).")

    # Email validation and uniqueness check
    email = data['email']
    if not re.match(EMAIL_REGEX, email):
        errors.append("Invalid email format.")
    else:
        # Check if email already exists in the database
        # This requires a database query - potentially move this check earlier or handle DB error in register_user
        try:
            if Customer.get_by_email(email):
                errors.append("This email address is already registered.")
                logger.warning(f"Registration attempt with existing email: {email}")
        except Exception as e:
            # Log DB error during validation but might let registration proceed to catch DB constraint error later
            logger.error(f"Database error during email uniqueness check for {email}: {e}")
            errors.append("Could not verify email uniqueness at this time.")


    # Phone number validation (check digits after stripping formatting)
    phone_digits = re.sub(r"[-()\s]", "", data['phone_number'])
    if not re.match(PHONE_DIGITS_REGEX, phone_digits):
        errors.append("Invalid phone number format (must contain 10-15 digits).")

    # Password validation
    password = data['password']
    confirm_password = data['confirm_password']
    if not re.match(PASSWORD_REGEX, password):
         errors.append("Password must be at least 8 characters and include an uppercase letter, a lowercase letter, a number, and a special character.")
    elif password != confirm_password:
        errors.append("Password and confirmation password do not match.")

    # Address validation
    if not re.match(ADDRESS_REGEX, data['address_line1']):
         errors.append("Invalid Address Line 1 format (max 100 chars, common characters allowed).")
    # Address line 2 is optional, but validate if present
    if data.get('address_line2') and not re.match(ADDRESS_REGEX, data['address_line2']):
         errors.append("Invalid Address Line 2 format (max 100 chars, common characters allowed).")
    if not re.match(NAME_REGEX, data['city']): # Assuming city names follow similar rules to person names
        errors.append("Invalid city format.")
    if not re.match(STATE_REGEX, data['state']):
        errors.append("Invalid state format (must be 2-letter abbreviation).")
    if not re.match(ZIP_CODE_REGEX, data['zip_code']):
        errors.append("Invalid ZIP code format (e.g., 12345 or 12345-6789).")

    return errors


def sanitize_form_input(form_data):
    """
    Sanitizes string values in a dictionary by escaping HTML and stripping whitespace.
    Also converts specified fields to lowercase.

    Args:
        form_data (dict): The input dictionary (e.g., request.form).

    Returns:
        dict: A new dictionary with sanitized values.
    """
    sanitized = {}
    # Fields to convert to lowercase during sanitization
    lowercase_fields = {'email', 'first_name', 'last_name', 'city', 'state'}

    for key, value in form_data.items():
        if isinstance(value, str):
            # Escape HTML special characters and strip leading/trailing whitespace
            processed_value = escape(value.strip())
            # Convert to lowercase if the key is in the designated set
            if key in lowercase_fields:
                processed_value = processed_value.lower()
            sanitized[key] = processed_value
        else:
            # Keep non-string values as they are (e.g., numbers if form allows)
            sanitized[key] = value
    return sanitized

# Note: normalize_case_fields seems redundant if lowercase conversion is handled in sanitize_form_input.
# Keeping sanitize_form_input as the primary sanitization step.