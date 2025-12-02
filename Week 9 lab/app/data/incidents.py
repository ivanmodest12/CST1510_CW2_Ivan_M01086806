import pandas as pd

def get_all_incidents(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM cyber_incidents")
    rows = cur.fetchall()
    return pd.DataFrame([dict(r) for r in rows])

def insert_incident(conn, title, severity, status, date=None):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cyber_incidents (title, severity, status, date) VALUES (?, ?, ?, ?)",
        (title, severity, status, date)
    )
    conn.commit()
    return cur.lastrowid

def update_incident(conn, incident_id, **fields):
    keys = ", ".join([f"{k} = ?" for k in fields.keys()])
    vals = list(fields.values()) + [incident_id]
    cur = conn.cursor()
    cur.execute(f"UPDATE cyber_incidents SET {keys} WHERE id = ?", vals)
    conn.commit()

def delete_incident(conn, incident_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
