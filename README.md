# 📚 Bookstore Management Web App

A Flask-based web application for managing a bookstore inventory, featuring user authentication, order processing, and responsive design. This project demonstrates full-stack development skills with a focus on modular architecture and deployment readiness.

---

## 🚀 Features
- User registration and login with secure password handling
- View a catalog of available books
- Create orders and calculate total purchase price
- Automatically update stock quantity upon purchase
- Organized and modular project structure
- Responsive design for desktop and mobile devices
- Deployed on Render @ ([https://render.com](https://bookstore-app-with-login.onrender.com))

---

## 🛠 Tech Stack

- **Backend**: Python, Flask  
- **Frontend**: HTML (Jinja2 templating), CSS
- **Database**: PostgreSQL
- **Authentication**: Flask-Login, Werkzeug Security
- **Deployment**: Render  
- **Version Control**: Git & GitHub  

---

## 📁 Project Structure
```
bookstore_app_with_login/
├── app/
│   ├── __init__.py                   # App factory: creates and configures Flask app
│   ├── routes.py                     # Routes using Blueprint (`main`)
│   ├── models/
│   │   ├── __init__.py               
│   │   ├── db.py                     # DB connection logic
│   │   ├── customer.py               # Customer model and user loader
│   │   ├── book.py                   # Book model
│   │   ├── order.py                  # Order model
│   │   └── order_item.py             # OrderItem model
│   ├── services/
│   │   ├── __init__.py               # Makes services a package
│   │   ├── auth_service.py           # Auth functions: login, validation, hashing
│   │   ├── reg_service.py            # Registration logic (split from auth)
│   │   ├── order_service.py          # Business logic for order processing
│   │   └── book_service.py           # Business logic for book processing
│   ├── templates/
│   │   ├── base.html                 # Base layout used across templates
│   │   ├── index.html                # Homepage
│   │   ├── login.html                # Login page
│   │   ├── register.html             # Registration page
│   │   └── order_confirmation.html   # Order confirmation page
│   ├── order_exceptions.py           # Custom exceptions for order errors
│   └── auth_exceptions.py            # Custom exceptions for auth errors
├── .gitignore                        # Excludes cache, logs, dumps, env files, etc.
├── .render.yaml                      # Render deployment configuration
├── main.py                           # Entry point for running app locally
├── requirements.txt                  # Python dependencies
├── logger.py                         # Logging setup used throughout the app
├── gen_password_hash.py              # Tool to generate hashed passwords
└── README.md                         # Project description, setup, usage

```
---

## 🔧 Setup & Installation (Local)

1. Clone the repository:
   git clone https://github.com/ReginaldCosensIII/bookstore_app_with_login.git
   cd bookstore_app

2. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Set environment variables:
   DATABASE_URL=your_postgres_connection_url
   FLASK_ENV=development
   SECRET_KEY=your_secret_key

5. Run the app locally
   python main.py
   
---

🌐 Deployment

This app is deployed on Render.
The .render.yaml file handles the configuration:
```
services:
  - type: web
    name: bookstore-app-login
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn main:app"
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: bookstore-db
          property: connectionString
      - key: FLASK_ENV
        value: production

databases:
  - name: bookstore-db
```
---

🧠 Author

```
Reginald Cosens III
GitHub:  @ReginaldCosensIII
Email:   ReginaldCosensIII@gmail.com
```
---

📌 Future Improvements

-  Add admin dashboard(admin & customer roles)
   - Admin report
   - Admin function  
-  Implement SQLAlchemy
-  Add book images on index.html and book description when hovering over
-  Add RESTful API support
-  Implement order history and customer profiles
-  Add pagination and search functionality

---

📜 License:
```
This project is for educational and demonstration purposes.
```
