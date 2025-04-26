# app/models/book.py
from app.models.db import get_db_connection

class Book:
    def __init__(self, book_id, title, author, genre, price, stock_quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price
        self.stock_quantity = stock_quantity

    @classmethod
    def get_by_id(cls, book_id):
        conn = get_db_connection()
        book = conn.execute('SELECT * FROM books WHERE book_id = %s', (book_id,)).fetchone()
        conn.close()
        if book:
            return cls(**book)
        return None

    def decrease_stock(self, quantity):
        if self.stock_quantity < quantity:
            raise ValueError("Not enough stock available.")
        self.stock_quantity -= quantity
        conn = get_db_connection()
        conn.execute('UPDATE books SET stock_quantity = %s WHERE book_id = %s',
                     (self.stock_quantity, self.book_id))
        conn.commit()
        conn.close()
