import sqlite3
from .db import connect_database

# -----------------------
# Insert ticket
# -----------------------
def insert_ticket(conn, title, description, priority, status):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO it_tickets (title, description, priority, status) VALUES (?, ?, ?, ?)",
        (title, description, priority, status)
    )
    conn.commit()
    return cursor.lastrowid

# -----------------------
# Update ticket status
# -----------------------
def update_ticket_status(conn, ticket_id, status):
    cursor = conn.cursor()
    cursor.execute("UPDATE it_tickets SET status = ? WHERE ticket_id = ?", (status, ticket_id))
    conn.commit()

# -----------------------
# Delete ticket
# -----------------------
def delete_ticket(conn, ticket_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
    conn.commit()

# -----------------------
# Get all tickets
# -----------------------
def get_all_tickets(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM it_tickets")
    return cursor.fetchall()
