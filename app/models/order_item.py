# app/models/order_item.py
from app.models.book import Book

class OrderItem:
    def __init__(self, book_id, quantity):
        self.book = Book.get_by_id(book_id)
        if not self.book:
            raise ValueError(f"Book with ID {book_id} not found.")
        if self.book.stock_quantity < quantity:
            raise ValueError(f"Not enough stock for '{self.book.title}'.")

        self.book_id = book_id
        self.quantity = quantity
        self.price = self.book.price
        self.subtotal = self.price * quantity

    def decrease_stock(self):
        self.book.decrease_stock(self.quantity)

    def to_dict(self):
        return {
            'book_id': self.book_id,
            'title': self.book.title,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.subtotal
        }
