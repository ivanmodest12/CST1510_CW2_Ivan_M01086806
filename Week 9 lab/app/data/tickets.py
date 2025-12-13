import pandas as pd

def get_all_tickets(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM it_tickets")
    rows = cur.fetchall()
    return pd.DataFrame([dict(r) for r in rows])

def insert_ticket(conn, title, priority, status, created_date=None):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO it_tickets (title, priority, status, created_date) VALUES (?, ?, ?, ?)",
        (title, priority, status, created_date)
    )
    conn.commit()
    return cur.lastrowid
