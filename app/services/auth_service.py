# bookstore_app_with_login/app/services/auth_service.py

from werkzeug.security import check_password_hash # For verifying passwords
from flask_login import LoginManager # Manages user sessions
from app.models.customer import Customer # Customer model
from app.models.db import get_db_connection # DB connection utility
from logger import logger # Custom logger
from html import escape # For basic input sanitization (prevent XSS)

# Initialize the LoginManager instance.
# This instance will be further configured in the application factory (__init__.py).
login_manager = LoginManager()
login_manager.login_view = 'main.login' # Route name for the login page
login_manager.login_message_category = 'info' # Flash message category

@login_manager.user_loader
def load_user(user_id):
    """
    Callback function used by Flask-Login to load a user object from the
    user ID stored in the session.

    Args:
        user_id (str): The user ID stored in the session cookie.

    Returns:
        Customer | None: The Customer object corresponding to the user_id,
                        or None if the user is not found or an error occurs.
    """
    try:
        # Ensure user_id is an integer before querying the database
        customer_id = int(user_id)
        # Use the Customer model's method to fetch the user by ID
        customer = Customer.get_by_id(customer_id)
        if customer:
            logger.debug(f"User {customer_id} loaded successfully from session.")
        else:
            # This case might happen if the user was deleted after logging in
            logger.warning(f"User ID {customer_id} found in session, but no matching user in database.")
        return customer # Return the Customer object or None if not found
    except ValueError:
        logger.error(f"Invalid user_id format encountered in session: {user_id}")
        return None
    except Exception as e:
        # Catch potential database or other errors during user loading
        logger.exception(f"Error loading user {user_id} from database: {e}")
        return None # Important to return None on error

def authenticate_user(email, password):
    """
    Authenticates a user based on email and password.

    Args:
        email (str): The user's email address.
        password (str): The plain-text password entered by the user.

    Returns:
        Customer | None: The authenticated Customer object if credentials are valid,
                        otherwise None.

    Raises:
        Exception: Propagates database or other unexpected errors.
    """
    if not email or not password:
        logger.warning("Authentication attempt with empty email or password.")
        return None # Basic check for empty credentials

    # Sanitize email: remove leading/trailing whitespace and convert to lowercase
    normalized_email = escape(email.strip().lower())

    try:
        # Fetch the customer record by the normalized email address
        customer = Customer.get_by_email(normalized_email)

        # Check if a customer was found and if the provided password matches the stored hash
        if customer and customer.password and check_password_hash(customer.password, password):
            # Password hashes match - authentication successful
            logger.info(f"User '{normalized_email}' authenticated successfully.")
            return customer # Return the Customer object
        else:
            # Either customer not found or password doesn't match
            logger.warning(f"Authentication failed for user: {normalized_email}. Invalid email or password.")
            return None # Indicate authentication failure

    except Exception as e:
        # Log any unexpected errors during the database query or password check
        logger.exception(f"Error during authentication process for user {normalized_email}: {e}")
        # Re-raise the exception to be handled by the calling route/function
        raise