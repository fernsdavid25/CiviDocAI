# pages/3_Document_Chat.py
import streamlit as st
from utils import create_chat_engine, initialize_session_state

def document_chat_page():
    st.title("💬 Document Chat")
    
    # Initialize states
    initialize_session_state()
    
    if st.session_state.chat_engines:
        # Document selector
        doc_names = list(st.session_state.chat_engines.keys())
        selected_doc = st.selectbox(
            "Select document to discuss:",
            doc_names,
            key="doc_selector"
        )
        
        # Display document content
        if selected_doc:
            with st.expander("Document Content", expanded=False):
                if selected_doc in st.session_state.analyses:
                    st.markdown(st.session_state.analyses[selected_doc]['analysis'])
                else:
                    st.info("Original document content not available")
        
        # Chat interface
        display_chat_interface(selected_doc)
        
        # Additional actions
        st.sidebar.subheader("Chat Actions")
        if st.sidebar.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        if st.sidebar.button("View Document History"):
            st.switch_page("pages/Document_History.py")
            
    else:
        st.info("Please analyze documents first in the Document Analysis section.")
        if st.button("Go to Document Analysis"):
            st.switch_page("pages/Document_Analysis.py")

def display_chat_interface(selected_doc):
    """Display the chat interface for a selected document"""
    st.subheader(f"Chatting about: {selected_doc}")
    
    # Initialize chat message list for the selected document
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display the chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    # User input for new chat message
    if prompt := st.chat_input("Ask a question about the document:"):
        # User message
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Retrieve chat engine and get response
        chat_engine = st.session_state.chat_engines[selected_doc]
        with st.spinner("Thinking..."):
            try:
                response = chat_engine.chat(prompt)
                assistant_response = response.response
                st.session_state.messages.append({
                    'role': 'assistant', 
                    'content': assistant_response
                })
                with st.chat_message("assistant"):
                    st.markdown(assistant_response)
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
                # Remove the failed message from history
                st.session_state.messages.pop()

def suggest_questions(doc_type):
    """Suggest relevant questions based on document type"""
    suggestions = {
        'application/pdf': [
            "What are the main requirements in this document?",
            "What are the important deadlines?",
            "Can you explain the technical terms used?",
            "What supporting documents are needed?"
        ],
        'image/jpeg': [
            "What type of form is this?",
            "How do I fill out this form?",
            "What are the submission instructions?",
            "Are there any special requirements?"
        ]
    }
    return suggestions.get(doc_type, [
        "What is this document about?",
        "What are the next steps?",
        "Can you explain this in simpler terms?",
        "What action is required from me?"
    ])

if __name__ == "__main__":
    document_chat_page()