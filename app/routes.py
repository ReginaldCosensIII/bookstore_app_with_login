from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.services.order_service import create_order, validate_order
from app.services.auth_service import validate_registration, sanitize_form_input
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.db import get_db_connection
from app.models.customer import Customer
from app.services.order_service import check_inventory
from logger import logger

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM books;')
            books = cur.fetchall()
    return render_template('index.html', books=books)

@bp.route('/create_order', methods=['POST'])
@login_required
def create_order_route():
    
    customer_id = current_user.id
    
    # Get multi-value fields BEFORE sanitizing
    selected_books = request.form.getlist('selected_books')

    # Sanitize the form input
    safe_data = sanitize_form_input(request.form)

    # Extract remaining fields from sanitized form data
    quantities = [int(safe_data.get(f'quantity_{book_id}', 1)) for book_id in selected_books]
    prices = [float(safe_data.get(f'price_{book_id}', 0.0)) for book_id in selected_books]
   
    # Validate order
    errors = validate_order(selected_books, quantities)
    
    if not selected_books or not quantities or not prices or quantities == [0] * len(quantities):
        flash("Please select at least one book and specify a quantity.", 'danger')
        logger.warning("Order validation error: No books or quantities selected.")
        errors.append("Please select at least one book and specify a quantity.")
    if errors:
        for error in errors:
            logger.warning(f"Order validation error: {error}")
        return redirect(url_for('main.index'))
    
    create_order(customer_id, selected_books, quantities, prices)
    flash('Order created successfully!', 'success')
    logger.info(f"Order created successfully for customer {customer_id}.")
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        safe_data = sanitize_form_input(request.form)
        errors = validate_registration(safe_data)

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html', form_data=safe_data)

        # Hash the password
        hashed_password = generate_password_hash(safe_data['password'])

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO customers (
                    first_name, last_name, email, phone_number, password,
                    address_line1, address_line2, city, state, zip_code,
                    is_guest, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, false, NOW())
            """, (
                safe_data['first_name'],
                safe_data['last_name'],
                safe_data['email'],
                safe_data['phone_number'],
                hashed_password,
                safe_data['address_line1'],
                safe_data['address_line2'],
                safe_data['city'],
                safe_data['state'],
                safe_data['zip_code']
            ))
            conn.commit()
            cur.close()
            conn.close()

            flash("Registration successful. You can now log in.", 'success')
            return redirect(url_for('main.login'))

        except Exception as e:
            flash("An error occurred during registration. Please try again.", 'danger')
            print("Registration error:", e)

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        form_data = sanitize_form_input(request.form)
        email = form_data['email'].lower()
        password = form_data['password']
        
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT customer_id, email, password FROM customers WHERE email = %s', (email,))
                user = cur.fetchone()
                
        if user and user["password"] is not None:
            if check_password_hash(user["password"], password):
                customer = Customer(id=user["customer_id"], email=user["email"], password=user["password"])
                login_user(customer)
                logger.info(f"User {email} logged in successfully.")
                flash('Login successful.', 'success')
                return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials', 'danger')
            logger.warning("Invalid login attempt.")
            return redirect(url_for('main.login'))

    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    logger.info("User logged out.")
    return redirect(url_for('main.login'))