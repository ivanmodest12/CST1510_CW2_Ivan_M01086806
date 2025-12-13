import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "DATA", "intelligence_platform.db")

def ensure_data_dir():
    data_dir = os.path.dirname(DB_PATH)
    os.makedirs(data_dir, exist_ok=True)

def connect_database(path=None):
    """Return a sqlite3 connection. Creates the DB and tables if missing."""
    ensure_data_dir()
    db_file = path or DB_PATH
    conn = sqlite3.connect(db_file, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # ensure tables exist
    _create_tables(conn)
    return conn

def _create_tables(conn):
    cur = conn.cursor()
    # users table
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )""")
    # incidents table
    cur.execute("""CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        severity TEXT,
        status TEXT,
        date TEXT
    )""")
    # datasets metadata
    cur.execute("""CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        source TEXT,
        category TEXT,
        size INTEGER
    )""")
    # it tickets
    cur.execute("""CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        priority TEXT,
        status TEXT,
        created_date TEXT
    )""")
    conn.commit()
