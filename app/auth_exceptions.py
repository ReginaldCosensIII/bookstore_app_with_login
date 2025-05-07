# bookstore_app_with_login/app/auth_exceptions.py

"""
Custom Exception classes for Authentication and Registration specific errors.

Using custom exceptions allows for more specific error handling in routes
and services, improving clarity and control flow compared to generic Exceptions.
"""

class AuthException(Exception):
    """Base class for all authentication and registration related exceptions."""
    # You could add common attributes or methods here if needed later.
    pass


class InvalidCredentials(AuthException):
    """Raised when a user provides an incorrect email or password during login."""
    def __init__(self, message: str = "Invalid email or password."):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExists(AuthException):
    """Raised during registration when the provided email already exists in the database."""
    def __init__(self, email: str):
        self.email = email
        # Provide a clear message indicating the conflict.
        self.message = f"The email address '{email}' is already registered."
        super().__init__(self.message)


class UserNotFound(AuthException):
    """Raised when an operation attempts to find a user (e.g., by email or ID) but fails."""
    # Note: Often handled by returning None from service/model methods, but can be
    # useful if an operation *expects* a user to exist.
    def __init__(self, identifier: str, identifier_type: str = "email"):
        self.identifier = identifier
        self.identifier_type = identifier_type
        self.message = f"No user found with {self.identifier_type} '{self.identifier}'."
        super().__init__(self.message)


class RegistrationError(AuthException):
    """Raised for general failures during the registration process not covered by other exceptions."""
    def __init__(self, details: str = "An error occurred during registration."):
        self.message = details
        super().__init__(self.message)


class PasswordMismatch(AuthException):
    """Raised during registration or password change if the password and confirmation do not match."""
    def __init__(self, message: str = "Password and confirmation password do not match."):
        self.message = message
        super().__init__(self.message)

class PasswordPolicyViolation(AuthException):
     """Raised if the provided password does not meet the defined strength requirements."""
     def __init__(self, message: str = "Password does not meet security requirements."):
         self.message = message
         super().__init__(self.message)


class InvalidInputFormat(AuthException):
    """Raised for general input format violations during registration or login."""
    def __init__(self, field: str, reason: str):
        self.field = field
        self.reason = reason
        self.message = f"Invalid format for field '{field}': {reason}"
        super().__init__(self.message)