from werkzeug.security import generate_password_hash

# Example: Hash a password and insert it into the database
hashed_password = generate_password_hash('password')
print(hashed_password)