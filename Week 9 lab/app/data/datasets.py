import pandas as pd

def get_all_datasets(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM datasets_metadata")
    rows = cur.fetchall()
    return pd.DataFrame([dict(r) for r in rows])

def insert_dataset(conn, name, source, category, size):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO datasets_metadata (name, source, category, size) VALUES (?, ?, ?, ?)",
        (name, source, category, size)
    )
    conn.commit()
    return cur.lastrowid
