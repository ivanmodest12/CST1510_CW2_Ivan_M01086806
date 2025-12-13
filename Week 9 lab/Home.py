import streamlit as st
import pandas as pd
import os
from app.data.db import connect_database
from app.data.users import verify_user, create_user
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Intelligence Platform", layout="wide")

# DB connection
conn = connect_database()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Path to CSV files
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Week 8 lab/DATA'))

# ------------------------
# If not logged in: show login/register
# ------------------------
if not st.session_state.logged_in:
    tabs = st.tabs(["Login", "Register"])

    with tabs[0]:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Log in"):
            if verify_user(conn, login_username, login_password):
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.success(f"Welcome, {login_username}!")
                st.rerun()  # <-- updated here
            else:
                st.error("Invalid credentials")

    with tabs[1]:
        st.subheader("Register")
        new_username = st.text_input("Choose a username", key="register_username")
        new_password = st.text_input("Choose a password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")

        if st.button("Create account"):
            if not new_username or not new_password:
                st.warning("Please fill in all fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                try:
                    create_user(conn, new_username, new_password)
                    st.success("Account created! Go to Login to sign in.")
                except Exception as e:
                    st.error(f"Could not create account: {e}")

# ------------------------
# After login: show dashboard only
# ------------------------
else:
    st.header(f"Welcome to the Dashboard, {st.session_state.username}!")

    # Load CSV files
    try:
        users_df = pd.read_csv(os.path.join(BASE_DIR, 'users.txt'))
        incidents_df = pd.read_csv(os.path.join(BASE_DIR, 'cyber_incidents.csv'))
        datasets_df = pd.read_csv(os.path.join(BASE_DIR, 'datasets_metadata.csv'))
        tickets_df = pd.read_csv(os.path.join(BASE_DIR, 'it_tickets.csv'))
    except FileNotFoundError as e:
        st.error(f"Could not find CSV files: {e}")
        st.stop()

    # Optional: Tabs in dashboard for organization
    dash_tabs = st.tabs(["Users", "Incidents", "Datasets", "Tickets", "Charts"])

    with dash_tabs[0]:
        st.subheader("Users")
        st.dataframe(users_df)

    with dash_tabs[1]:
        st.subheader("Incidents")
        st.dataframe(incidents_df)

    with dash_tabs[2]:
        st.subheader("Datasets Metadata")
        st.dataframe(datasets_df)

    with dash_tabs[3]:
        st.subheader("IT Tickets")
        st.dataframe(tickets_df)

    with dash_tabs[4]:
        st.subheader("Incidents by Priority")
        st.bar_chart(incidents_df['priority'].value_counts())

        st.subheader("Tickets by Status")
        st.bar_chart(tickets_df['status'].value_counts())

        st.subheader("Incidents by Status (Seaborn)")
        fig, ax = plt.subplots()
        sns.countplot(data=incidents_df, x='status', palette='Set2', ax=ax)
        st.pyplot(fig)
