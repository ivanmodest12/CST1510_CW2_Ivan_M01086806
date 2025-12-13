import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_user(conn, username: str, password: str, role: str = "user"):
    cur = conn.cursor()
    pw = hash_password(password)
    cur.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (username, pw, role))
    conn.commit()
    return cur.lastrowid

def verify_user(conn, username: str, password: str) -> bool:
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    if not row:
        return False
    return row["password_hash"] == hash_password(password)

def get_user_role(conn, username: str):
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE username = ?", (username,))
    r = cur.fetchone()
    return r["role"] if r else None
