# bookstore_app_with_login/app/services/order_service.py

import json # For potentially handling JSON input if needed differently
from logger import logger
from datetime import datetime
from app.models.book import Book
from app.models.order import Order
from app.models.customer import Customer # Needed for getting customer details
from app.models.order_item import OrderItem
from app.models.db import get_db_connection
from decimal import Decimal, InvalidOperation # Use Decimal for accurate money calculations
from app.order_exceptions import QuantityExceedsStock, InvalidOrderFormat, DatabaseOperationError # Custom DB error during order processing

# It seems OrderCreationError isn't explicitly raised, consider removing if unused
# from app.order_exceptions import OrderCreationError

def create_order(customer_id, items_data, total_amount_from_form):
    """
    Creates a new order, validates items, saves to the database, and updates stock.

    Handles the entire order creation workflow within a database transaction.

    Args:
        customer_id (int): The ID of the customer placing the order.
        items_data (list[dict]): A list of dictionaries, where each dict represents an item
                                 and should contain 'book_id' and 'quantity'.
                                 Example: [{'book_id': 1, 'quantity': 2}, ...]
        total_amount_from_form (float): The total amount calculated on the frontend (for verification).

    Returns:
        dict: A dictionary containing:
              {'success': True, 'order_id': new_order_id} on success.
              {'success': False, 'message': error_message} on failure due to validation
              or stock issues (before database operations start).

    Raises:
        DatabaseOperationError: If a database error occurs during the save process.
        ValueError: If input data types are incorrect (should be caught earlier ideally).
    """
    logger.info(f"Attempting to create order for customer_id: {customer_id} with items: {items_data}")

    # --- Input Validation ---
    if not customer_id or not isinstance(customer_id, int):
        logger.error("Order creation failed: Invalid or missing customer_id.")
        # Raising InvalidOrderFormat here might be caught by the generic Exception handler later.
        # Returning a dict is clearer for flow control in the route.
        # Consider standardizing return format or exception usage.
        raise InvalidOrderFormat("Invalid customer ID provided.")

    if not items_data or not isinstance(items_data, list) or len(items_data) == 0:
        logger.error("Order creation failed: Items data is missing, not a list, or empty.")
        raise InvalidOrderFormat("Order must contain at least one item.")

    # --- Transactional Processing ---
    conn = None # Initialize connection variable
    try:
        conn = get_db_connection() # Get a connection for the transaction
        calculated_total_price = Decimal('0.00') # Use Decimal for calculation
        order_items_to_create = [] # List to hold validated OrderItem objects

        # --- Item Validation and Calculation (within the 'try' block, before DB writes) ---
        for item_dict in items_data:
            book_id = item_dict.get("book_id")
            quantity = item_dict.get("quantity")

            # Validate item structure and types
            if not isinstance(book_id, int) or not isinstance(quantity, int) or quantity <= 0:
                raise InvalidOrderFormat(f"Invalid data for item: book_id={book_id}, quantity={quantity}.")

            # Fetch the book details (use the connection context if model methods require it)
            # Assuming Book.get_by_id handles its own connection/cursor or can accept one
            book = Book.get_by_id(book_id) # Fetch within the transaction scope potentially
            if not book:
                raise InvalidOrderFormat(f"Book with ID {book_id} not found.")

            # Check stock availability
            if not book.has_stock(quantity):
                 # Raise specific exception for stock issues
                raise QuantityExceedsStock(book.title, quantity, book.stock_quantity)

            # Calculate item subtotal and add to total
            item_price = book.price * quantity # Decimal arithmetic
            calculated_total_price += item_price

            # Create OrderItem object (without saving yet)
            order_items_to_create.append(OrderItem(book_id=book.book_id, quantity=quantity))

        # --- Verification (Optional but Recommended) ---
        # Compare calculated total with the total received from the form
        try:
             form_total_decimal = Decimal(total_amount_from_form)
             # Use is_close for floating point comparison robustness if needed, or exact match for Decimal
             if calculated_total_price != form_total_decimal:
                 logger.warning(f"Order total mismatch for customer {customer_id}. Calculated: {calculated_total_price}, Form: {form_total_decimal}. Proceeding with calculated total.")
                 # Decide whether to proceed, raise error, or just log
                 # For now, we proceed using the server-calculated total.
        except (InvalidOperation, TypeError):
             logger.error(f"Invalid total amount received from form for customer {customer_id}: {total_amount_from_form}")
             raise InvalidOrderFormat("Invalid total amount format received.")


        # --- Database Operations (Order and Stock Update) ---

        # Create the Order object (header)
        order_header = Order(
            customer_id=customer_id,
            total_amount=calculated_total_price # Use server-calculated total
            # items list will be populated by adding OrderItem instances
        )
        # Add validated OrderItem objects to the order header
        for oi in order_items_to_create:
            order_header.add_item(oi)

        # Save the order header and all items (this handles inserts)
        # The Order.save method should handle inserting items via OrderItem.save
        new_order_id = order_header.save(conn) # Pass the connection

        # Decrease stock for each book AFTER order and items are successfully inserted
        for item in order_items_to_create:
            # Re-fetch book within the same transaction context might be safer if stock could change,
            # but decreases atomicity. Assuming stock check earlier is sufficient for this operation.
            # OR, pass 'conn' to decrease_stock if it needs the cursor.
             book_to_update = Book.get_by_id(item.book_id) # Fetch again or use previously fetched 'book' if safe
             if book_to_update:
                 book_to_update.decrease_stock(item.quantity, conn) # Pass the connection
             else:
                 # This case implies book was deleted between validation and stock update - very unlikely but possible
                 raise DatabaseOperationError(f"Book {item.book_id} disappeared during order processing.")


        # --- Commit Transaction ---
        conn.commit()
        logger.info(f"Order {new_order_id} created and committed successfully for customer {customer_id}.")

        # Return success indicator and the new order ID
        return {"success": True, "order_id": new_order_id}

    except (InvalidOrderFormat, QuantityExceedsStock) as e:
        # Handle validation/stock errors: Log, rollback, return failure
        logger.warning(f"Order creation failed for customer {customer_id} due to validation/stock issue: {e}")
        if conn:
            conn.rollback() # Rollback any partial changes if validation failed mid-process
        # Re-raise the specific exception to be caught by the route
        raise e

    except Exception as e:
        # Handle unexpected database or other errors
        logger.exception(f"Unexpected error during order creation for customer {customer_id}: {e}")
        if conn:
            conn.rollback() # Rollback the transaction on any error
        # Raise a generic DB error for the route to handle
        raise DatabaseOperationError(f"An internal error occurred while processing the order: {e}")

    finally:
        # Ensure the database connection is closed
        if conn:
            conn.close()
            logger.debug("Database connection closed for create_order.")

