"""
Multi-Domain Intelligence Platform - OOP Refactoring
Week 11: Object-Oriented Programming Project
"""
import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
from services.ai_assistant import AIAssistant

# Page config
st.set_page_config(page_title="Multi-Domain Platform", layout="wide")

# Initialize services
@st.cache_resource
def get_db_manager():
    return DatabaseManager()

@st.cache_resource  
def get_auth_manager():
    return AuthManager(get_db_manager())

@st.cache_resource
def get_ai_assistant():
    return AIAssistant()

# Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

# Get services
db_manager = get_db_manager()
auth_manager = get_auth_manager()
ai_assistant = get_ai_assistant()

def main():
    if not st.session_state.logged_in:
        show_login_page()
    else:
        show_main_app()

def show_login_page():
    st.title("🔐 Multi-Domain Intelligence Platform")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if auth_manager.login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    with tab2:
        st.subheader("Register")
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        
        if st.button("Create Account"):
            if new_pass == confirm:
                if auth_manager.register(new_user, new_pass):
                    st.success("Account created! Please login.")
                else:
                    st.error("Username already exists")
            else:
                st.error("Passwords don't match")

def show_main_app():
    with st.sidebar:
        st.title(f"👋 {st.session_state.username}")
        st.markdown("---")
        
        # Simple navigation - using selectbox
        page_options = ["Dashboard", "🛡️ Cybersecurity", "📊 Data Science", "💻 IT Operations", "🤖 AI Assistant"]
        page = st.selectbox("Go to Page", page_options)
        
        # Map selection to actual page
        if page == "Dashboard":
            st.session_state.current_page = "dashboard"
        elif page == "🛡️ Cybersecurity":
            st.session_state.current_page = "cybersecurity"
        elif page == "📊 Data Science":
            st.session_state.current_page = "datascience"
        elif page == "💻 IT Operations":
            st.session_state.current_page = "itops"
        elif page == "🤖 AI Assistant":
            st.session_state.current_page = "ai_assistant"
        
        st.markdown("---")
        
        # Quick stats
        try:
            incidents = len(db_manager.fetch_all("SELECT id FROM cyber_incidents"))
            datasets = len(db_manager.fetch_all("SELECT id FROM datasets_metadata"))
            tickets = len(db_manager.fetch_all("SELECT id FROM it_tickets"))
            
            st.subheader("📈 Quick Stats")
            st.metric("Incidents", incidents)
            st.metric("Datasets", datasets)
            st.metric("Tickets", tickets)
        except:
            pass
        
        st.markdown("---")
        
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    
    # Load the selected page
    try:
        # Show Dashboard by default
        if st.session_state.current_page == "dashboard":
            st.title("📊 Dashboard")
            st.write(f"Welcome to the Dashboard, {st.session_state.username}!")
            
            # Show quick overview
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Active Incidents", 
                         len(db_manager.fetch_all("SELECT id FROM cyber_incidents WHERE status IN ('Open', 'In Progress')")))
            with col2:
                st.metric("Total Datasets", 
                         len(db_manager.fetch_all("SELECT id FROM datasets_metadata")))
            with col3:
                st.metric("Open Tickets", 
                         len(db_manager.fetch_all("SELECT id FROM it_tickets WHERE status IN ('Open', 'In Progress')")))
            
            st.info("Select a domain page from the sidebar to manage data.")
            
        elif st.session_state.current_page == "cybersecurity":
            from pages.cybersecurity import show_cybersecurity
            show_cybersecurity(db_manager)
        elif st.session_state.current_page == "datascience":
            from pages.datascience import show_datascience
            show_datascience(db_manager)
        elif st.session_state.current_page == "itops":
            from pages.itoperations import show_itops
            show_itops(db_manager)
        elif st.session_state.current_page == "ai_assistant":
            from pages.ai_assistant import show_ai_assistant
            show_ai_assistant(db_manager)
    except Exception as e:
        st.error(f"Error loading page: {e}")
        st.info(f"Current page: {st.session_state.current_page}")

if __name__ == "__main__":
    main()