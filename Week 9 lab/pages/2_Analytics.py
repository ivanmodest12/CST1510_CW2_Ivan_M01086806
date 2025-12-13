import streamlit as st
import pandas as pd
from app.data.db import connect_database
from app.data.incidents import get_all_incidents

st.set_page_config(page_title="Analytics", layout="wide")

# Auth guard
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    st.stop()

conn = connect_database()

st.title("📈 Analytics")

incidents = get_all_incidents(conn)
if incidents.empty:
    st.info("No incident data yet — add some from the Dashboard or sample data.")
else:
    st.subheader("Incident severity distribution")
    counts = incidents['severity'].value_counts()
    st.bar_chart(counts)

    st.subheader("Incidents over time (if dates present)")
    if 'date' in incidents.columns and incidents['date'].notnull().any():
        try:
            df = incidents.dropna(subset=['date'])
            df['date'] = pd.to_datetime(df['date'])
            df2 = df.groupby(df['date'].dt.date).size()
            st.line_chart(df2)
        except Exception as e:
            st.write("Could not parse dates:", e)
