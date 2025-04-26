# app/services/order_service.py
import json
from logger import logger
from decimal import Decimal
from datetime import datetime
from app.models.book import Book
from app.models.order import Order
from app.models.customer import Customer
from psycopg2.extras import RealDictCursor
from app.models.order_item import OrderItem
from app.models.db import get_db_connection
from app.order_exceptions import QuantityExceedsStock
from app.services.book_service import get_quantity_by_book_id

def create_order(customer_id, order_items, total_amount):
    """
    Create an order and its items in the database.
    Validate the order items and total amount before proceeding.
    If any validation fails, log the error and return a failure response.
    If the order is created successfully, return the order ID.
    """
    try:
        # Initialize the order items and reassure total amount is a float
        total_amount = float(total_amount)
        items = json.loads(order_items)
        
        # Validate order items and total amount
        if not validate_order_items(items, total_amount, customer_id):
            logger.error("Invalid order items format")
            raise ValueError("Invalid order items format")
        
        # Get DB connection to create order
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                
                # Insert order and set order ID
                order_id = insert_order(cur, customer_id, total_amount)
                
                # Check if order ID is valid
                if not order_id:
                    raise ValueError("Order insertion failed")
                
                # Log the order ID
                logger.info(f"Order inserted with ID: {order_id}")
                
                # Insert order items if not raise an error
                if not insert_order_items(cur, items, order_id):
                    raise ValueError("Failed to insert order items")
                
                # Decrease stock quantities if not raise an error
                if not decrease_stock_quantities(cur, items):
                    raise ValueError("Failed to update stock quantities")
                
                # Commit the transaction
                conn.commit()
                
                # Log the successful order and items insertion
                logger.info(f"Order and items committed successfully: {order_id}")
                
                return {"success": True, "order_id": order_id}
            
    # Handle specific exceptions for better error handling
    except (json.JSONDecodeError, TypeError) as e:
        logger.error(f"Error decoding JSON or invalid type: {e}")
        conn.rollback()              
        return {"success": False, "error": str(e)}

def validate_order_items(order_items, total_amount, customer_id):
    """
    Validate order items, total amount, customer_id to ensure they are in the correct format and 
    have valid quantities.
    """
    # Check if customer_id is an int and positive integer
    if not isinstance(customer_id, int):
        logger.error("Invalid customer ID")
        return False
    
    # Check if customer id exists in the database
    if not check_if_customer_exists(customer_id):
        logger.error(f"Customer with ID {customer_id} does not exist")
        return False
    
    # Total amount and customer ID should be positive integers
    if total_amount <= 0 or customer_id <= 0:
        logger.error("Total amount or customer ID is not a positive integer")
        return False
    
    # For loop to checks each order item in the order_items list
    for item in order_items:
        book_id = item["book_id"]
        quantity = item["quantity"]
           
        # Check if item is a dictionary
        if not isinstance(item, dict):
            logger.error("Order item is not a dictionary")
            return False
        
        # Check if item contains book_id and quantity
        if "book_id" not in item or "quantity" not in item:
            logger.error("Order item does not contain book_id or quantity")
            return False
        
        # Check if book_id and quantity are integers
        if not isinstance(item["book_id"], int) or not isinstance(item["quantity"], int):
            logger.error("book_id or quantity is not an integer")
            return False
        
        # Check if book_id is positive integers
        if book_id <= 0:
            logger.error("book_id is not a positive integer")
            return False

        # Check if quantity is a positive integer
        if quantity <= 0:
            logger.error("Quantity is not a positive integer")
            return False
            
        # Check if the book exists in the database
        if not check_if_book_exists(book_id):
            logger.error(f"Book with ID {book_id} does not exist")
            return False    
          
        # Check if the quantity is available in stock
        available = get_quantity_by_book_id(book_id) 
                    
        if quantity > available:
            # Log the error if requested quantity is greater than available stock
            logger.error(f"Requested {quantity} but only {available} in stock for book {book_id}")
            raise QuantityExceedsStock(get_title_by_book_id(book_id), quantity, available)

    return True 

