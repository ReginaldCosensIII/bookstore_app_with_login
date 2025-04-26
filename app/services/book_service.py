# app/services/book_service.py
from app.models.book import Book
from app.models.db import get_db_connection

def get_all_books():
    """Returns all the books from the database.
    """    
    # Get a connection to the database
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to fetch all books
            cur.execute('SELECT book_id, title, author, price, stock_quantity, genre FROM books;')
            
            # Verify by fetching all the rows returned by the query
            rows = cur.fetchall()

        # Initialize an empty list to store the books
        books = []
        
        # For loop to iterate through the rows and create a list of dictionaries for each book
        for row in rows:
            books.append({
                'book_id': row[0],
                'title': row[1],
                'author': row[2],
                'price': row[3],
                'stock_quantity': row[4],
                'genre': row[5],
            })

    return books

def get_books_by_author(author):
    """
    Returns all the books by a specific author from the database.
    """
    # Get a connection to the database
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to fetch books by author
            cur.execute('SELECT book_id, title, author, price, stock_quantity FROM books WHERE author = %s;', (author,))
            
            # Verify by fetching all the rows returned by the query
            rows = cur.fetchall()
            
            # Initialize an empty list to store the books
            books = []
            
            # For loop to iterate through the rows and create a list of dictionaries for each book
            for row in rows:
                books.append({
                    'book_id': row[0],
                    'title': row[1],
                    'author': row[2],
                    'price': row[3],
                    'stock_quantity': row[4],
                })
                
    return books

def get_book_by_id(book_id):
    """
    Returns a single book by its ID from the database.
    """
    # Get a connection to the database
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to fetch a book by its ID
            cur.execute('SELECT book_id, title, author, price, stock_quantity, genre FROM books WHERE book_id = %s;', (book_id,))
            
            # Verify by fetching the row returned by the query
            row = cur.fetchone()
            
            # If a row returns True, return a dictionary for the book
            if row:
                return {
                    'book_id': row[0],
                    'title': row[1],
                    'author': row[2],
                    'price': row[3],
                    'stock_quantity': row[4],
                    'genre': row[5],
                }
                
    return None

def get_books_by_genre(genre):
    """
    Returns all the books of a specific genre from the database.
    """
    # Get a connection to the database
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to fetch books by genre
            cur.execute('SELECT book_id, title, author, price, stock_quantity FROM books WHERE genre = %s;', (genre,))
            
            # Verify by fetching all the rows returned by the query
            rows = cur.fetchall()
            
            # Initialize an empty list to store the books
            books = []
            
            # For loop to iterate through the rows and create a list of dictionaries for each book
            for row in rows:
                books.append({
                    'book_id': row[0],
                    'title': row[1],
                    'author': row[2],
                    'price': row[3],
                    'stock_quantity': row[4],
                })
                
    return books

def get_quantity_by_book_id(book_id):
    """
    Returns the stock quantity of a specific book by its ID from the database.
    """
    # Get a connection to the database
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to fetch the stock quantity of a book by its ID
            cur.execute('SELECT stock_quantity FROM books WHERE book_id = %s;', (book_id,))
            
            # Verify by fetching the row returned by the query
            row = cur.fetchone()
            
            # If a row returns True, return the stock quantity
            if row:
                return row[0]
            
    return None

def add_book(title, author, price, stock_quantity, genre):
    """
    Adds a new book to the database.
    """
    # Get a connection to the database
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            
            # Execute the SQL query to insert a new book
            cur.execute('INSERT INTO books (title, author, price, stock_quantity, genre) VALUES (%s, %s, %s, %s, %s);',
                        (title, author, price, stock_quantity, genre))
            
            # Commit the changes to the database
            conn.commit()
            
            return cur.lastrowid


