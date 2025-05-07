# bookstore_app_with_login/app/models/__init__.py

"""
Models Package Initialization.

This file makes the 'models' directory a Python package.
It can also be used to conveniently import model classes
for easier access elsewhere in the application.

Example:
Instead of `from app.models.customer import Customer`, you could
potentially use `from app.models import Customer` if you import it here.
"""

# Import key model classes to make them available directly from the package
# (Optional, but can be convenient)
from app.models.customer import Customer
from app.models.book import Book
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.db import get_db_connection # Expose db connection function if needed directly

# You can define __all__ to specify what gets imported with 'from .models import *'
# Example: __all__ = ['Customer', 'Book', 'Order', 'OrderItem', 'get_db_connection']