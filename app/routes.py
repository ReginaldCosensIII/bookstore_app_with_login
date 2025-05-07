# bookstore_app_with_login/app/routes.py

# Import models
from app.models.book import Book
from app.models.customer import Customer
from app.models.db import get_db_connection # Import DB connection function

# Import custom exceptions
from app.auth_exceptions import RegistrationError
from app.order_exceptions import QuantityExceedsStock, InvalidOrderFormat

# Import services
from app.services.auth_service import authenticate_user
from app.services.reg_service import register_user, sanitize_form_input
from app.services.order_service import create_order, get_confirmation_details

# Import other necessities 
import json
from logger import logger # Import custom logger
from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

# Create a Blueprint named 'main'
# Blueprints help organize routes in larger applications.
bp = Blueprint('main', __name__)

# --- Order Routes ---

@bp.route("/order/confirmation")
@login_required # Ensures only logged-in users can access this route
def order_confirmation():
    """
    Displays the order confirmation page for a specific order.

    Fetches the order ID from the URL query parameters and retrieves
    the detailed order information (including customer and item details)
    using the `get_confirmation_details` service function.
    """
    order_id = request.args.get("order_id") # Get 'order_id' from query string (?order_id=123)

    if not order_id:
        flash("Order ID is missing.", "warning")
        logger.warning("Attempted to access order confirmation without an order_id.")
        return redirect(url_for("main.index"))

    try:
        order_id = int(order_id) # Ensure order_id is an integer
        with get_db_connection() as conn:
            order_details = get_confirmation_details(order_id, conn) # Fetch details via service

        if not order_details:
            flash("Order not found or you do not have permission to view it.", "warning")
            logger.warning(f"Order confirmation attempt failed: Order ID {order_id} not found or access denied for user {current_user.customer_id}.")
            return redirect(url_for("main.index"))

        logger.info(f"Displaying confirmation for Order ID: {order_id}")
        # Pass the fetched details to the template
        return render_template("order_confirmation.html", order=order_details)

    except ValueError:
        flash("Invalid Order ID format.", "danger")
        logger.error(f"Invalid Order ID format received: {order_id}")
        return redirect(url_for("main.index"))
    except Exception as e:
        flash("An error occurred while retrieving order details.", "danger")
        logger.exception(f"Error retrieving order confirmation for Order ID {order_id}: {e}")
        return redirect(url_for("main.index"))


@bp.route('/create_order', methods=['POST'])
@login_required
def create_order_route():
    """
    Handles the submission of the order form.

    Processes the selected books and quantities, calculates the total,
    and attempts to create the order using the `create_order` service.
    Handles potential errors like stock issues or invalid data.
    """
    if request.method == 'POST':
        try:
            customer_id = current_user.customer_id # Get ID of the logged-in user
            # Safely get total_amount, default to 0.0 if missing or invalid
            total_amount_str = request.form.get("total_amount", "0")
            total_amount = float(total_amount_str) if total_amount_str else 0.0

            items_json_str = request.form.get("items") # Get items as a JSON string

            if not items_json_str:
                flash("No items selected for the order.", "warning")
                logger.warning(f"Order creation attempt by user {customer_id} failed: No items provided.")
                return redirect(url_for('main.index'))

            # Parse the JSON string into a Python list/dict
            items_data = json.loads(items_json_str)

            logger.info(f"Processing order creation for customer {customer_id} with items: {items_data}")

            # Call the order creation service function
            order_result = create_order(customer_id, items_data, total_amount)

            # Check the result from the service
            if order_result.get("success") and order_result.get("order_id"):
                order_id = order_result["order_id"]
                session["last_order_id"] = order_id # Store last order ID in session if needed
                logger.info(f"Order {order_id} created successfully for customer {customer_id}.")
                flash("Order created successfully!", "success")
                # Redirect to the confirmation page
                return redirect(url_for('main.order_confirmation', order_id=order_id))
            else:
                # If the service indicates failure without a specific exception
                error_msg = order_result.get('message', 'Order creation failed. Please try again.')
                flash(error_msg, "danger")
                logger.error(f"Order creation failed for customer {customer_id}: {error_msg}")
                return redirect(url_for('main.index'))

        # Handle specific known exceptions from the service layer
        except (QuantityExceedsStock, InvalidOrderFormat) as e:
            flash(str(e), "warning") # Show the specific error message to the user
            logger.warning(f"Order validation error for customer {customer_id}: {e}")
            return redirect(url_for('main.index'))
        except json.JSONDecodeError:
            flash("Invalid order data submitted.", "danger")
            logger.error(f"Failed to decode items JSON for customer {customer_id}.")
            return redirect(url_for('main.index'))
        except ValueError:
             flash("Invalid total amount received.", "danger")
             logger.error(f"Invalid total amount format received for customer {customer_id}.")
             return redirect(url_for('main.index'))
        # Handle unexpected errors
        except Exception as e:
            flash("An unexpected error occurred while creating the order.", "danger")
            logger.exception(f"Unexpected error during order creation for customer {customer_id}: {e}")
            return redirect(url_for('main.index'))

    # Redirect if not a POST request (shouldn't normally happen with route decorator)
    return redirect(url_for('main.index'))


