from flask_login import UserMixin
from logger import logger # Importing custom logger for logging

class Customer(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

        logger.debug(f"Customer object initialized with ID: {self.id} and Email: {self.email}")

    # Flask-Login integration
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
