# bookstore_app_with_login/app/models/order.py

from datetime import datetime
from decimal import Decimal # Use Decimal for monetary values
from logger import logger
from app.models.db import get_db_connection
from app.models.order_item import OrderItem
from app.models.book import Book # Needed to resolve item details

class Order:
    """
    Represents a customer order in the bookstore.

    Contains information about the customer, order date, total amount,
    and a list of items included in the order. Provides methods to
    save the order and its items to the database and retrieve order details.
    """
    def __init__(self, customer_id, total_amount, order_date=None, order_id=None, items=None):
        """
        Initializes an Order object.

        Args:
            customer_id (int): The ID of the customer placing the order.
            total_amount (Decimal or float): The total calculated amount for the order.
            order_date (datetime, optional): The date and time the order was placed.
                                            Defaults to the current UTC time if None.
            order_id (int, optional): The unique ID of the order (usually assigned by the DB).
                                      Defaults to None for new orders.
            items (list[OrderItem], optional): A list of OrderItem objects associated with this order.
                                               Defaults to an empty list.
        """
        self.order_id = order_id
        self.customer_id = customer_id
        # Ensure total_amount is stored as Decimal for precision
        self.total_amount = Decimal(total_amount) if total_amount is not None else Decimal('0.00')
        self.order_date = order_date or datetime.utcnow() # Default to current UTC time
        self.items = items or [] # Initialize with an empty list if None is provided

    def add_item(self, order_item: OrderItem):
        """
        Adds an OrderItem object to the order's item list.

        Args:
            order_item (OrderItem): The order item to add.
        """
        if not isinstance(order_item, OrderItem):
            raise TypeError("Can only add OrderItem objects to an order.")
        self.items.append(order_item)
        # Note: This does NOT recalculate total_amount. Recalculation should happen
        # before initializing the Order or within the service layer.

    def save(self, conn):
        """
        Saves the order header and all associated items to the database
        within a single transaction managed by the provided connection.

        Args:
            conn (psycopg2.connection): An active database connection. The caller
                                        is responsible for committing or rolling back.

        Returns:
            int: The generated order_id for the saved order.

        Raises:
            Exception: If saving the order header or any item fails.
        """
        if self.order_id is not None:
            logger.error(f"Attempted to save order which already has ID {self.order_id}.")
            raise ValueError("Cannot save an order that already has an ID.")
        if not self.items:
            logger.warning(f"Attempted to save order for customer {self.customer_id} with no items.")
            raise ValueError("Cannot save an order with no items.")

        try:
            with conn.cursor() as cur:
                # 1. Insert the order header
                cur.execute(
                    """
                    INSERT INTO orders (customer_id, order_date, total_amount)
                    VALUES (%s, %s, %s) RETURNING order_id;
                    """,
                    (self.customer_id, self.order_date, self.total_amount)
                )
                result = cur.fetchone()
                if not result or not result['order_id']:
                    raise Exception("Failed to create order header or retrieve order_id.")
                self.order_id = result['order_id'] # Assign the generated ID back to the object

                # 2. Insert each order item, linking it to the new order_id
                for item in self.items:
                    item.save(conn, self.order_id) # Call save on the OrderItem instance

            logger.info(f"Order {self.order_id} and its {len(self.items)} items saved successfully to DB (pending commit).")
            return self.order_id # Return the new order ID
        except Exception as e:
            logger.exception(f"Error saving order for customer {self.customer_id}: {e}")
            # The caller (service layer) should handle rollback
            raise # Re-raise the exception

    # --- Class Methods for Database Interaction ---

    @classmethod
    def from_db(cls, order_id, conn):
        """
        Loads an order and its associated items from the database using its ID.

        Args:
            order_id (int): The ID of the order to load.
            conn (psycopg2.connection): An active database connection.

        Returns:
            Order | None: An Order object instance if found, otherwise None.
        """
        try:
            order = None
            with conn.cursor() as cur:
                # 1. Load the main order details
                cur.execute(
                    """SELECT order_id, customer_id, order_date, total_amount
                       FROM orders WHERE order_id = %s;""",
                    (order_id,)
                )
                order_row = cur.fetchone()

                if not order_row:
                    logger.warning(f"Order with ID {order_id} not found in database.")
                    return None # Order doesn't exist

                # Create the Order object
                order = cls(
                    customer_id=order_row["customer_id"],
                    total_amount=order_row["total_amount"], # Should be Decimal from DB
                    order_date=order_row["order_date"],
                    order_id=order_row["order_id"]
                )

                # 2. Load the associated order items
                cur.execute(
                    """SELECT order_item_id, book_id, quantity
                       FROM order_items WHERE order_id = %s;""",
                    (order_id,)
                )
                item_rows = cur.fetchall()

                # Create OrderItem objects and add them to the order
                for item_row in item_rows:
                    order_item = OrderItem(
                        book_id=item_row["book_id"],
                        quantity=item_row["quantity"]
                    )
                    # Optionally store order_item_id if the OrderItem model needs it
                    # order_item.order_item_id = item_row["order_item_id"]
                    order.add_item(order_item)

            logger.info(f"Order {order_id} loaded successfully with {len(order.items)} items.")
            return order
        except Exception as e:
            logger.exception(f"Error loading order ID {order_id} from database: {e}")
            return None # Return None on error

    def to_dict(self, include_item_details=True):
        """
        Converts the Order object and optionally its items into a dictionary.

        Args:
            include_item_details (bool): If True, fetches details (title, price) for each
                                         book in the items list. Defaults to True.

        Returns:
            dict: A dictionary representation of the order.
        """
        order_data = {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            # Format datetime objects for serialization
            "order_date": self.order_date.isoformat() if self.order_date else None,
            # Ensure total amount is a string for JSON compatibility if needed, or float
            "total_amount": float(self.total_amount),
            "items": [] # Initialize items list
        }

        if include_item_details:
            item_details_list = []
            try:
                # Use a single connection for fetching all book details
                with get_db_connection() as conn:
                    for item in self.items:
                        # Fetch book details using the connection
                        book = Book.get_by_id(item.book_id) # Assuming Book.get_by_id handles its own connection/cursor
                        if book:
                            subtotal = book.price * item.quantity
                            item_details_list.append({
                                "book_id": book.book_id,
                                "title": book.title,
                                "price": float(book.price), # Convert Decimal to float for JSON
                                "quantity": item.quantity,
                                "subtotal": float(subtotal) # Convert Decimal to float for JSON
                            })
                        else:
                            logger.warning(f"Book ID {item.book_id} not found for order {self.order_id} item.")
                            # Optionally add placeholder or skip item
                            item_details_list.append({
                                "book_id": item.book_id,
                                "title": "Book Not Found",
                                "price": 0.0,
                                "quantity": item.quantity,
                                "subtotal": 0.0
                            })
                order_data["items"] = item_details_list
            except Exception as e:
                 logger.exception(f"Error fetching book details for order {self.order_id} items: {e}")
                 # Decide how to handle partial data: return what we have, or indicate error
                 order_data["items_error"] = "Could not retrieve full item details."
        else:
            # Just include basic item info (book_id, quantity) if details not requested
             order_data["items"] = [item.to_dict() for item in self.items]

        return order_data

    def __repr__(self):
        """String representation for debugging."""
        return f"<Order(id={self.order_id}, customer_id={self.customer_id}, items={len(self.items)}, total={self.total_amount})>"