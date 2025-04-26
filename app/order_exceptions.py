#app/order_exceptions.py

class OrderException(Exception):
    """Base class for all order-related exceptions."""
    pass


class QuantityExceedsStock(OrderException):
    """Raised when the requested quantity exceeds available stock."""

    def __init__(self, book_title: str, requested: int, available: int):
        self.book_title = book_title
        self.requested = requested
        self.available = available
        self.message = (
            f"You requested {requested} copies of '{book_title}', "
            f"but only {available} are in stock."
        )
        super().__init__(self.message)

class InvalidOrderFormat(OrderException):
    """Raised when the order item data is invalid or improperly formatted."""

    def __init__(self, details: str = "The order data is invalid."):
        self.message = details
        super().__init__(self.message)


class OrderCreationError(OrderException):
    """Raised for general issues during order creation."""

    def __init__(self, details: str = "There was an issue creating your order."):
        self.message = details
        super().__init__(self.message)


class DatabaseOperationError(OrderException):
    """Raised when a database operation fails during order processing."""

    def __init__(self, operation: str, original_exception: Exception):
        self.operation = operation
        self.original_exception = original_exception
        self.message = (
            f"Database operation '{operation}' failed: {str(original_exception)}"
        )
        super().__init__(self.message)
