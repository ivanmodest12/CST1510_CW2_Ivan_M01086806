import streamlit as st
from app.data.db import connect_database
from app.data.users import get_user_role

st.set_page_config(page_title="Settings", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    st.stop()

conn = connect_database()

st.title("⚙️ Settings")
st.write(f"Current user: {st.session_state.get('username')}")
try:
    role = get_user_role(conn, st.session_state.get('username'))
    st.write(f"Role: {role}")
except Exception:
    st.write("Could not fetch role from DB (not critical for demo).")

if st.button("Delete local demo DB (reset)"):
    import os
    dbfile = conn.execute('PRAGMA database_list').fetchall()[0]['file']
    conn.close()
    if os.path.exists(dbfile):
        os.remove(dbfile)
        st.success("Database removed. Reload the app.")
    else:
        st.warning("DB file not found.")
