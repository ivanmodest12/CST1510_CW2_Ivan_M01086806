"""
Cybersecurity Page - Manage security incidents
Refactored from procedural code to OOP
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from services.database_manager import DatabaseManager
from models.security_incident import SecurityIncident

def show_cybersecurity(db_manager: DatabaseManager):
    """
    Display cybersecurity page
    
    Args:
        db_manager: DatabaseManager instance
    """
    st.title("🛡️ Cybersecurity Incident Management")
    
    tab1, tab2, tab3 = st.tabs(["View Incidents", "Add Incident", "Incident Analytics"])
    
    with tab1:
        st.subheader("Security Incidents")
        
        try:
            # Fetch incidents using OOP
            incidents_data = db_manager.fetch_all("SELECT * FROM cyber_incidents ORDER BY date DESC")
            incidents = [SecurityIncident(**data) for data in incidents_data]
            
            if incidents:
                # Convert to DataFrame for display
                incidents_df = pd.DataFrame([incident.to_dict() for incident in incidents])
                
                # Allow filtering
                status_filter = st.selectbox(
                    "Filter by Status",
                    ["All", "Open", "In Progress", "Resolved", "Closed"]
                )
                
                if status_filter != "All":
                    incidents_df = incidents_df[incidents_df['status'] == status_filter]
                
                # Display table
                st.dataframe(incidents_df, use_container_width=True)
                
                # Incident details and actions
                st.subheader("Incident Actions")
                selected_id = st.selectbox(
                    "Select Incident ID to Manage",
                    incidents_df['id'].tolist()
                )
                
                if selected_id:
                    selected_incident = next((i for i in incidents if i.id == selected_id), None)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        new_status = st.selectbox(
                            "Update Status",
                            SecurityIncident.STATUS_VALUES,
                            index=SecurityIncident.STATUS_VALUES.index(selected_incident.status)
                        )
                        if st.button("Update Status") and new_status != selected_incident.status:
                            selected_incident.update_status(new_status)
                            db_manager.update('cyber_incidents', selected_id, {'status': new_status})
                            st.success(f"Status updated to {new_status}")
                            st.rerun()
                    
                    with col2:
                        if st.button("Delete Incident", type="secondary"):
                            if db_manager.delete('cyber_incidents', selected_id):
                                st.success("Incident deleted")
                                st.rerun()
            else:
                st.info("No security incidents found. Add some using the 'Add Incident' tab.")
                
        except Exception as e:
            st.error(f"Error loading incidents: {e}")
    
    with tab2:
        st.subheader("Add New Security Incident")
        
        with st.form("add_incident_form"):
            title = st.text_input("Incident Title*", placeholder="e.g., Phishing Attack")
            severity = st.selectbox(
                "Severity*",
                SecurityIncident.SEVERITY_LEVELS,
                index=1  # Medium as default
            )
            status = st.selectbox(
                "Status*",
                SecurityIncident.STATUS_VALUES,
                index=0  # Open as default
            )
            description = st.text_area("Description", placeholder="Detailed description of the incident...")
            reported_by = st.text_input("Reported By", placeholder="Your name or department")
            date = st.date_input("Incident Date", datetime.now())
            
            submitted = st.form_submit_button("Add Incident")
            
            if submitted:
                if not title:
                    st.error("Title is required!")
                else:
                    # Create incident object
                    incident = SecurityIncident(
                        title=title,
                        severity=severity,
                        status=status,
                        description=description,
                        reported_by=reported_by or "Anonymous",
                        date=date.strftime("%Y-%m-%d")
                    )
                    
                    # Save to database
                    incident_id = db_manager.insert('cyber_incidents', incident.to_dict())
                    if incident_id:
                        st.success(f"Incident added successfully! ID: {incident_id}")
                        st.rerun()
                    else:
                        st.error("Failed to add incident")
    
    with tab3:
        st.subheader("Incident Analytics")
        
        try:
            incidents_data = db_manager.fetch_all("SELECT * FROM cyber_incidents")
            if incidents_data:
                incidents_df = pd.DataFrame(incidents_data)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Incidents by Severity")
                    severity_counts = incidents_df['severity'].value_counts()
                    st.bar_chart(severity_counts)
                
                with col2:
                    st.subheader("Incidents by Status")
                    status_counts = incidents_df['status'].value_counts()
                    st.bar_chart(status_counts)
                
                # Trend analysis
                if 'date' in incidents_df.columns and not incidents_df['date'].isna().all():
                    st.subheader("Incidents Over Time")
                    incidents_df['date'] = pd.to_datetime(incidents_df['date'], errors='coerce')
                    daily_incidents = incidents_df.groupby(incidents_df['date'].dt.date).size()
                    st.line_chart(daily_incidents)
            else:
                st.info("No incident data available for analytics")
                
        except Exception as e:
            st.error(f"Error in analytics: {e}")