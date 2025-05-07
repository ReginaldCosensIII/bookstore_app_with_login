# bookstore_app_with_login/gen_password_hash.py

"""
Utility script to generate a Werkzeug password hash for a given password.

This script is typically used for manual database setup or testing purposes.
It takes a plain-text password, hashes it using Werkzeug's security functions,
and prints the resulting hash to the console.
"""

from werkzeug.security import generate_password_hash

# --- Configuration ---
# Set the plain-text password you want to hash here.
# IMPORTANT: Do not hardcode sensitive passwords in production code.
# Consider using environment variables or a secure input method if needed.
PASSWORD_TO_HASH = 'your_password_here' # Replace with the actual password

# --- Execution ---
if __name__ == "__main__":
    # Generate the password hash using Werkzeug's recommended method.
    # The method automatically includes a salt and uses a strong hashing algorithm.
    hashed_password = generate_password_hash(PASSWORD_TO_HASH)

    # Print the generated hash to the console.
    # This hash can then be stored in the database (e.g., in the 'customers' table).
    print("Generated Password Hash:")
    print(hashed_password)
    print("\nCopy this hash and store it securely in your database.")