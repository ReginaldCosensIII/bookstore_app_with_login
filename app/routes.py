# app/routes.py
from logger import logger
from app.models.customer import Customer
from app.auth_exceptions import RegistrationError
from app.services.book_service import get_all_books
from app.services.order_service import create_order, get_order_details
from app.services.auth_service import get_name_by_id, authenticate_user
from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.reg_service import validate_registration, sanitize_form_input, register_user
from app.order_exceptions import QuantityExceedsStock, InvalidOrderFormat, OrderCreationError, DatabaseOperationError

bp = Blueprint('main', __name__)

@bp.route("/order/confirmation")
@login_required
def order_confirmation():
    """
    Renders the order confirmation page with order details.
    It fetches the order ID from the URL and retrieves the order details from the database.
    If the order is not found, it flashes an error message and redirects to the index page.
    """
    # Fetch the order_id from the URL parameters
    order_id = request.args.get("order_id")  # Fetch the order_id from the URL
    
    # Check if order_id is present 
    if not order_id:
        flash("Order id not found.")
        
        # Redirect to the index page if order_id is not found
        return redirect(url_for("main.index"))

    # Fetch the order from the database using order_id
    order_items = get_order_details(order_id)

    # If order_items is None or empty, flash an error message and redirect to the index page
    if not order_items:        
        flash("Order not found.")        
        
        # Redirect to the index page if order not found
        return redirect(url_for("main.index"))
    
    # Render the order confirmation page with the order details
    return render_template("order_confirmation.html", order=order_items)

@bp.route('/')
@login_required
def index():
    """
    Renders the index page with a list of books and the user's name.
    If no books are available, a warning message is displayed.
    """
    # Get all books from the database and assigns user name
    books = get_all_books()
    users_name = get_name_by_id(current_user.id).title()
    
    # Check if books is empty and if so, flash a warning message
    if not books:
        flash("No books available at the moment.", 'warning')
        logger.warning("No books available in the database.")
        
        # Render the index page with an empty list of books
        return render_template('index.html', books=[], users_name = users_name)
    
    else:
        logger.info(f"Books retrieved successfully for user {current_user.id}.")
        
        # Render the index page with the list of books and user's name
        return render_template('index.html', books=books, users_name = users_name)

@bp.route('/create_order', methods=['POST'])
@login_required
def create_order_route():
    """
    Handles the creation of an order based on the request data.
    Validates the order data and creates an order in the database.
    If successful, redirects to the index page with a success message.
    If an error occurs, flashes an error message and redirects to the index page.
    """
    if request.method == 'POST':
        # Assigns cusomter_id and total_amount and items_json from the request form
        customer_id = current_user.id
        total_amount = float(request.form.get("total_amount", 0))
        items_json = request.form.get("items")

        try:
            # Starts the order creation process
            order_condition = create_order(customer_id, items_json, total_amount)
            session["last_order_id"] = order_condition["order_id"]  # make sure you store this
            
            # Checks if the order was created successfully and if an order ID was returned
            if order_condition["success"] == True and order_condition["order_id"] is not None:
                order_id = order_condition["order_id"]
                logger.info(f"Order {order_id} created successfully for customer {customer_id}.")
                flash("Order created successfully!", "success")
                
                # Redirect to the order confirmation page with the order ID                
                return redirect(url_for('main.order_confirmation', order_id=order_id))
            
            else:
                flash("Order creation failed. Please try again.", "danger")
                logger.error(f"Order creation failed: {order_condition['error']}")
                
                # Redirect to the index page if order creation failed                
                return redirect(url_for('main.index'))
            
        # Custom exceptions for specific error handling
        except QuantityExceedsStock as qes:
            flash(str(qes), "danger")  # Displays error message like "Quantity exceeds stock for book ID: 1"
            logger.warning(f"Order validation error: {qes}") 
            
            # Redirect to the index page if quantity exceeds stock           
            return redirect(url_for('main.index'))
        
        except ValueError as ve:
            flash(str(ve), "warning")  # Displays error message like "Invalid order items format"
            logger.warning(f"Order validation error: {ve}")
            
            # Redirect to the index page if invalid order items format
            return redirect(url_for('main.index'))

        except Exception as e:
            flash("An unexpected error occurred while creating the order.", "danger")
            logger.exception("Unexpected error during order creation")
            
            # Redirect to the index page if an unexpected error occurred
            return redirect(url_for('main.index'))

    # Redirect to the index page if the request method is not POST
    return redirect(url_for('main.index'))
   
@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration. If the request method is POST, it processes the registration form data.
    It sanitizes the input, validates the data, and attempts to register the user.
    If successful, redirects to the login page with a success message.
    If there are validation errors, it flashes error messages and re-renders the registration form.
    """
    if request.method == 'POST':
        # Sanitizes the form input to prevent XSS attacks/SQL injection and validates the registration data
        safe_data = sanitize_form_input(request.form)
        errors = validate_registration(safe_data)

        # Check for errors in the registration data
        if errors:
            for error in errors:
                flash(error, 'danger')
            
            # Render the registration form with the sanitized data and error messages
            return render_template('register.html', form_data=safe_data)

        # Register the user in the database and verify if the registration was successful
        if register_user(safe_data):
            flash("Registration successful. You can now log in.", 'success')
            
            # Redirect to the login page after successful registration
            return redirect(url_for('main.login'))
        
        # Else, if the registration failed, flash an error message and log the error
        else:
            flash("An error occurred during registration. Please try again.", 'danger')
            logger.error(f"Registration error:")
            
            # Redirect to the registration page if registration failed
            return redirect(url_for('main.register'))

    # Render the registration form if the request method is GET
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login. If the request method is POST, it processes the login form data.
    It sanitizes the input, authenticates the user, and logs them in if successful.
    If authentication fails, it flashes an error message and redirects to the login page.
    """
    if request.method == 'POST':
        # Sanitize the form input to prevent XSS attacks/SQL injection and assigns email and password
        form_data = sanitize_form_input(request.form)
        email = form_data['email'].lower()
        password = form_data['password']

        try:
            # Authenticate the user using the provided email and password
            customer = authenticate_user(email, password)
            
            # Verify if the authentication was successful
            if customer:
                # log the user in and redirect to the index page
                login_user(customer)
                logger.info(f"User {email} logged in successfully.")
                flash('Login successful.', 'success')
                
                # Redirect to the index page
                return redirect(url_for('main.index'))
            
            # Else, if the authentication failed, flash an error message and log the error
            else:
                flash('Invalid credentials.', 'danger')
                logger.warning(f"Invalid login attempt for email: {email}")
                
                # Redirect to the login page if authentication failed
                return redirect(url_for('main.login'))

        except Exception as e:
            flash('An unexpected error occurred during login.', 'danger')
            
            # Redirect to the login page if an unexpected error occurred
            return redirect(url_for('main.login'))
        
    # Render the login form if the request method is GET
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    """
    Logs out the current user and redirects to the login page.
    It also flashes a message indicating successful logout.
    """
    # Log out the user and redirect to the login page
    logout_user()
    
    # Log logout and Flash a message indicating successful logout
    logger.info("User logged out.")
    flash('You have been logged out.', 'info')
    
    # Redirect to the login page
    return redirect(url_for('main.login'))