def get_title_by_book_id(book_id):
    """
    Get the title of a book by its ID.
    """
    # Get DB connection
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to fetch the book title by its ID
            cur.execute('SELECT title FROM books WHERE book_id = %s;', (book_id,))
            
            # Verify if the book exists by fetching the row
            row = cur.fetchone()
            
            # If row returns true, return the book title
            if row:
                return row[0]
            
    return None 

def insert_order(cur, customer_id, total_amount):
    """
    Insert an order into the database using the provided cursor.
    """
    # Validate customer ID and total amount
    if not isinstance(customer_id, int) or customer_id <= 0:
        logger.error("Invalid customer ID")
        return None
    
    # Execute the SQL query to insert order into the database
    cur.execute(
        "INSERT INTO orders (customer_id, order_date, total_amount) "
        "VALUES (%s, CURRENT_TIMESTAMP, %s) RETURNING order_id;",
        (customer_id, total_amount)
    )
    
    # Fetch the order ID of the inserted order
    row = cur.fetchone()
    
    # Check if the order was inserted successfully
    if row is None:
        logger.error("Failed to insert order")
        return None
    
    return row[0]

def insert_order_items(cur, order_items, order_id):
    """
    Insert order items into the database using the provided cursor.
    """
    # Validate order ID and order items
    if not isinstance(order_items, list) or len(order_items) == 0:
        logger.error("Order items are not in the correct format")
        return False
    
    # For loop to insert each order item into the database
    for item in order_items:
        book_id = item["book_id"]
        quantity = item["quantity"]
        
        # Execute the SQL query to insert order item into the database
        cur.execute(
            "INSERT INTO order_items (order_id, book_id, quantity) VALUES (%s, %s, %s);",
            (order_id, book_id, quantity)
        )
        
        # Check if the order item was inserted successfully
        if cur.rowcount == 0:
            logger.error(f"Failed to insert order item for book ID {book_id}")
            return False
        
    return True

def decrease_stock_quantities(cur, order_items):
    """
    Decrease stock for each book in the order using a single cursor.
    """
    # Validate order items
    if not isinstance(order_items, list) or len(order_items) == 0:
        logger.error("Order items are not in the correct format")
        return False
    
    # For loop to decrease stock for each book in the order
    for item in order_items:
        book_id = item["book_id"]
        quantity = item["quantity"]
        
        # Execute the SQL query to decrease stock quantity for the book
        cur.execute(
            "UPDATE books SET stock_quantity = stock_quantity - %s WHERE book_id = %s;",
            (quantity, book_id)
        )
        
        # Check if the stock quantity was updated successfully
        if cur.rowcount == 0:
            logger.error(f"Failed to decrease stock for book ID {book_id}")
            return False
        
    return True

def decrease_stock(book_id, quantity):
    """
    Decrease stock for a specific book.
    """
    # Validate book ID
    if not isinstance(book_id, int) or book_id <= 0:
        logger.error("Invalid book ID")
        return False
      
    # Validate quantity
    if not isinstance(quantity, int) or quantity <= 0:
        logger.error("Invalid quantity")
        return False
     
    # Check if the book exists in the database
    if not check_if_book_exists(book_id):
        logger.error(f"Book with ID {book_id} does not exist")
        return False
       
    # Check if the quantity is available in stock
    available = get_quantity_by_book_id(book_id)
    if quantity > available:        
        logger.error(f"Requested {quantity} but only {available} in stock for book {book_id}")
        raise QuantityExceedsStock(get_title_by_book_id(book_id), quantity, available)
        return False
    
    # Get DB connection and to decrease stock for the book
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to decrease stock quantity for the book
            cur.execute(
                "UPDATE books SET stock_quantity = stock_quantity - %s WHERE book_id = %s;",
                (quantity, book_id)
            )
            
            # Check if the update was successful
            if cur.rowcount == 0:
                logger.error(f"Failed to decrease stock for book ID {book_id}")
                return False
            
    return True

def check_if_book_exists(book_id):
    """
    Get DB connection and check if a book exists in the database using its book ID.
    """
    # Get DB connection
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to check if the book exists by its ID
            cur.execute('SELECT book_id FROM books WHERE book_id = %s;', (book_id,))
            
            # Verify if the book exists by fetching the row
            row = cur.fetchone()
            
            # If row returns true, it means the book exists in the database
            if row is not None:
                logger.info(f"Book with ID {book_id} exists in the database")
                return True
        
        return False
    
