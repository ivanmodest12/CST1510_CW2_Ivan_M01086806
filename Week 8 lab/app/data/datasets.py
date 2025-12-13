import sqlite3
from .db import connect_database

# -----------------------
# Insert dataset
# -----------------------
def insert_dataset(conn, domain, source, description):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO datasets_metadata (domain, source, description) VALUES (?, ?, ?)",
        (domain, source, description)
    )
    conn.commit()
    return cursor.lastrowid

# -----------------------
# Get all datasets
# -----------------------
def get_all_datasets(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets_metadata")
    return cursor.fetchall()
