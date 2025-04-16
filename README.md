# 📚 Bookstore Management Web App

A simple Flask web application backed by PostgreSQL for managing a bookstore inventory, built as a personal project to demonstrate full-stack development skills and hands-on database integration.

---

## 🚀 Features

- View a catalog of available books
- Create orders and calculate total purchase price
- Automatically update stock quantity upon purchase
- Organized and modular project structure
- Deployable on [Render.com](https://render.com)

---

## 🛠 Tech Stack

- **Backend**: Python, Flask  
- **Frontend**: HTML (Jinja2 templating)  
- **Database**: PostgreSQL  
- **Deployment**: Render  
- **Version Control**: Git & GitHub  

---

## 📁 Project Structure
```
bookstore_app_with_login/
├── app/
│   ├── __init__.py                # App factory: creates and configures Flask app
│   ├── routes.py                  # Routes using Blueprint (`main`)
│   ├── models/
│   │   ├── db.py                  # DB connection logic
│   │   └── customer.py            # Customer model and user loader
│   ├── services/
│   │   ├── __init__.py            # Makes services a package
│   │   ├── auth_service.py        # Auth functions: register, login, validate, hash
│   │   └── order_service.py       # Business logic for order processing
│   └── templates/
│       ├── index.html             # Homepage
│       ├── login.html             # Login page
│       ├── register.html          # Registration page
│       └── order_confirmation.html# (Optional) Order success/confirmation page
├── .gitignore                     # Excludes cache, logs, dumps, env files, etc.
├── .render.yaml                   # Render deployment configuration
├── main.py                        # Entry point for running app locally
├── requirements.txt               # Cleaned Python dependencies
├── logger.py                      # Logging setup used throughout the app
├── gen_password_hash.py          # Tool to generate hashed passwords
├── test_order.py                  # Optional test script for order creation
└── README.md                      # Project description, setup, usage
```
---

## 🔧 Setup & Installation (Local)

1. Clone the repository:
   git clone https://github.com/ReginaldCosensIII/bookstore_app.git
   cd bookstore_app

2. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Set environment variables:
   DATABASE_URL=your_postgres_connection_url

5. Run the app locally

---

🌐 Deployment

This app is deployed on Render.
The .render.yaml file handles the configuration:
```
services:
  - type: web
    name: bookstore-app
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn app:app"
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: bookstore-db
          property: connectionString

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

-  Add (admin & customer roles)
-  Improve UI with CSS framework (e.g., Bootstrap or Tailwind)
-  Add RESTful API support
-  Implement order history and customer profiles
-  Add pagination and search functionality

---

📜 License:
```
This project is for educational and demonstration purposes.
```