def check_if_order_exists(order_id):
    """
    Get DB connection and check if an order exists in the database using its order ID.
    """
    # Get DB connection
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to check if the order exists by its ID
            cur.execute('SELECT order_id FROM orders WHERE order_id = %s;', (order_id,))
            
            # Verify if the order exists by fetching the row
            row = cur.fetchone()
            
            # If row returns true, it means the order exists in the database
            if row:
                return True
        
        return False
    
def check_if_customer_exists(customer_id):
    """
    Get DB connection and check if a customer exists in the database using its customer ID.
    """
    # Get DB connection
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to check if the customer exists by its ID
            cur.execute('SELECT customer_id FROM customers WHERE customer_id = %s;', (customer_id,))
            
            # Verify if the customer exists by fetching the row
            row = cur.fetchone()
            
            # If row returns true, it means the customer exists in the database
            if row:
                return True
        
        return False

def get_order_details(order_id):
    """
    Get order details by order ID.
    Fetches order information, customer details, and order items from the database.
    """
    # Validate order ID exist in the database
    if not check_if_order_exists(order_id):
        logger.error(f"Order with ID {order_id} does not exist")
        return None
    
    # Get DB connection
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to fetch order details by order ID and assign details
            cur.execute('SELECT order_id, customer_id, order_date, total_amount FROM orders WHERE order_id = %s;', (order_id,))
            row = cur.fetchone()
            order_id = row[0]
            customer_id = row[1]
            order_date = row[2]
            total_amount = row[3]
            
            # Execute the SQL query to fetch customer details by customer ID and assign details          
            cur.execute('SELECT first_name, last_name FROM customers WHERE customer_id = %s;', (customer_id,))
            row = cur.fetchone()
            customer_name = row[0] + " " + row[1]
            
            # Execute the SQL query to fetch customer address by customer ID and assign details
            # Fetch address fields
            cur.execute('SELECT address_line1, address_line2, city, state, zip_code  FROM customers WHERE customer_id = %s;', (customer_id,))
            row = cur.fetchone()
            
            # Concatenate address fields to create a full shipping address
            # Check if address_line2 is None and format the address accordingly
            if row[1] is None:
                shipping_address = row[0] + ", " + row[2] + ", " + row[3] + " " + row[4]                
            else:
                shipping_address = row[0] + " " + row[1] + ", " + row[2] + ", " + row[3] + " " + row[4]
            
            # Execute the SQL query to fetch order items by order ID and assign details
            # Fetch book title and price
            cur.execute('SELECT book_id, quantity FROM order_items WHERE order_id = %s;', (order_id,))
            rows = cur.fetchall()
            
            order_list = []
            
            # For loop to iterate through each order item and fetch book details
            for row in rows:
                book_id = row[0]
                quantity = row[1]
                
                # Execute the SQL query to fetch book details by book ID and assign details
                # Fetch book title and price
                cur.execute('SELECT title, price FROM books WHERE book_id = %s;', (book_id,))
                new_row = cur.fetchone()
                title = new_row[0]
                price = new_row[1]
                
                # Create a dictionary for each order item
                order_list.append(
                    {
                        "title": title,
                        "quantity": quantity,
                        "price": price,
                        "subtotal": quantity * price
                    })
            
            # Create a dictionary to store order details             
            order = {
                "id": order_id,
                "customer_name": customer_name.title(),
                "shipping_address": shipping_address.title(),
                "total": total_amount,
                "created_at": order_date,
                "items": order_list
            }
            return order

def get_order_by_id(order_id):
    """
    Get DB connection and return order details by order ID.
    """
    # Get DB connection
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to fetch order details by order ID
            cur.execute('SELECT order_id, customer_id, order_date, total_amount FROM orders WHERE order_id = %s;', (order_id,))
            
            # Verify if the order exists by fetching the row
            row = cur.fetchone()
            
            # If row returns true, it means the order exists in the database and return the order details
            if row:
                return {
                    'order_id': row[0],
                    'customer_id': row[1],
                    'order_date': row[2],
                    'total_amount': row[3],
                }
                
    return None
        
