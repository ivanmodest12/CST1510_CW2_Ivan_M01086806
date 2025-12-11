import streamlit as st
import pandas as pd
from app.data.db import connect_database
import os

st.set_page_config(page_title="Dashboard", layout="wide")

# ------------------------
# Authentication guard
# ------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.experimental_rerun()
    st.stop()

st.title("📊 Dashboard")
st.success(f"Welcome, {st.session_state.get('username', 'User')}!")

conn = connect_database()

# ------------------------
# Define absolute paths to CSV files
# ------------------------
BASE_PATH = r"C:\Users\Spark\Documents\week10_multidomain\Week 8 lab\DATA"

INCIDENTS_FILE = os.path.join(BASE_PATH, "cyber_incidents.csv")
DATASETS_FILE  = os.path.join(BASE_PATH, "datasets_metadata.csv")
TICKETS_FILE   = os.path.join(BASE_PATH, "it_tickets.csv")

# ------------------------
# Load CSV data safely
# ------------------------
def load_csv(filepath, default_columns):
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        if df.empty:
            return pd.DataFrame(columns=default_columns)
        return df
    else:
        return pd.DataFrame(columns=default_columns)

incidents = load_csv(INCIDENTS_FILE, ["Title", "Severity", "Status"])
datasets  = load_csv(DATASETS_FILE, ["Dataset Name", "Description"])
tickets   = load_csv(TICKETS_FILE, ["Ticket ID", "Issue", "Status"])

# ------------------------
# Metrics area
# ------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Incidents", len(incidents))
col2.metric("Datasets", len(datasets))
col3.metric("Tickets", len(tickets))

st.divider()

# ------------------------
# Show incidents table
# ------------------------
st.subheader("Incidents Table")
if not incidents.empty:
    st.dataframe(incidents, use_container_width=True)
else:
    st.info("No incidents found in the CSV file.")

# ------------------------
# Show datasets table
# ------------------------
st.subheader("Datasets Table")
if not datasets.empty:
    st.dataframe(datasets, use_container_width=True)
else:
    st.info("No datasets found in the CSV file.")

# ------------------------
# Show tickets table
# ------------------------
st.subheader("Tickets Table")
if not tickets.empty:
    st.dataframe(tickets, use_container_width=True)
else:
    st.info("No tickets found in the CSV file.")

st.divider()

# ------------------------
# Log out button
# ------------------------
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.experimental_rerun()
