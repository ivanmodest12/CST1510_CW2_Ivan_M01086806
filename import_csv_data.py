# import_csv_data.py
import pandas as pd
import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('database/platform.db')
cursor = conn.cursor()

print("📊 Importing CSV data into database...")

# 1. Import cyber_incidents.csv
try:
    incidents_df = pd.read_csv('cyber_incidents.csv')
    for _, row in incidents_df.iterrows():
        cursor.execute("""
            INSERT INTO cyber_incidents 
            (title, severity, status, description, reported_by, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row['title'],
            row.get('priority', 'Medium'),  # Map priority to severity
            row.get('status', 'Open'),
            row.get('description', ''),
            f"User_{row.get('reported_by', 1)}",
            datetime.now().strftime('%Y-%m-%d')
        ))
    print(f"✅ Imported {len(incidents_df)} incidents")
except FileNotFoundError:
    print("⚠️ cyber_incidents.csv not found")

# 2. Import datasets_metadata.csv  
try:
    datasets_df = pd.read_csv('datasets_metadata.csv')
    for _, row in datasets_df.iterrows():
        cursor.execute("""
            INSERT INTO datasets_metadata 
            (name, description, created_at)
            VALUES (?, ?, ?)
        """, (
            row['name'],
            row.get('description', ''),
            row.get('created_at', datetime.now().isoformat())
        ))
    print(f"✅ Imported {len(datasets_df)} datasets")
except FileNotFoundError:
    print("⚠️ datasets_metadata.csv not found")

# 3. Import it_tickets.csv
try:
    tickets_df = pd.read_csv('it_tickets.csv')
    for _, row in tickets_df.iterrows():
        cursor.execute("""
            INSERT INTO it_tickets 
            (title, priority, status, assigned_to, description, created_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row.get('subject', row.get('title', '')),
            row.get('priority', 'Medium'),
            row.get('status', 'Open'),
            f"User_{row.get('assigned_to', 1)}",
            row.get('description', ''),
            datetime.now().strftime('%Y-%m-%d')
        ))
    print(f"✅ Imported {len(tickets_df)} tickets")
except FileNotFoundError:
    print("⚠️ it_tickets.csv not found")

# 4. Create a default admin user
cursor.execute("""
    INSERT OR IGNORE INTO users 
    (username, password_hash, role) 
    VALUES (?, ?, ?)
""", ('admin', 'admin123', 'admin'))

conn.commit()
conn.close()
print("\n🎉 Data import complete!")
print("Refresh your dashboard to see the data.")