# bookstore_app_with_login/app/models/order_item.py

from logger import logger # Import the custom logger

class OrderItem:
    """
    Represents a single item line within a customer order.

    Links a specific book (by book_id) and quantity to an order (by order_id).
    """
    def __init__(self, book_id, quantity, order_item_id=None, order_id=None):
        """
        Initializes an OrderItem object.

        Args:
            book_id (int): The ID of the book being ordered.
            quantity (int): The number of copies of the book being ordered.
            order_item_id (int, optional): The unique ID for this specific order item line
                                           (usually assigned by the database). Defaults to None.
            order_id (int, optional): The ID of the order this item belongs to.
                                      Often set after the OrderItem is saved. Defaults to None.
        """
        if not isinstance(book_id, int) or book_id <= 0:
            raise ValueError("OrderItem requires a valid positive integer book_id.")
        if not isinstance(quantity, int) or quantity <= 0:
             raise ValueError("OrderItem requires a valid positive integer quantity.")

        self.order_item_id = order_item_id # Primary key for the order_items table (optional here)
        self.book_id = book_id
        self.quantity = quantity
        self.order_id = order_id # Foreign key linking to the orders table

    def save(self, conn, order_id):
        """
        Inserts this order item into the 'order_items' table using an
        existing database connection and the parent order's ID.

        Args:
            conn (psycopg2.connection): An active database connection.
            order_id (int): The ID of the order this item belongs to.

        Raises:
            Exception: If the database insertion fails.
        """
        if self.order_item_id is not None:
            # This prevents accidentally trying to re-insert an item that might already exist
            # Although usually, OrderItems are created and saved once per order creation.
            logger.warning(f"Attempted to save OrderItem for book {self.book_id} which may already have an ID.")
            # Depending on logic, you might allow updates or raise an error.
            # For simple order creation, raising might be safer if this state is unexpected.
            # raise ValueError("Cannot re-save an OrderItem that might already exist in DB.")

        self.order_id = order_id # Ensure the order_id is set on the instance

        try:
            with conn.cursor() as cur:
                # Execute the insert statement for the order item
                cur.execute(
                    """INSERT INTO order_items (order_id, book_id, quantity)
                       VALUES (%s, %s, %s) RETURNING order_item_id;""", # Optionally return the new PK
                    (self.order_id, self.book_id, self.quantity)
                )
                # Optionally capture the returned order_item_id
                result = cur.fetchone()
                if result and result['order_item_id']:
                     self.order_item_id = result['order_item_id']
                     logger.debug(f"OrderItem for book {self.book_id} (qty: {self.quantity}) saved with ID {self.order_item_id} for order {self.order_id}.")
                else:
                     # This shouldn't happen with RETURNING if insert worked, but good to check
                     raise Exception(f"Failed to retrieve order_item_id after inserting item for book {self.book_id}.")

                # Commit is handled by the caller (typically the Order.save method or service layer)

        except Exception as e:
            logger.exception(f"Error saving OrderItem for book {self.book_id}, order {self.order_id}: {e}")
            # Rollback should be handled by the caller
            raise # Re-raise the exception

    def to_dict(self):
        """
        Converts the OrderItem object attributes into a dictionary.
        Useful for serialization or debugging.
        """
        item_dict = {
            "order_item_id": self.order_item_id, # May be None if not saved/retrieved yet
            "order_id": self.order_id,           # May be None if not saved yet
            "book_id": self.book_id,
            "quantity": self.quantity
            # Note: Does not include book title or price, as those belong to the Book model.
            # These details are typically joined or fetched separately when needed for display.
        }
        return item_dict

    def __repr__(self):
        """String representation for debugging."""
        return f"<OrderItem(order_id={self.order_id}, book_id={self.book_id}, qty={self.quantity})>"