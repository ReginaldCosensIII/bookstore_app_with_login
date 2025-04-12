from flask_login import LoginManager
from app.models.customer import Customer
from app.models.db import get_db_connection  # adjust if needed

login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Redirect to 'login' route if not logged in

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT customer_id, email, password FROM customers WHERE customer_id = %s', (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return Customer(id=row[0], email=row[1], password=row[2])
    return None
