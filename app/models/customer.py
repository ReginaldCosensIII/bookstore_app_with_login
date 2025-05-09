# bookstore_app_with_login/app/models/customer.py

from flask_login import UserMixin # Provides default implementations for Flask-Login
from logger import logger
from app.models.db import get_db_connection # Function to get DB connection

class Customer(UserMixin):
    """
    Represents a customer in the bookstore system.

    This class interfaces with the 'customers' table in the database
    using raw SQL queries via psycopg2. It includes methods for fetching,
    saving, and representing customer data, and integrates with Flask-Login.
    """
    def __init__(self, customer_id, name, email, phone_number, password,
                 created_at=None, first_name=None, last_name=None,
                 address_line1=None, address_line2=None, city=None, state=None, zip_code=None, role="customer"):
        """
        Initializes a Customer object.

        Args:
            customer_id (int): The unique ID of the customer. Can be None for new customers.
            name (str): The full name of the customer (might be deprecated if using first/last).
            email (str): The customer's email address (used for login).
            phone_number (str): The customer's phone number.
            password (str): The hashed password for the customer. NEVER store plain text.
            created_at (datetime, optional): Timestamp when the customer was created. Defaults to None.
            first_name (str, optional): Customer's first name. Defaults to None.
            last_name (str, optional): Customer's last name. Defaults to None.
            address_line1 (str, optional): First line of the shipping address. Defaults to None.
            address_line2 (str, optional): Second line of the shipping address. Defaults to None.
            city (str, optional): City of the shipping address. Defaults to None.
            state (str, optional): State (abbreviation) of the shipping address. Defaults to None.
            zip_code (str, optional): ZIP code of the shipping address. Defaults to None.
            role (str): A identifier indicating if the user is a Customer or Admin. Defaults to customer.
        """
        # --- Core Attributes ---
        self.customer_id = customer_id # Primary key
        self.email = email.lower().strip() if email else None # Normalize email
        self.phone_number = phone_number
        self.password = password # Hashed password
        self.created_at = created_at

        # --- Name Attributes (Prefer first/last over single 'name') ---
        self.first_name = first_name
        self.last_name = last_name
        # Fallback or combined name - adjust logic as needed
        self.name = name or f"{first_name or ''} {last_name or ''}".strip()

        # --- Address Attributes ---
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.role = role

    # --- Flask-Login required property ---
    @property
    def id(self):
        """
        Returns the unique identifier for the user, required by Flask-Login.
        Must return a string.
        """
        return str(self.customer_id)
    
        # --- Class Methods for Database Interaction ---

    @classmethod
    def from_row(cls, row_dict):
        """
        Factory method to create a Customer instance from a database row
        (obtained via DictCursor).

        Args:
            row_dict (dict): A dictionary representing a row from the 'customers' table.

        Returns:
            Customer | None: A Customer object if row_dict is valid, otherwise None.
        """
        if not row_dict:
            return None

        # Create and return a new Customer instance using data from the dictionary
        return cls(
            customer_id=row_dict.get("customer_id"),
            name=row_dict.get("name"), # Keep original name field if needed
            email=row_dict.get("email"),
            phone_number=row_dict.get("phone_number"),
            password=row_dict.get("password"), # Password hash
            created_at=row_dict.get("created_at"),
            first_name=row_dict.get("first_name"),
            last_name=row_dict.get("last_name"),
            address_line1=row_dict.get("address_line1"),
            address_line2=row_dict.get("address_line2"),
            city=row_dict.get("city"),
            state=row_dict.get("state"),
            zip_code=row_dict.get("zip_code"),
            role=row_dict.get("role")
        )

    @classmethod
    def get_by_id(cls, customer_id):
        """
        Fetches a customer from the database by their unique customer_id.

        Args:
            customer_id (int): The ID of the customer to retrieve.

        Returns:
            Customer | None: A Customer object if found, otherwise None.
        """
        query = "SELECT * FROM customers WHERE customer_id = %s"
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (customer_id,))
                    row = cur.fetchone() # Returns dict or None
            customer = cls.from_row(row)
            if customer:
                 logger.debug(f"Customer found for ID: {customer_id}")
            else:
                 logger.warning(f"No customer found for ID: {customer_id}")
            return customer
        except Exception as e:
            logger.exception(f"Error fetching customer by ID {customer_id}: {e}")
            return None # Return None on database error

    @classmethod
    def get_by_email(cls, email):
        """
        Fetches a customer from the database by their email address.
        Email comparison should be case-insensitive.

        Args:
            email (str): The email address to search for.

        Returns:
            Customer | None: A Customer object if found, otherwise None.
        """
        if not email:
            return None
        normalized_email = email.lower().strip() # Normalize before querying

        query = "SELECT * FROM customers WHERE lower(email) = %s"
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (normalized_email,))
                    row = cur.fetchone()
            customer = cls.from_row(row)
            if customer:
                logger.debug(f"Customer found for email: {normalized_email}")
            else:
                logger.warning(f"No customer found for email: {normalized_email}")
            return customer
        except Exception as e:
            logger.exception(f"Error fetching customer by email {normalized_email}: {e}")
            return None # Return None on database error

    # --- Instance Methods ---

    def save_to_db(self):
        """
        Inserts a new customer record into the database.
        Assumes `self.customer_id` is None before saving.
        Updates `self.customer_id` with the ID generated by the database.

        Raises:
            Exception: If the database insertion fails.
        """
        if self.customer_id is not None:
            logger.error(f"Attempted to save customer {self.email} which already has ID {self.customer_id}.")
            raise ValueError("Cannot save a customer that already has an ID. Use an update method instead.")

        insert_query = """
            INSERT INTO customers (name, email, phone_number, password,
                                   first_name, last_name, address_line1, address_line2,
                                   city, state, zip_code, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING customer_id;
        """
        # Combine first/last name if 'name' wasn't explicitly provided
        calculated_name = self.name or f"{self.first_name or ''} {self.last_name or ''}".strip()

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(insert_query, (
                        calculated_name, self.email, self.phone_number, self.password,
                        self.first_name, self.last_name,
                        self.address_line1, self.address_line2, self.city,
                        self.state, self.zip_code
                    ))
                    # Fetch the newly generated customer_id
                    result = cur.fetchone()
                    if result and result['customer_id']:
                        self.customer_id = result['customer_id']
                        logger.info(f"Customer '{self.email}' saved successfully with ID {self.customer_id}")
                    else:
                        # This case should ideally not happen with RETURNING clause if insert worked
                        raise Exception("Failed to retrieve customer_id after insert.")
                conn.commit() # Commit the transaction
        except Exception as e:
            logger.exception(f"Error saving customer '{self.email}' to database: {e}")
            # Consider rolling back if part of a larger transaction elsewhere
            raise # Re-raise the exception

    def get_full_name(self):
        """
        Returns the customer's full name, prioritizing first and last names.
        """
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()
        return self.name # Fallback to the 'name' field if first/last are empty

    def get_single_line_address(self):
        """
        Returns a formatted single-line address suitable for display.
        Handles optional address line 2.
        """
        parts = [
            self.address_line1,
            self.address_line2, # Include only if it exists
            self.city,
            self.state,
            self.zip_code
        ]
        # Filter out None or empty strings and join with ", "
        return ', '.join(filter(None, parts))

    def to_dict(self):
        """
        Converts the Customer object attributes into a dictionary.
        Useful for serialization (e.g., to JSON) but excludes the password hash.
        """
        return {
            "customer_id": self.customer_id,
            "name": self.get_full_name(), # Use the combined name
            "email": self.email,
            "phone_number": self.phone_number,            
            "created_at": self.created_at, # Format datetime
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address_line1": self.address_line1,
            "address_line2": self.address_line2,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "role": self.role
        }

    def __repr__(self):
        """String representation for debugging purposes."""
        return f"<Customer(id={self.customer_id}, email='{self.email}')>"