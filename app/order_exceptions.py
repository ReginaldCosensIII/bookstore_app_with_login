# bookstore_app_with_login/app/order_exceptions.py

"""
Custom Exception classes for Order Processing specific errors.

These help differentiate between various issues that can occur during
order creation, validation, or retrieval.
"""

class OrderException(Exception):
    """Base class for all order-related exceptions."""
    pass


class QuantityExceedsStock(OrderException):
    """
    Raised during order validation when the requested quantity
    for a specific book exceeds the available stock.
    """
    def __init__(self, book_title: str, requested: int, available: int):
        """
        Initializes the exception with details about the stock issue.

        Args:
            book_title (str): The title of the book with insufficient stock.
            requested (int): The quantity the customer tried to order.
            available (int): The actual quantity available in stock.
        """
        self.book_title = book_title
        self.requested = requested
        self.available = available
        # User-friendly message detailing the specific stock issue.
        self.message = (
            f"Cannot order {requested} copies of '{book_title}'. "
            f"Only {available} available in stock."
        )
        super().__init__(self.message)


class InvalidOrderFormat(OrderException):
    """
    Raised when the structure or content of the order data
    (e.g., the list of items, customer ID) is invalid or improperly formatted.
    """
    def __init__(self, details: str = "The submitted order data is invalid or incomplete."):
        """
        Initializes the exception with specific details about the format error.

        Args:
            details (str): A description of why the order format is invalid.
        """
        self.message = details
        super().__init__(self.message)


class OrderCreationError(OrderException):
    """
    Raised for general, non-specific issues encountered during the order creation process
    that aren't covered by more specific exceptions like stock or format errors.
    (Consider if DatabaseOperationError is often more appropriate).
    """
    def __init__(self, details: str = "An unexpected issue occurred while creating your order."):
        """
        Initializes the exception with details about the creation failure.

        Args:
            details (str): A description of the problem encountered.
        """
        self.message = details
        super().__init__(self.message)


class DatabaseOperationError(OrderException):
    """
    Raised specifically when a database operation (INSERT, UPDATE, SELECT) fails
    during the order processing workflow (e.g., saving the order, updating stock).
    It's helpful to wrap the original database exception.
    """
    def __init__(self, operation_description: str, original_exception: Exception | None = None):
        """
        Initializes the exception with details about the failed DB operation.

        Args:
            operation_description (str): A brief description of what DB operation failed
                                         (e.g., "saving order header", "updating stock").
            original_exception (Exception | None): The original exception raised by the
                                                   database driver (e.g., psycopg2.Error), if available.
        """
        self.operation_description = operation_description
        self.original_exception = original_exception
        # Construct a message including the original error if available.
        if original_exception:
            self.message = (
                f"Database error during '{operation_description}': {type(original_exception).__name__} - {str(original_exception)}"
            )
        else:
             self.message = f"A database error occurred during '{operation_description}'."

        super().__init__(self.message)


class OrderNotFound(OrderException):
    """Raised when attempting to retrieve an order (e.g., for confirmation) that does not exist."""
    def __init__(self, order_id: int):
        """
        Initializes the exception with the ID of the order that wasn't found.

        Args:
            order_id (int): The ID of the order.
        """
        self.order_id = order_id
        self.message = f"Order with ID {order_id} was not found."
        super().__init__(self.message)