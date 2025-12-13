"""
Data Science Page - Manage datasets
Refactored from procedural code to OOP
"""
import streamlit as st
import pandas as pd
from services.database_manager import DatabaseManager
from models.dataset import Dataset

def show_datascience(db_manager: DatabaseManager):
    """
    Display data science page
    
    Args:
        db_manager: DatabaseManager instance
    """
    st.title("📊 Data Science Dataset Management")
    
    tab1, tab2 = st.tabs(["View Datasets", "Add Dataset"])
    
    with tab1:
        st.subheader("Available Datasets")
        
        try:
            # Fetch datasets using OOP
            datasets_data = db_manager.fetch_all("SELECT * FROM datasets_metadata ORDER BY created_at DESC")
            datasets = [Dataset(**data) for data in datasets_data]
            
            if datasets:
                # Convert to DataFrame for display
                datasets_df = pd.DataFrame([dataset.to_dict() for dataset in datasets])
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    total_datasets = len(datasets)
                    st.metric("Total Datasets", total_datasets)
                with col2:
                    total_size_gb = sum(dataset.calculate_size_gb() for dataset in datasets)
                    st.metric("Total Size", f"{total_size_gb:.2f} GB")
                with col3:
                    categories = datasets_df['category'].nunique()
                    st.metric("Categories", categories)
                
                # Filter options
                col1, col2 = st.columns(2)
                with col1:
                    category_filter = st.selectbox(
                        "Filter by Category",
                        ["All"] + datasets_df['category'].dropna().unique().tolist()
                    )
                
                with col2:
                    size_threshold = st.slider(
                        "Minimum Size (MB)",
                        0, 10000,
                        0,
                        help="Filter datasets larger than this size"
                    )
                
                # Apply filters
                if category_filter != "All":
                    datasets_df = datasets_df[datasets_df['category'] == category_filter]
                
                if size_threshold > 0:
                    datasets_df = datasets_df[datasets_df['size_mb'] >= size_threshold]
                
                # Display table
                st.dataframe(
                    datasets_df[['name', 'category', 'size_mb', 'source', 'created_at']],
                    use_container_width=True
                )
                
                # Dataset details
                st.subheader("Dataset Details")
                if not datasets_df.empty:
                    selected_name = st.selectbox(
                        "Select Dataset",
                        datasets_df['name'].tolist()
                    )
                    
                    if selected_name:
                        selected_dataset = next((d for d in datasets if d.name == selected_name), None)
                        if selected_dataset:
                            with st.expander("View Full Details"):
                                st.json(selected_dataset.to_dict())
            else:
                st.info("No datasets found. Add some using the 'Add Dataset' tab.")
                
        except Exception as e:
            st.error(f"Error loading datasets: {e}")
    
    with tab2:
        st.subheader("Add New Dataset")
        
        with st.form("add_dataset_form"):
            name = st.text_input("Dataset Name*", placeholder="e.g., Customer Behavior Data")
            source = st.text_input("Data Source", placeholder="e.g., Internal Database, API, CSV file")
            category = st.selectbox(
                "Category",
                ["Raw Data", "Processed", "Analytics", "Training", "Testing", "Validation", "Other"]
            )
            size = st.number_input("Size in Bytes*", min_value=0, value=1000000)
            description = st.text_area("Description", placeholder="Describe the dataset contents, format, and usage...")
            
            submitted = st.form_submit_button("Add Dataset")
            
            if submitted:
                if not name:
                    st.error("Dataset name is required!")
                elif size <= 0:
                    st.error("Size must be greater than 0!")
                else:
                    # Create dataset object
                    dataset = Dataset(
                        name=name,
                        source=source,
                        category=category,
                        size=size,
                        description=description
                    )
                    
                    # Save to database
                    dataset_id = db_manager.insert('datasets_metadata', dataset.to_dict())
                    if dataset_id:
                        st.success(f"Dataset added successfully! ID: {dataset_id}")
                        st.rerun()
                    else:
                        st.error("Failed to add dataset")