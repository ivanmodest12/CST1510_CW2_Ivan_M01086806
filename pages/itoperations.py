"""
IT Operations Page - Manage IT support tickets
Refactored from procedural code to OOP
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from services.database_manager import DatabaseManager
from models.it_ticket import ITTicket

def show_itops(db_manager: DatabaseManager):
    """
    Display IT operations page
    
    Args:
        db_manager: DatabaseManager instance
    """
    st.title("💻 IT Operations Ticket Management")
    
    tab1, tab2, tab3 = st.tabs(["View Tickets", "Add Ticket", "Ticket Analytics"])
    
    with tab1:
        st.subheader("IT Support Tickets")
        
        try:
            # Fetch tickets using OOP
            tickets_data = db_manager.fetch_all("SELECT * FROM it_tickets ORDER BY created_date DESC")
            tickets = [ITTicket(**data) for data in tickets_data]
            
            if tickets:
                # Convert to DataFrame for display
                tickets_df = pd.DataFrame([ticket.to_dict() for ticket in tickets])
                
                # Filter options
                col1, col2 = st.columns(2)
                with col1:
                    status_filter = st.selectbox(
                        "Filter by Status",
                        ["All"] + ITTicket.STATUS_VALUES
                    )
                
                with col2:
                    priority_filter = st.selectbox(
                        "Filter by Priority",
                        ["All"] + ITTicket.PRIORITY_LEVELS
                    )
                
                # Apply filters
                if status_filter != "All":
                    tickets_df = tickets_df[tickets_df['status'] == status_filter]
                
                if priority_filter != "All":
                    tickets_df = tickets_df[tickets_df['priority'] == priority_filter]
                
                # Display table
                st.dataframe(tickets_df, use_container_width=True)
                
                # Ticket management
                st.subheader("Ticket Management")
                selected_id = st.selectbox(
                    "Select Ticket ID to Manage",
                    tickets_df['id'].tolist()
                )
                
                if selected_id:
                    selected_ticket = next((t for t in tickets if t.id == selected_id), None)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        new_status = st.selectbox(
                            "Update Status",
                            ITTicket.STATUS_VALUES,
                            index=ITTicket.STATUS_VALUES.index(selected_ticket.status)
                        )
                        if st.button("Update Status") and new_status != selected_ticket.status:
                            selected_ticket.update_status(new_status)
                            db_manager.update('it_tickets', selected_id, {'status': new_status})
                            st.success(f"Status updated to {new_status}")
                            st.rerun()
                    
                    with col2:
                        new_assignee = st.text_input(
                            "Assign To",
                            value=selected_ticket.assigned_to or ""
                        )
                        if st.button("Assign") and new_assignee != selected_ticket.assigned_to:
                            selected_ticket.assign_to(new_assignee)
                            db_manager.update('it_tickets', selected_id, {'assigned_to': new_assignee})
                            st.success(f"Assigned to {new_assignee}")
                            st.rerun()
                    
                    with col3:
                        if st.button("Close Ticket", type="secondary"):
                            selected_ticket.close_ticket()
                            db_manager.update('it_tickets', selected_id, {'status': 'Closed'})
                            st.success("Ticket closed")
                            st.rerun()
            else:
                st.info("No IT tickets found. Add some using the 'Add Ticket' tab.")
                
        except Exception as e:
            st.error(f"Error loading tickets: {e}")
    
    with tab2:
        st.subheader("Create New IT Ticket")
        
        with st.form("add_ticket_form"):
            title = st.text_input("Ticket Title*", placeholder="e.g., Printer not working")
            priority = st.selectbox(
                "Priority*",
                ITTicket.PRIORITY_LEVELS,
                index=1  # Medium as default
            )
            status = st.selectbox(
                "Status*",
                ITTicket.STATUS_VALUES,
                index=0  # Open as default
            )
            assigned_to = st.text_input("Assign To", placeholder="Staff name or department")
            description = st.text_area("Description*", placeholder="Detailed description of the issue...")
            created_date = st.date_input("Date Created", datetime.now())
            
            submitted = st.form_submit_button("Create Ticket")
            
            if submitted:
                if not title:
                    st.error("Title is required!")
                elif not description:
                    st.error("Description is required!")
                else:
                    # Create ticket object
                    ticket = ITTicket(
                        title=title,
                        priority=priority,
                        status=status,
                        assigned_to=assigned_to or "Unassigned",
                        description=description,
                        created_date=created_date.strftime("%Y-%m-%d")
                    )
                    
                    # Save to database
                    ticket_id = db_manager.insert('it_tickets', ticket.to_dict())
                    if ticket_id:
                        st.success(f"Ticket created successfully! ID: {ticket_id}")
                        st.rerun()
                    else:
                        st.error("Failed to create ticket")
    
    with tab3:
        st.subheader("Ticket Analytics")
        
        try:
            tickets_data = db_manager.fetch_all("SELECT * FROM it_tickets")
            if tickets_data:
                tickets_df = pd.DataFrame(tickets_data)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Tickets by Priority")
                    priority_counts = tickets_df['priority'].value_counts()
                    st.bar_chart(priority_counts)
                
                with col2:
                    st.subheader("Tickets by Status")
                    status_counts = tickets_df['status'].value_counts()
                    st.bar_chart(status_counts)
                
                # Resolution time analysis
                if 'created_date' in tickets_df.columns and 'status' in tickets_df.columns:
                    st.subheader("Resolution Trends")
                    # For demo - would need actual resolution dates in real implementation
                    open_tickets = len(tickets_df[tickets_df['status'] == 'Open'])
                    in_progress = len(tickets_df[tickets_df['status'] == 'In Progress'])
                    resolved = len(tickets_df[tickets_df['status'] == 'Resolved'])
                    closed = len(tickets_df[tickets_df['status'] == 'Closed'])
                    
                    resolution_data = pd.DataFrame({
                        'Status': ['Open', 'In Progress', 'Resolved', 'Closed'],
                        'Count': [open_tickets, in_progress, resolved, closed]
                    })
                    st.bar_chart(resolution_data.set_index('Status'))
            else:
                st.info("No ticket data available for analytics")
                
        except Exception as e:
            st.error(f"Error in analytics: {e}")