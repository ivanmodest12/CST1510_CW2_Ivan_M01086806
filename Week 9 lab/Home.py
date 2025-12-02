import streamlit as st
from app.data.db import connect_database
from app.data.users import verify_user, create_user

# Page config
st.set_page_config(page_title="Intelligence Platform - Home", layout="wide")

st.title("🔐 Intelligence Platform — Login")

# connect db
conn = connect_database()

if 'users_initialized' not in st.session_state:
    st.session_state['users_initialized'] = True

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
            st.experimental_rerun()
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
