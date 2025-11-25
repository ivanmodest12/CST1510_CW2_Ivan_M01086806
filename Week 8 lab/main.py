import sqlite3
from app.data.db import connect_database
from app.data.schema import create_all_tables, drop_all_tables
from app.data.users import register_user, login_user
from app.data.incidents import insert_incident, update_incident_status, delete_incident, get_incidents_by_type_count
from app.data.datasets import insert_dataset, get_all_datasets
from app.data.tickets import insert_ticket, update_ticket_status, delete_ticket, get_all_tickets
from pathlib import Path

# -----------------------
# Setup database
# -----------------------
DB_PATH = Path("DATA/intelligence_platform.db")
conn = connect_database(DB_PATH)

# Drop & create tables
drop_all_tables(conn)
create_all_tables(conn)

# -----------------------
# Users Demo
# -----------------------
print("=== Users Demo ===")
success, msg = register_user("alice", "Password123!", "admin")
print("Register alice:", msg)

success, msg = login_user("alice", "Password123!")
print("Login alice:", msg)

# -----------------------
# Incidents Demo
# -----------------------
print("\n=== Cyber Incidents Demo ===")
incident_id = insert_incident(
    conn,
    "2024-11-01",
    "Phishing",
    "High",
    "Open",
    "Test phishing incident",
    "alice"
)
print("Inserted incident ID:", incident_id)

update_incident_status(conn, incident_id, "Resolved")
print("Updated incident status to Resolved")

incidents_summary = get_incidents_by_type_count(conn)
print("Incident types count:\n", incidents_summary)

delete_incident(conn, incident_id)
print("Deleted incident ID:", incident_id)

# -----------------------
# Datasets Demo
# -----------------------
print("\n=== Datasets Demo ===")
dataset_id = insert_dataset(conn, "Cybersecurity", "Network Logs", "Sample dataset")
print("Inserted dataset ID:", dataset_id)

datasets = get_all_datasets(conn)
print("All datasets:\n", datasets)

# -----------------------
# Tickets Demo
# -----------------------
print("\n=== IT Tickets Demo ===")
ticket_id = insert_ticket(conn, "Printer not working", "Cannot print on floor 2", "High", "Open")
print("Inserted ticket ID:", ticket_id)

update_ticket_status(conn, ticket_id, "Closed")
print("Updated ticket status to Closed")

tickets = get_all_tickets(conn)
print("All tickets:\n", tickets)

delete_ticket(conn, ticket_id)
print("Deleted ticket ID:", ticket_id)

# Close connection
conn.close()
print("\n=== Demo Completed ===")
