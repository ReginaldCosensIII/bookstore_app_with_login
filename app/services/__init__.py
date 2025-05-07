# bookstore_app_with_login/app/services/__init__.py

"""
Services Package Initialization.

This file makes the 'services' directory a Python package.
It can also be used to import service functions or classes
for easier access from other parts of the application, similar
to how __init__.py works in the 'models' package.
"""

# Import key service functions/classes if you want to access them directly
# from the package (e.g., from app.services import authenticate_user)
# This is optional and depends on our preferred import style.

# from .auth_service import authenticate_user, load_user, login_manager
# from .book_service import get_books_by_author, get_books_by_genre # Add other functions if needed
# from .order_service import create_order, get_confirmation_details
# from .reg_service import register_user, validate_registration, sanitize_form_input

# Example using __all__ if you prefer 'from app.services import *' (generally less recommended)
# __all__ = [
#     'authenticate_user', 'load_user', 'login_manager',
#     'get_books_by_author', 'get_books_by_genre',
#     'create_order', 'get_confirmation_details',
#     'register_user', 'validate_registration', 'sanitize_form_input'
# ]