# app/models/customer.py
from flask_login import UserMixin
from logger import logger # Importing custom logger for logging
from app.extensions import db # Importing the SQLAlchemy instance from extensions.py

class Customer(UserMixin, db.Model):
    """
    Model representing a customer in the database.
    Inherits from UserMixin for Flask-Login integration.
    """
    # This class represents the customers table in the database.
    __tablename__ = 'customers'

    # Define the columns for the customers table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        """
        Returns a string representation of the Customer object.
        This is useful for debugging and logging purposes.
        """
        # Using f-string for better readability and performance
        return f"<Customer {self.username}>"
