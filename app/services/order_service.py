from app.models.db import get_db_connection
from logger import logger  # Make sure to import your logger
from flask import flash

def create_order(customer_id, selected_books, quantities, prices):
    total_amount = sum(qty * price for qty, price in zip(quantities, prices))
    order_items = list(zip(selected_books, quantities))

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO orders (customer_id, order_date, total_amount) VALUES (%s, NOW(), %s) RETURNING order_id',
                    (customer_id, total_amount)
                )
                order_id = cur.fetchone()["order_id"]
                logger.info(f"Order {order_id} created for customer {customer_id} with total ${total_amount:.2f}.")

                for book_id, qty in order_items:
                    cur.execute(
                        'INSERT INTO order_items (order_id, book_id, quantity) VALUES (%s, %s, %s)',
                        (order_id, book_id, qty)
                    )
                    if not decrease_quantity(book_id, qty):
                        logger.warning(f"Failed to decrease stock for book {book_id} after order {order_id}.")

            conn.commit()
        return order_id
    except Exception as e:
        logger.error(f"Failed to create order for customer {customer_id}: {e}")
        return None

def validate_order(selected_books, quantities):
    errors = []

    # Check if each book exists and if quantity is available
    insufficient_stock = check_inventory(selected_books, quantities)
    if insufficient_stock:
        errors.append("Insufficient stock for the following books: " + ', '.join([str(item[0]) for item in insufficient_stock]))

    # Ensure quantities are positive integers
    if any(qty <= 0 for qty in quantities):
        errors.append("Quantities must be positive integers.")

    return errors

def check_inventory(selected_books, quantities):
    insufficient_stock = []

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            for book_id, qty in zip(selected_books, quantities):
                cur.execute("SELECT title, stock_quantity FROM books WHERE book_id = %s", (book_id,))
                book = cur.fetchone()
                if book is None:
                    logger.warning(f"Book ID {book_id} not found during inventory check.")
                    insufficient_stock.append((book_id, "Book not found"))
                elif book["stock_quantity"] < qty:
                    logger.info(f"Insufficient stock for '{book['title']}': requested {qty}, available {book['stock_quantity']}.")
                    insufficient_stock.append((book["title"], book["stock_quantity"]))
                    flash(f"Insufficient stock for '{book['title']}': requested {qty}, available {book['stock_quantity']}.", 'danger')
    
    return insufficient_stock

def update_stock_quantity(book_id, quantity_purchased):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE books 
                    SET stock_quantity = stock_quantity - %s
                    WHERE book_id = %s AND stock_quantity >= %s
                """, (quantity_purchased, book_id, quantity_purchased))
            conn.commit()
        logger.info(f"Stock quantity updated: -{quantity_purchased} for book {book_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating stock quantity for book {book_id}: {e}")
        return False

def update_quantity(book_id, new_quantity):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE books 
                    SET stock_quantity = %s
                    WHERE book_id = %s
                """, (new_quantity, book_id))
            conn.commit()
        logger.info(f"Stock quantity set to {new_quantity} for book {book_id}")
        return True
    except Exception as e:
        logger.error(f"Error setting stock quantity for book {book_id}: {e}")
        return False

def decrease_quantity(book_id, quantity):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE books 
                    SET stock_quantity = stock_quantity - %s
                    WHERE book_id = %s AND stock_quantity >= %s
                """, (quantity, book_id, quantity))
            conn.commit()
        logger.info(f"Decreased stock by {quantity} for book {book_id}")
        return True
    except Exception as e:
        logger.error(f"Error decreasing stock quantity for book {book_id}: {e}")
        return False

def increase_quantity(book_id, quantity):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE books 
                    SET stock_quantity = stock_quantity + %s
                    WHERE book_id = %s
                """, (quantity, book_id))
            conn.commit()
        logger.info(f"Increased stock by {quantity} for book {book_id}")
        return True
    except Exception as e:
        logger.error(f"Error increasing stock quantity for book {book_id}: {e}")
        return False
