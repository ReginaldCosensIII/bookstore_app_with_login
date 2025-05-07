# bookstore_app_with_login/app/services/book_service.py

# Note: This service currently is not being used and we can decide as a group
# how to handle it. I was keeping them to possible use when and if we
# implement a sort/filter feature on the index page.
# We will reconsider whether these service functions are necessary or if the
# model methods suffice for our current needs. If complex logic involving
# multiple models or external services related to books arises, then a
# dedicated book service makes more sense.

from app.models.book import Book # Import the Book model
from app.models.db import get_db_connection # Import DB connection utility
from logger import logger # Import custom logger
from decimal import Decimal # For price handling

# --- Potentially Redundant Functions (Consider using Model methods directly) we can consider---

# If you decide to keep these, ensure the Book model doesn't already provide identical methods.

def get_books_by_author(author_name):
    """
    Fetches all books by a specific author. (Case-insensitive search)

    Args:
        author_name (str): The name of the author to search for.

    Returns:
        list[Book]: A list of Book objects by the specified author.
    """
    books_by_author = []
    if not author_name:
        return books_by_author

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Use LOWER for case-insensitive comparison
                query = """SELECT book_id, title, author, genre, price, stock_quantity
                           FROM books WHERE LOWER(author) = LOWER(%s) ORDER BY title;"""
                cur.execute(query, (author_name.strip(),))
                rows = cur.fetchall()

        for row in rows:
            books_by_author.append(Book(
                book_id=row["book_id"],
                title=row["title"],
                author=row["author"],
                genre=row["genre"],
                price=row["price"],
                stock_quantity=row["stock_quantity"]
            ))
        logger.info(f"Found {len(books_by_author)} books for author '{author_name}'.")
        return books_by_author
    except Exception as e:
        logger.exception(f"Error retrieving books by author '{author_name}'.")
        return []


def get_books_by_genre(genre_name):
    """
    Fetches all books belonging to a specific genre. (Case-insensitive search)

     Args:
        genre_name (str): The name of the genre to search for.

    Returns:
        list[Book]: A list of Book objects in the specified genre.
    """
    books_by_genre = []
    if not genre_name:
        return books_by_genre

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                 # Use LOWER for case-insensitive comparison
                query = """SELECT book_id, title, author, genre, price, stock_quantity
                           FROM books WHERE LOWER(genre) = LOWER(%s) ORDER BY title;"""
                cur.execute(query, (genre_name.strip(),))
                rows = cur.fetchall()

        for row in rows:
             books_by_genre.append(Book(
                book_id=row["book_id"],
                title=row["title"],
                author=row["author"],
                genre=row["genre"],
                price=row["price"],
                stock_quantity=row["stock_quantity"]
            ))
        logger.info(f"Found {len(books_by_genre)} books for genre '{genre_name}'.")
        return books_by_genre
    except Exception as e:
         logger.exception(f"Error retrieving books by genre '{genre_name}'.")
         return []

# We will consider adding functions for more complex book-related logic if needed as a group, e.g.,
# - get_featured_books()
# - search_books(query)
# - update_book_details(book_id, ...) -> interacts with Book model's update