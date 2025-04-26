# app/models/order.py
from datetime import datetime
from app.models.order_item import OrderItem

class Order:
    def __init__(self, customer_id, items_data):
        """
        items_data: list of dicts like [{'book_id': 1, 'quantity': 2}, ...]
        """
        self.customer_id = customer_id
        self.order_date = datetime.now()
        self.items = []
        self.total_amount = 0.0

        for item in items_data:
            order_item = OrderItem(item['book_id'], item['quantity'])
            self.items.append(order_item)
            self.total_amount += order_item.subtotal

    def save(self, db_conn):
        """
        Saves order and order items to the database.
        Also decreases stock for each book.
        """
        with db_conn.cursor() as cur:
            # Insert order
            cur.execute("""
                INSERT INTO orders (customer_id, order_date, total_amount)
                VALUES (%s, %s, %s)
                RETURNING order_id;
            """, (self.customer_id, self.order_date, self.total_amount))
            order_id = cur.fetchone()[0]

            # Insert each order item
            for item in self.items:
                cur.execute("""
                    INSERT INTO order_items (order_id, book_id, quantity)
                    VALUES (%s, %s, %s);
                """, (order_id, item.book_id, item.quantity))
                # Update book stock
                cur.execute("""
                    UPDATE books
                    SET stock_quantity = stock_quantity - %s
                    WHERE book_id = %s;
                """, (item.quantity, item.book_id))

        db_conn.commit()
        return order_id

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "order_date": self.order_date.isoformat(),
            "total_amount": self.total_amount,
            "items": [item.to_dict() for item in self.items]
        }
