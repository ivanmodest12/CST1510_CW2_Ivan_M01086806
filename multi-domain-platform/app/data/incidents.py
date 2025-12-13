import sqlite3
import pandas as pd
from .db import connect_database

# -----------------------
# Insert incident
# -----------------------
def insert_incident(conn, incident_date, incident_type, severity, status, description, reported_by):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cyber_incidents (incident_date, incident_type, severity, status, description, reported_by) VALUES (?, ?, ?, ?, ?, ?)",
        (incident_date, incident_type, severity, status, description, reported_by)
    )
    conn.commit()
    return cursor.lastrowid

# -----------------------
# Update incident status
# -----------------------
def update_incident_status(conn, incident_id, status):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE incident_id = ?",
        (status, incident_id)
    )
    conn.commit()

# -----------------------
# Delete incident
# -----------------------
def delete_incident(conn, incident_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE incident_id = ?", (incident_id,))
    conn.commit()

# -----------------------
# Analytical Queries
# -----------------------
def get_incidents_by_type_count(conn):
    query = "SELECT incident_type, COUNT(*) as count FROM cyber_incidents GROUP BY incident_type"
    return pd.read_sql_query(query, conn)

def get_high_severity_by_status(conn):
    query = "SELECT status, COUNT(*) as count FROM cyber_incidents WHERE severity='High' GROUP BY status"
    return pd.read_sql_query(query, conn)
