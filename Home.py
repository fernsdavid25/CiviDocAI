# Home.py
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Government Document Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        height: 100px;
        font-size: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
    }
    .feature-icon {
        font-size: 24px;
        margin-right: 10px;
    }
    h1 {
        padding: 1rem 0;
    }
    h3 {
        padding: 0.5rem 0;
    }
    .highlight {
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Header Section
    col1, col2 = st.columns([2,1])
    with col1:
        st.title("🏛️ Government Document Assistant")
        st.markdown("""
        <p style='font-size: 1.2em;'>
        Your comprehensive AI-powered assistant for understanding, creating, and managing government documents.
        </p>
        """, unsafe_allow_html=True)
    
    # Quick Access Section
    st.markdown("### 🚀 Quick Access")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Document Analysis\n\nUnderstand & process documents", key="analyze"):
            st.switch_page("pages/Document_Analysis.py")
    
    with col2:
        if st.button("✍️ Writing Assistant\n\nCreate government documents", key="write"):
            st.switch_page("pages/Writing_Assistant.py")
    
    with col3:
        if st.button("💬 Interactive Chat\n\nGet real-time assistance", key="chat"):
            st.switch_page("pages/Document_Chat.py")

    # Main Features Section
    st.markdown("---")
    st.markdown("### 🌟 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("""
            <div class='feature-card'>
                <h3>📑 Document Analysis</h3>
                <ul>
                    <li>Upload government documents (PDFs, images)</li>
                    <li>Get instant analysis and explanations</li>
                    <li>Understand complex terminology</li>
                    <li>Extract key requirements and deadlines</li>
                    <li>Step-by-step form filling guidance</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='feature-card'>
                    <h3>✍️ Writing Assistant</h3>
                    <ul>
                        <li>Generate RTI applications</li>
                        <li>Create complaint letters</li>
                        <li>Draft legal notices</li>
                        <li>Write appeal letters</li>
                        <li>Format government applications</li>
                        <li>Custom document templates</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown("""
            <div class='feature-card'>
                <h3>💬 Interactive Help</h3>
                <ul>
                    <li>Chat with AI about your documents</li>
                    <li>Get instant answers to queries</li>
                    <li>Understand procedures better</li>
                    <li>Clarify doubts in real-time</li>
                    <li>Multi-document context support</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            with st.container():
                st.markdown("""
                <div class='feature-card'>
                    <h3>📚 Document Management</h3>
                    <ul>
                        <li>Organize all your documents</li>
                        <li>Track application status</li>
                        <li>Access document history</li>
                        <li>Download processed documents</li>
                        <li>Secure document storage</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

    # How It Works Section
    st.markdown("---")
    st.markdown("### 🔄 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card' style='text-align: center;'>
            <h4>1. Upload or Create</h4>
            <p>Upload existing documents or create new ones using our templates</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card' style='text-align: center;'>
            <h4>2. Process & Analyze</h4>
            <p>Our AI analyzes and helps you understand the content</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card' style='text-align: center;'>
            <h4>3. Get Assistance</h4>
            <p>Receive guidance, explanations, and next steps</p>
        </div>
        """, unsafe_allow_html=True)

    # Additional Information
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Who Is This For?")
        st.markdown("""
        - Citizens dealing with government procedures
        - Individuals filing RTI applications
        - People seeking government services
        - Anyone needing help with official documents
        """)
    
    with col2:
        st.markdown("### 🛡️ Privacy & Security")
        st.markdown("""
        - Secure document processing
        - No permanent storage of sensitive data
        - End-to-end encryption
        - Privacy-first approach
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6B7280; padding: 1rem;'>
        <p>Need help? Start with Document Analysis or use our Writing Assistant</p>
        <p style='font-size: 0.8em;'>Government Document Assistant - Making bureaucracy simpler</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()