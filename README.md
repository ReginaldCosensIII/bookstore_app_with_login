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
│   ├── __init__.py                # Initializes the Flask application
│   ├── auth_exceptions.py         # Custom exceptions for authentication-related errors
│   ├── extensions.py              # Extensions setup (e.g., for SQLAlchemy, login manager, etc.)
│   ├── order_exceptions.py        # Custom exceptions for order-related errors
│   ├── routes.py                  # Defines application routes using Flask Blueprints
│   ├── models/
│   │   ├── __init__.py            # Makes the models directory a Python package
│   │   ├── book.py                # Book model class definition
│   │   ├── customer.py            # Customer model and user loader for authentication
│   │   ├── db.py                  # Database connection and setup using psycopg2
│   │   ├── order.py               # Order model class definition
│   │   └── order_items.py         # OrderItem model class definition
│   ├── services/
│   │   ├── __init__.py            # Initializes the services package
│   │   ├── auth_service.py        # Authentication logic: login, logout, credential validation
│   │   ├── book_service.py        # Business logic for book inventory management
│   │   ├── order_service.py       # Order creation, validation, inventory updates
│   │   └── reg_service.py         # Handles registration logic and validation
│   ├── templates/                 # HTML templates rendered by Flask
│   │   ├── base.html              # Base template with shared layout and styles
│   │   ├── index.html             # Homepage template
│   │   ├── login.html             # Login page template
│   │   ├── register.html          # Registration page template
│   │   └── order_confirmation.html # Order confirmation page template
│   └── static/css/styles.css      # Main CSS stylesheet for template styling
├── .gitignore                     # Specifies files and directories to be ignored by Git
├── .render.yaml                   # Configuration file for deployment on Render
├── README.md                      # Project overview and setup instructions
├── gen_password_hash.py           # Utility script for generating password hashes using werkzeug.security
├── logger.py                      # Configures application-wide logging with timestamps and levels
├── main.py                        # Entry point for running the application locally
└── requirements.txt               # Lists Python dependencies for the app

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
