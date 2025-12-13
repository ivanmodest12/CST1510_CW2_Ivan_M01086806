"""
AI Assistant Page - Get AI-powered assistance
"""
import streamlit as st
from services.ai_assistant import AIAssistant
from services.database_manager import DatabaseManager

def show_ai_assistant(db_manager: DatabaseManager):
    """
    Display AI assistant page
    
    Args:
        db_manager: DatabaseManager instance
    """
    st.title("🤖 AI Assistant")
    
    # Initialize AI Assistant
    ai_assistant = AIAssistant()
    
    # Check if OpenAI API is configured
    if not ai_assistant.client:
        st.warning("⚠️ OpenAI API not configured")
        st.info("To use the AI Assistant:")
        st.code("""
        # Create a .env file in your project root with:
        OPENAI_API_KEY=your_api_key_here
        
        # Or set it directly:
        import os
        os.environ['OPENAI_API_KEY'] = 'your_api_key_here'
        """)
    
    tab1, tab2, tab3 = st.tabs(["Chat Assistant", "Incident Analysis", "Dataset Analysis"])
    
    with tab1:
        st.subheader("Chat with AI Assistant")
        
        # Domain selection
        domain = st.selectbox(
            "Select Domain",
            ["general", "cybersecurity", "datascience", "itops"],
            format_func=lambda x: {
                "general": "General Assistance",
                "cybersecurity": "Cybersecurity",
                "datascience": "Data Science", 
                "itops": "IT Operations"
            }[x]
        )
        
        # Chat interface
        user_input = st.text_area(
            "Your Question",
            placeholder="Ask me anything about cybersecurity, data science, IT operations, or general assistance...",
            height=100
        )
        
        if st.button("Send", type="primary"):
            if user_input:
                with st.spinner("AI is thinking..."):
                    response = ai_assistant.send_message(user_input, domain)
                    
                    # Display conversation
                    st.subheader("Conversation")
                    col1, col2 = st.columns([1, 4])
                    
                    with col1:
                        st.markdown("**You:**")
                    with col2:
                        st.markdown(user_input)
                    
                    st.divider()
                    
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown("**AI:**")
                    with col2:
                        st.markdown(response)
            else:
                st.warning("Please enter a question")
        
        # Conversation history
        if ai_assistant.conversation_history:
            with st.expander("View Conversation History"):
                for i, message in enumerate(ai_assistant.conversation_history[-5:]):
                    role = "You" if message['role'] == 'user' else "AI"
                    st.markdown(f"**{role}:** {message['content']}")
                    if i < len(ai_assistant.conversation_history[-5:]) - 1:
                        st.divider()
                
                if st.button("Clear History"):
                    ai_assistant.clear_history()
                    st.rerun()
    
    with tab2:
        st.subheader("AI-Powered Incident Analysis")
        
        try:
            # Get incidents for analysis
            incidents_data = db_manager.fetch_all("SELECT * FROM cyber_incidents")
            
            if incidents_data:
                incident_options = {f"{inc['id']}: {inc['title']}": inc for inc in incidents_data}
                selected_incident_key = st.selectbox(
                    "Select Incident to Analyze",
                    list(incident_options.keys())
                )
                
                if selected_incident_key:
                    selected_incident = incident_options[selected_incident_key]
                    
                    # Display incident details
                    with st.expander("View Incident Details"):
                        st.json(selected_incident)
                    
                    if st.button("Analyze with AI"):
                        with st.spinner("AI is analyzing the incident..."):
                            analysis = ai_assistant.analyze_incident(selected_incident)
                            st.subheader("AI Analysis")
                            st.markdown(analysis)
            else:
                st.info("No incidents available for analysis. Add some in the Cybersecurity section.")
                
        except Exception as e:
            st.error(f"Error analyzing incidents: {e}")
    
    with tab3:
        st.subheader("AI-Powered Dataset Analysis")
        
        try:
            # Get datasets for analysis
            datasets_data = db_manager.fetch_all("SELECT * FROM datasets_metadata")
            
            if datasets_data:
                dataset_options = {f"{ds['id']}: {ds['name']}": ds for ds in datasets_data}
                selected_dataset_key = st.selectbox(
                    "Select Dataset to Analyze",
                    list(dataset_options.keys())
                )
                
                if selected_dataset_key:
                    selected_dataset = dataset_options[selected_dataset_key]
                    
                    # Display dataset details
                    with st.expander("View Dataset Details"):
                        st.json(selected_dataset)
                    
                    if st.button("Analyze with AI"):
                        with st.spinner("AI is analyzing the dataset..."):
                            analysis = ai_assistant.analyze_dataset(selected_dataset)
                            st.subheader("AI Analysis")
                            st.markdown(analysis)
            else:
                st.info("No datasets available for analysis. Add some in the Data Science section.")
                
        except Exception as e:
            st.error(f"Error analyzing datasets: {e}")