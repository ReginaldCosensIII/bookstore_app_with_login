from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.services.order_service import create_order  # Import the service
from werkzeug.security import check_password_hash
from app.models.db import get_db_connection
from app.models.customer import Customer

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    conn.close()
    return render_template('index.html', books=books)

@bp.route('/create_order', methods=['POST'])
def create_order_route():
    customer_id = request.form.get("customer_id")
    
    if not customer_id or customer_id.strip() == "":
        customer_id = 1
    else:
        customer_id = int(customer_id)
    
    selected_books = request.form.getlist('selected_books')
    quantities = [int(request.form.get(f'quantity_{book_id}', 1)) for book_id in selected_books]
    prices = [float(request.form.get(f'price_{book_id}', 0.0)) for book_id in selected_books]
    
    # Use the order service to create the order
    create_order(customer_id, selected_books, quantities, prices)
    
    return redirect(url_for('main.index'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT customer_id, email, password FROM customers WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        print(user)  # Debugging line to check the user fetched from DB
        print(f"Email: {email}, Password: {password}")  # Debugging line to check input values
        #print(user[2])
        #print(f"Hashed Password: {user[2]}")
        if user and check_password_hash(user[2], password):  # Compare hashed password
            customer = Customer(id=user[0], email=user[1], password=user[2])
            login_user(customer)
            return redirect(url_for('main.index'))  # or any protected route
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))
