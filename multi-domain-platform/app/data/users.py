import sqlite3
import bcrypt
from .db import connect_database

# -----------------------
# Register user
# -----------------------
def register_user(username, password, role="user"):
    conn = connect_database()
    cursor = conn.cursor()
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    password_hash = hashed.decode('utf-8')
    
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        conn.commit()
        return True, "User registered successfully"
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    finally:
        conn.close()

# -----------------------
# Login user
# -----------------------
def login_user(username, password):
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result is None:
        return False, "User not found"
    
    stored_hash = result[0].encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return True, "Login successful"
    else:
        return False, "Incorrect password"