def get_confirmation_details(order_id, conn):
    """
    Retrieves detailed information for an order confirmation page.

    Fetches the order, its items (including book details like title/price),
    and customer information (name, address).

    Args:
        order_id (int): The ID of the order to retrieve details for.
        conn (psycopg2.connection): An active database connection.

    Returns:
        dict | None: A dictionary containing structured order details suitable for
                     the confirmation template, or None if the order is not found.
                     Example structure:
                     {
                         "id": 123,
                         "customer_name": "Jane Doe",
                         "shipping_address": "123 Main St, Anytown, CA 90210",
                         "total": Decimal('59.97'),
                         "created_at": "2024-01-15T10:30:00",
                         "items": [
                             {"book_id": 1, "title": "The Great Novel", "price": 19.99, "quantity": 1, "subtotal": 19.99},
                             {"book_id": 5, "title": "Another Story", "price": 9.99, "quantity": 4, "subtotal": 39.96}
                         ]
                     }
    """
    logger.info(f"Fetching confirmation details for Order ID: {order_id}")
    try:
        # 1. Load the Order object and its basic items from the DB
        # The `from_db` method should handle joining/fetching necessary item data.
        order = Order.from_db(order_id, conn)

        if not order:
            logger.warning(f"Attempted to get confirmation details for non-existent Order ID: {order_id}")
            return None # Order not found

        order_dict = order.to_dict()
        order_items = order_dict.get("items", [])
        
        # 2. Fetch Customer details associated with the order
        customer = Customer.get_by_id(order.customer_id) # Assumes get_by_id uses its own connection or accepts `conn`
        if not customer:
            logger.error(f"Customer data not found for Customer ID {order.customer_id} associated with Order ID {order_id}.")
            # Decide how to handle missing customer: return None, or return partial order data?
            # Returning None might be safer.
            return None

        # 3. Prepare the dictionary for the template, enriching item data
        order_details = {
            "id": order.order_id,
            "customer_name": customer.get_full_name().title(), # Get formatted name
            "shipping_address": customer.get_single_line_address().title(), # Get formatted address
            "total": order.total_amount, # Keep as Decimal or convert as needed
            "created_at": order.order_date.isoformat(), # Format date
            "items": order_items
        }

        logger.info(f"Successfully retrieved confirmation details for Order ID: {order_id}")
        return order_details

    except Exception as e:
        logger.exception(f"Error retrieving confirmation details for Order ID {order_id}: {e}")
        # Don't expose internal errors directly, return None or raise a custom exception
        return None

