# bookstore_app_with_login/app/models/book.py

from app.models.db import get_db_connection
from logger import logger # Import the custom logger
from decimal import Decimal # Use Decimal for precise price representation

class Book:
    """
    Represents a book entity in the bookstore.

    Provides methods for CRUD operations (Create, Read, Update, Delete - though Delete isn't implemented yet)
    and stock management related to books in the database.
    """
    def __init__(self, book_id, title, author, genre, price, stock_quantity, description="This is a placeholder description."):
        """
        Initializes a Book object.

        Args:
            book_id (int): The unique identifier for the book.
            title (str): The title of the book.
            author (str): The author of the book.
            genre (str): The genre of the book.
            price (Decimal): The price of the book. Stored as Decimal for accuracy.
            stock_quantity (int): The current number of copies in stock.
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        # Ensure price is stored/handled as Decimal for financial calculations
        self.price = Decimal(price) if price is not None else None
        self.stock_quantity = int(stock_quantity) if stock_quantity is not None else 0
        self.description = description
        
    def get_id(self):
        """Returns the book's unique ID."""
        return self.book_id

    def has_stock(self, quantity_needed):
        """
        Checks if there is enough stock for the requested quantity.

        Args:
            quantity_needed (int): The number of copies requested.

        Returns:
            bool: True if stock_quantity >= quantity_needed, False otherwise.
        """
        return self.stock_quantity >= quantity_needed

    def increase_stock(self, quantity, conn):
        """
        Increases the stock quantity of the book in the database within a transaction.

        Args:
            quantity (int): The amount to increase the stock by.
            conn (psycopg2.connection): An active database connection.
        """
        if quantity <= 0:
            logger.warning(f"Attempted to increase stock for book {self.book_id} by non-positive amount: {quantity}")
            return # Or raise ValueError("Quantity must be positive")

        self.stock_quantity += quantity
        try:
            with conn.cursor() as cur:
                cur.execute(
                    'UPDATE books SET stock_quantity = %s WHERE book_id = %s',
                    (self.stock_quantity, self.book_id)
                )
            # Commit should happen outside this method, typically at the end of the service operation
            logger.debug(f"Stock for book {self.book_id} tentatively increased by {quantity} to {self.stock_quantity}.")
        except Exception as e:
            logger.exception(f"Failed to update stock (increase) for book {self.book_id} in database: {e}")
            # Rollback might be needed at a higher level
            raise # Re-raise the exception

    def decrease_stock(self, quantity, conn):
        """
        Decreases the stock quantity of the book in the database within a transaction.

        Args:
            quantity (int): The amount to decrease the stock by.
            conn (psycopg2.connection): An active database connection.

        Raises:
            ValueError: If the requested quantity exceeds available stock or is non-positive.
        """
        if quantity <= 0:
            logger.warning(f"Attempted to decrease stock for book {self.book_id} by non-positive amount: {quantity}")
            raise ValueError("Quantity to decrease must be positive.")
        if self.stock_quantity < quantity:
            logger.error(f"Not enough stock for book {self.book_id}. Available: {self.stock_quantity}, Requested: {quantity}")
            raise ValueError(f"Not enough stock for book '{self.title}'. Available: {self.stock_quantity}.")

        self.stock_quantity -= quantity
        try:
            with conn.cursor() as cur:
                cur.execute(
                    'UPDATE books SET stock_quantity = %s WHERE book_id = %s',
                    (self.stock_quantity, self.book_id)
                )
            # Commit should happen outside this method
            logger.debug(f"Stock for book {self.book_id} tentatively decreased by {quantity} to {self.stock_quantity}.")
        except Exception as e:
            logger.exception(f"Failed to update stock (decrease) for book {self.book_id} in database: {e}")
            # Rollback might be needed at a higher level
            raise # Re-raise the exception

    # --- Class Methods for Database Interaction ---

    @classmethod
    def add_book(cls, title, author, genre, price, stock_quantity, description="This is a placeholder description."):
        """
        Adds a new book record to the database.

        Args:
            title (str): Book title.
            author (str): Book author.
            genre (str): Book genre.
            price (Decimal or float): Book price.
            stock_quantity (int): Initial stock quantity.

        Returns:
            Book: An instance of the newly created Book object.

        Raises:
            Exception: If the database insertion fails.
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """INSERT INTO books (title, author, genre, price, stock_quantity, description)
                           VALUES (%s, %s, %s, %s, %s, %s) RETURNING book_id""",
                        (title, author, genre, Decimal(price), int(stock_quantity), description)
                    )
                    book_id = cur.fetchone()[0] # Fetch the returned book_id
                conn.commit() # Commit the transaction
            logger.info(f"Book '{title}' added successfully with ID: {book_id}.")
            # Return a new instance of the Book class
            return cls(book_id, title, author, genre, price, stock_quantity)
        except Exception as e:
            logger.exception(f"Error adding book '{title}' to database: {e}")
            raise # Re-raise the exception

    @classmethod
    def get_by_id(cls, book_id):
        """
        Fetches a single book from the database by its primary key (book_id).

        Args:
            book_id (int): The ID of the book to retrieve.

        Returns:
            Book | None: A Book object instance if found, otherwise None.
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT * FROM books WHERE book_id = %s', (book_id,))
                    book_data = cur.fetchone() # fetchone() returns one row or None

            if book_data:
                logger.debug(f"Book found for ID: {book_id}")
                # Create and return a Book instance from the fetched data
                return cls(
                    book_id=book_data["book_id"],
                    title=book_data["title"],
                    author=book_data["author"],
                    genre=book_data["genre"],
                    price=book_data["price"], # Already Decimal from DB if type is NUMERIC
                    stock_quantity=book_data["stock_quantity"],
                    description=book_data["description"]
                )
            else:
                logger.warning(f"No book found for ID: {book_id}")
                return None
        except Exception as e:
            logger.exception(f"Error fetching book by ID {book_id}: {e}")
            return None # Return None on error

    @classmethod
    def get_all_books(cls):
        """
        Fetches all book records from the database.

        Returns:
            list[Book]: A list of Book object instances. Returns an empty list if no books
                        are found or an error occurs.
        """
        books_list = []
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT * FROM books ORDER BY title') # Optional: Order results
                    all_book_data = cur.fetchall() # fetchall() returns a list of rows

            # Convert each row into a Book object
            for book_data in all_book_data:
                books_list.append(cls(
                    book_id=book_data["book_id"],
                    title=book_data["title"],
                    author=book_data["author"],
                    genre=book_data["genre"],
                    price=book_data["price"],
                    stock_quantity=book_data["stock_quantity"],
                    description=book_data["description"]
                ))
            logger.info(f"Retrieved {len(books_list)} books from database.")
        except Exception as e:
            logger.exception("Error fetching all books from database.")
            # Return empty list on error, or could re-raise
        return books_list

    def to_dict(self, include_book_description=True):
        """
        Converts the Book object and optionally its description into a dictionary.

        Args:
            include_book_description (bool): If True, book description is included. Defaults to True.

        Returns:
            dict: A dictionary representation of the book.
        """
        book_data = {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "price": self.price, # Already Decimal from DB if type is NUMERIC
            "stock_quantity": self.stock_quantity,
        }
        
        if include_book_description:
            book_data["description"] = self.description
            
        return book_data

    def update_book(self, title=None, author=None, genre=None, price=None, stock_quantity=None, description=None):
        """
        Updates the details of this book instance in the database.
        Only updates fields that are provided (not None).

        Args:
            title (str, optional): New title.
            author (str, optional): New author.
            genre (str, optional): New genre.
            price (Decimal or float, optional): New price.
            stock_quantity (int, optional): New stock quantity.

        Returns:
            Book: The updated Book instance (self).

        Raises:
            ValueError: If price or stock_quantity are invalid types.
            Exception: If the database update fails.
        """
        fields_to_update = {}
        if title is not None: fields_to_update['title'] = title
        if author is not None: fields_to_update['author'] = author
        if genre is not None: fields_to_update['genre'] = genre
        if price is not None: fields_to_update['price'] = Decimal(price) # Ensure Decimal
        if stock_quantity is not None: fields_to_update['stock_quantity'] = int(stock_quantity)
        if description is not None: fields_to_update['description'] = description

        if not fields_to_update:
            logger.info(f"No fields provided to update for book {self.book_id}.")
            return self # No changes needed

        # Construct the SET part of the SQL query dynamically
        set_clause = ", ".join([f"{field} = %s" for field in fields_to_update])
        query = f"UPDATE books SET {set_clause} WHERE book_id = %s"
        values = list(fields_to_update.values()) + [self.book_id]

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, tuple(values))
                conn.commit()

            # Update the instance attributes after successful DB update
            for field, value in fields_to_update.items():
                setattr(self, field, value)

            logger.info(f"Book {self.book_id} updated successfully. Fields changed: {list(fields_to_update.keys())}")
            return self
        except Exception as e:
            logger.exception(f"Error updating book {self.book_id}: {e}")
            raise # Re-raise the exception

    def __repr__(self):
        """String representation for debugging."""
        return f"<Book(id={self.book_id}, title='{self.title}', stock={self.stock_quantity})>"