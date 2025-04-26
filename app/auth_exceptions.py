# app/auth_exceptions.py

class AuthException(Exception):
    """Base class for all authentication-related exceptions."""
    pass


class InvalidCredentials(AuthException):
    """Raised when a user provides incorrect login information."""

    def __init__(self, details: str = "Invalid username or password."):
        self.message = details
        super().__init__(self.message)


class UserAlreadyExists(AuthException):
    """Raised when attempting to register a username that already exists."""

    def __init__(self, username: str):
        self.username = username
        self.message = f"The username '{username}' is already taken."
        super().__init__(self.message)


class UserNotFound(AuthException):
    """Raised when a user is not found in the database."""

    def __init__(self, username: str):
        self.username = username
        self.message = f"No user found with username '{username}'."
        super().__init__(self.message)


class RegistrationError(AuthException):
    """Raised when there is a general failure during registration."""

    def __init__(self, details: str = "There was an error during registration."):
        self.message = details
        super().__init__(self.message)


class PasswordMismatch(AuthException):
    """Raised when the password and confirmation do not match."""

    def __init__(self):
        self.message = "Passwords do not match."
        super().__init__(self.message)


class InvalidUsername(AuthException):
    """Raised when the username provided is invalid or doesn't meet criteria."""

    def __init__(self, reason: str = "Invalid username format."):
        self.message = reason
        super().__init__(self.message)
