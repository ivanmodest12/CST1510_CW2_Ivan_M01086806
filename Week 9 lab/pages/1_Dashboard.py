import streamlit as st
from app.data.db import connect_database
from app.data.incidents import get_all_incidents
from app.data.datasets import get_all_datasets
from app.data.tickets import get_all_tickets

st.set_page_config(page_title="Dashboard", layout="wide")

# Authentication guard
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.experimental_rerun()
    st.stop()

conn = connect_database()

st.title("📊 Dashboard")
st.success(f"Welcome, {st.session_state.get('username', 'User')}!")

# Metrics area
col1, col2, col3 = st.columns(3)
incidents = get_all_incidents(conn)
datasets = get_all_datasets(conn)
tickets = get_all_tickets(conn)

col1.metric("Incidents", len(incidents))
col2.metric("Datasets", len(datasets))
col3.metric("Tickets", len(tickets))

st.divider()

st.subheader("Incidents table")
st.dataframe(incidents, use_container_width=True)

st.subheader("Quick actions")
with st.expander("Add sample incident (for demo)"):
    title = st.text_input("Title", key="sample_title")
    severity = st.selectbox("Severity", ["Low","Medium","High","Critical"], key="sample_sev")
    status = st.selectbox("Status", ["Open","In Progress","Resolved"], key="sample_stat")
    if st.button("Add incident"):
        from app.data.incidents import insert_incident
        insert_incident(conn, title, severity, status)
        st.success("Incident added. Refreshing...")
        st.experimental_rerun()

st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.experimental_rerun()
