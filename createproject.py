# create_week11_project.py
import os
import zipfile
from pathlib import Path

def create_project_structure():
    """Creates the complete Week 11 OOP project structure"""
    
    # Define the complete project structure
    project_files = {
        "requirements.txt": """streamlit>=1.20.0
openai>=1.0.0
python-dotenv>=0.21.0
bcrypt==4.2.0
pandas>=2.0.0""",
        
        "README.md": """# Multi-Domain Intelligence Platform - OOP Refactoring

## Week 11: Object-Oriented Programming & Project Refactoring

### Features:
- ✅ OOP Architecture with SOLID principles
- ✅ Four Domains: Cybersecurity, Data Science, IT Operations, AI Assistant
- ✅ Complete authentication system
- ✅ Database persistence with SQLite
- ✅ Ready-to-run Streamlit application""",
        
        ".gitignore": """__pycache__/
*.pyc
.env
*.db
.DS_Store
.streamlit/secrets.toml""",
        
        ".streamlit/config.toml": """[theme]
primaryColor = "#1E88E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true""",
        
        "Home.py": """import streamlit as st
from services.auth_manager import AuthManager
from services.database_manager import DatabaseManager

# Page config
st.set_page_config(page_title="Multi-Domain Platform", layout="wide")

# Initialize services
db_manager = DatabaseManager()
auth_manager = AuthManager(db_manager)

# Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Main application
if not st.session_state.logged_in:
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
        confirm_pass = st.text_input("Confirm Password", type="password")
        
        if st.button("Create Account"):
            if new_pass == confirm_pass:
                if auth_manager.register(new_user, new_pass):
                    st.success("Account created! Please login.")
                else:
                    st.error("Username already exists")
            else:
                st.error("Passwords don't match")
else:
    st.title(f"🎯 Dashboard - Welcome {st.session_state.username}")
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", [
        "Dashboard",
        "Cybersecurity",
        "Data Science", 
        "IT Operations",
        "AI Assistant",
        "Settings"
    ])
    
    if page == "Dashboard":
        from pages import dashboard_page
        dashboard_page.show(db_manager)
    elif page == "Cybersecurity":
        from pages import cybersecurity_page
        cybersecurity_page.show(db_manager)
    elif page == "Data Science":
        from pages import datascience_page
        datascience_page.show(db_manager)
    elif page == "IT Operations":
        from pages import itops_page
        itops_page.show(db_manager)
    elif page == "AI Assistant":
        from pages import ai_assistant_page
        ai_assistant_page.show(db_manager)
    elif page == "Settings":
        from pages import settings_page
        settings_page.show(db_manager, auth_manager)
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()"""
    }
    
    # Create directories
    directories = [
        "models",
        "services", 
        "database",
        "pages",
        ".streamlit"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Create all files
    for file_path, content in project_files.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("✅ Project structure created successfully!")
    print("📁 Folders created: models/, services/, database/, pages/, .streamlit/")
    print("📄 Files created: requirements.txt, README.md, .gitignore, Home.py")
    print("\nTo run the project:")
    print("1. pip install -r requirements.txt")
    print("2. streamlit run Home.py")

if __name__ == "__main__":
    create_project_structure()