# Step 3: Import Required Modules
import bcrypt
import os

# Step 6: Define the User Data File
USER_DATA_FILE = "users.txt"

# -----------------------------
# Step 4: Implement the Password Hashing Function
# -----------------------------
def hash_password(plain_text_password):
    """
    Hashes a password using bcrypt with automatic salt generation.

    Args:
        plain_text_password (str): The plaintext password to hash

    Returns:
        str: The hashed password as a UTF-8 string
    """
    # Encode the password to bytes (bcrypt requires byte strings)
    password_bytes = plain_text_password.encode('utf-8')

    # Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()

    # Hash the password using bcrypt.hashpw()
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Decode the hash back to a string to store in a text file
    hashed_str = hashed.decode('utf-8')

    return hashed_str

# -----------------------------
# Step 5: Implement the Password Verification Function
# -----------------------------
def verify_password(plain_text_password, hashed_password):
    """
    Verifies a plaintext password against a stored bcrypt hash.

    Args:
        plain_text_password (str): The password to verify
        hashed_password (str): The stored hash to check against

    Returns:
        bool: True if the password matches, False otherwise
    """
    # Encode both the plaintext password and the stored hash to bytes
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    # Use bcrypt.checkpw() to verify the password
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# -----------------------------
# Step 6: Test Your Hashing Functions (Temporary Test Code)
# -----------------------------
test_password = "SecurePassword123"

# Test hashing
hashed = hash_password(test_password)
print(f"Original password: {test_password}")
print(f"Hashed password: {hashed}")
print(f"Hash length: {len(hashed)} characters")

# Test verification with correct password
is_valid = verify_password(test_password, hashed)
print(f"\nVerification with correct password: {is_valid}")

# Test verification with incorrect password
is_invalid = verify_password("WrongPassword", hashed)
print(f"Verification with incorrect password: {is_invalid}")

# -----------------------------
# Step 7: Implement the Registration Function
# -----------------------------
def register_user(username, password):
    """
    Registers a new user by hashing their password and storing credentials.

    Args:
        username (str): The username for the new account
        password (str): The plaintext password to hash and store

    Returns:
        bool: True if registration successful, False if username already exists
    """
    # Check if the username already exists
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                stored_username = line.strip().split(",")[0]
                if username == stored_username:
                    return False  # Username already exists

    # Hash the password
    hashed_pw = hash_password(password)

    # Append the new user to the file
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{hashed_pw}\n")

    return True

# -----------------------------
# Step 8: Implement the User Existence Check
# -----------------------------
def user_exists(username):
    """
    Checks if a username already exists in the user database.

    Args:
        username (str): The username to check

    Returns:
        bool: True if the user exists, False otherwise
    """
    # Handle the case where the file doesn't exist yet
    if not os.path.exists(USER_DATA_FILE):
        return False

    # Read the file and check each line for the username
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_username = line.strip().split(",")[0]
            if username == stored_username:
                return True  # User exists

    return False  # User not found

# -----------------------------
# Step 9: Implement the Login Function
# -----------------------------
def login_user(username, password):
    """
    Authenticates a user by verifying their username and password.

    Args:
        username (str): The username to authenticate
        password (str): The plaintext password to verify

    Returns:
        bool: True if authentication successful, False otherwise
    """
    # Handle the case where no users are registered yet
    if not os.path.exists(USER_DATA_FILE):
        return False

    # Search for the username in the file
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_username, stored_hash = line.strip().split(",")

            # If username matches, verify the password
            if username == stored_username:
                return verify_password(password, stored_hash)

    # If we reach here, the username was not found
    return False

# -----------------------------
# Step 10: Implement Input Validation
# -----------------------------
def validate_username(username):
    """
    Validates username format.

    Args:
        username (str): The username to validate

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if " " in username:
        return False, "Username cannot contain spaces."
    return True, ""

def validate_password(password):
    """
    Validates password strength.

    Args:
        password (str): The password to validate

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number."
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."
    return True, ""

# -----------------------------
# Step 11: Implement the Main Menu
# -----------------------------
def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Register the user
            if register_user(username, password):
                print(f"User '{username}' registered successfully!")
            else:
                print(f"Error: Username '{username}' already exists.")

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the database or protected area.)")
            else:
                print("\nLogin failed. Invalid username or password.")

            # Optional: Ask if they want to logout or exit
            input("\nPress Enter to return to main menu...")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

# Run the program
if __name__ == "__main__":
    main()