# --- Authentication & User Routes ---

@bp.route('/')
@login_required
def index():
    """
    Displays the main bookstore page showing available books.

    Fetches all books from the database and the current user's name
    to personalize the welcome message.
    """
    try:
        books = Book.get_all_books() # Fetch all books using the model method
        # Safely get user's name - assumes Customer model has get_full_name()
        user_customer = Customer.get_by_id(current_user.customer_id)
        users_name = user_customer.get_full_name().title() if user_customer else "Valued Customer"

        if not books:
            flash("No books available at the moment.", 'warning')
            logger.warning("Book index loaded, but no books found in the database.")

        logger.info(f"Index page loaded successfully for user {current_user.customer_id}.")
        return render_template('index.html', books=books, users_name=users_name)

    except Exception as e:
        flash("Error loading bookstore contents.", "danger")
        logger.exception(f"Error loading index page for user {current_user.customer_id}: {e}")
        # Render template with empty list and default name on error
        return render_template('index.html', books=[], users_name="Valued Customer")


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.

    GET: Displays the registration form.
    POST: Processes submitted registration data, validates it,
          and attempts to register the user via the `register_user` service.
    """
    if request.method == 'POST':
        # Sanitize form data first
        safe_data = sanitize_form_input(request.form)
        logger.info(f"Registration attempt with email: {safe_data.get('email')}")

        # Call the registration service function
        result = register_user(safe_data) # register_user handles validation internally

        if result.get("success"):
            flash(result.get("message", "Registration successful. Please log in."), 'success')
            logger.info(f"Registration successful for email: {safe_data.get('email')}")
            return redirect(url_for('main.login')) # Redirect to login page on success
        else:
            # If registration failed, flash the error messages provided by the service
            error_messages = result.get("messages", ["Registration failed."])
            for error in error_messages:
                flash(error, 'danger')
            logger.warning(f"Registration failed for email {safe_data.get('email')}: {error_messages}")
            # Re-render the registration form, passing back the (sanitized) data
            # to repopulate fields, helping the user correct errors.
            return render_template('register.html', form_data=safe_data)

    # For GET request, just render the empty registration form
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.

    GET: Displays the login form.
    POST: Processes submitted login credentials, authenticates the user
          via the `authenticate_user` service, and logs them in using Flask-Login.
    """
    if request.method == 'POST':
        # Sanitize form data first
        safe_data = sanitize_form_input(request.form)
        email = safe_data.get('email')
        password = safe_data.get('password')

        if not email or not password:
            flash("Email and password are required.", "warning")
            return redirect(url_for('main.login'))

        logger.info(f"Login attempt for email: {email}")

        try:
            # Attempt to authenticate the user using the service
            customer = authenticate_user(email, password)
                
            if customer is not None:
                # If authentication is successful, log the user in
                login_user(customer) # Flask-Login handles session management
                logger.info(f"User '{email}' logged in successfully.")
                flash('Login successful.', 'success')

                # Redirect to the page the user was trying to access, or index if none
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.index'))
            else:
                # Authentication failed (wrong email/password)
                flash('Invalid email or password.', 'danger')
                logger.warning(f"Invalid login attempt for email: {email}")
                # Re-render login form, potentially with email pre-filled
                return render_template('login.html', email=email)

        # Handle unexpected errors during the login process
        except Exception as e:
            flash("An unexpected error occurred during login.", 'danger')
            logger.exception(f"Unexpected error during login for email {email}: {e}")
            return redirect(url_for('main.login'))

    # For GET request, render the login form
    return render_template('login.html')

@bp.route('/logout')
@login_required # Ensure user must be logged in to log out
def logout():
    """
    Logs out the current user.
    Uses Flask-Login's `logout_user` function to clear the session.
    """
    user_email = current_user.email # Get email before logging out for logging
    logout_user() # Clears the user session
    logger.info(f"User '{user_email}' logged out.")
    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('main.login')) # Redirect to the login page