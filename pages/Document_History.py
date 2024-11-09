# pages/4_Document_History.py
import streamlit as st
import pandas as pd
from datetime import datetime
from utils import initialize_session_state, get_document_history, delete_from_history, format_timestamp

def document_history_page():
    st.title("📚 Document History")
    initialize_session_state()
    
    # Create DataFrame from document history
    if st.session_state.document_history:
        history_data = []
        for doc_name, details in get_document_history().items():
            history_data.append({
                'Document Name': doc_name,
                'Type': details['type'],
                'Date': format_timestamp(details['timestamp']),
                'Status': details['status']
            })
        
        df = pd.DataFrame(history_data)
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            doc_type_filter = st.multiselect(
                "Filter by Document Type",
                options=df['Type'].unique(),
                default=[]
            )
        
        with col2:
            date_range = st.date_input(
                "Filter by Date Range",
                value=(datetime.now().date(), datetime.now().date()),
                key="date_range"
            )
        
        # Apply filters
        filtered_df = df.copy()
        if doc_type_filter:
            filtered_df = filtered_df[filtered_df['Type'].isin(doc_type_filter)]
        if len(date_range) == 2:
            filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
            mask = (filtered_df['Date'].dt.date >= date_range[0]) & (filtered_df['Date'].dt.date <= date_range[1])
            filtered_df = filtered_df[mask]
        
        # Display interactive table
        st.dataframe(
            filtered_df,
            column_config={
                "Document Name": st.column_config.TextColumn(
                    "Document Name",
                    width="medium",
                ),
                "Type": st.column_config.TextColumn(
                    "Type",
                    width="small",
                ),
                "Date": st.column_config.TextColumn(
                    "Processing Date",
                    width="small",
                ),
                "Status": st.column_config.TextColumn(
                    "Status",
                    width="small",
                ),
            },
            hide_index=True,
        )
        
        # Document Details Section
        st.subheader("Document Details")
        selected_doc = st.selectbox(
            "Select a document to view details",
            options=df['Document Name'].tolist()
        )
        
        if selected_doc:
            doc_details = st.session_state.document_history[selected_doc]
            
            col1, col2, col3 = st.columns([2,2,1])
            with col1:
                st.markdown(f"**Type:** {doc_details['type']}")
                st.markdown(f"**Processed on:** {format_timestamp(doc_details['timestamp'])}")
            
            with col2:
                st.markdown(f"**Status:** {doc_details['status']}")
            
            with col3:
                if st.button("Delete Document", key=f"delete_{selected_doc}"):
                    delete_from_history(selected_doc)
                    st.rerun()
            
            # Display document content
            with st.expander("Document Content", expanded=True):
                st.markdown(doc_details['content'])
            
            # Actions
            st.subheader("Actions")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Chat about Document", use_container_width=True):
                    st.session_state.current_doc = selected_doc
                    st.switch_page("pages/Document_Chat.py")
            
            with col2:
                if st.button("Download Document", use_container_width=True):
                    # Create downloadable version
                    content = doc_details['content']
                    st.download_button(
                        label="Download",
                        data=content.encode(),
                        file_name=f"{selected_doc}.txt",
                        mime="text/plain"
                    )
            
            with col3:
                if st.button("Share Document", use_container_width=True):
                    # Generate shareable link or copy to clipboard
                    st.info("Document sharing functionality coming soon!")
    
    else:
        st.info("No documents in history. Start by analyzing or creating documents!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Analyze Documents", use_container_width=True):
                st.switch_page("pages/Document_Analysis.py")
        
        with col2:
            if st.button("Create New Document", use_container_width=True):
                st.switch_page("pages/Writing_Assistant.py")

if __name__ == "__main__":
    document_history_page()
