# pages/2_Writing_Assistant.py
import streamlit as st
from theme import apply_dark_theme, show_page_header, show_footer
from utils import initialize_session_state, generate_document, save_to_history
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Writing Assistant | CiviDoc AI",
    page_icon="✍️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Apply dark theme
st.markdown(apply_dark_theme(), unsafe_allow_html=True)

def writing_assistant_page():
    # Initialize states
    initialize_session_state()
    
    # Header
    st.markdown(show_page_header(
        "✍️ Writing Assistant",
        "Create professional government documents effortlessly"
    ), unsafe_allow_html=True)
    
    # Document Type Selection
    st.markdown(
        "<div class='card'>"
        "<h3>Select Document Type</h3>"
        "<p>Choose the type of document you need to create</p>"
        "</div>",
        unsafe_allow_html=True
    )
    
    doc_types = {
        "RTI": "📝 RTI Application",
        "COMPLAINT": "📢 Complaint Letter",
        "LEGAL": "⚖️ Legal Notice",
        "APPEAL": "📨 Appeal Letter",
        "PERMISSION": "🔑 Permission Request",
        "APPLICATION": "📋 Government Application",
        "CUSTOM": "✒️ Custom Document"
    }
    
    # Mobile-friendly document type selector with icons
    selected_type = st.selectbox(
        "Document Type",
        options=list(doc_types.keys()),
        format_func=lambda x: doc_types[x],
        key="doc_type_selector"
    )
    
    # Common Fields Section - Always visible
    st.markdown(
        "<div class='card'>"
        "<h4>Personal Information</h4>",
        unsafe_allow_html=True
    )
    
    name = st.text_input("Full Name", placeholder="Enter your full name")
    address = st.text_area("Address", placeholder="Enter your complete address")
    contact = st.text_input("Contact Number", placeholder="Enter your contact number")
    email = st.text_input("Email Address", placeholder="Enter your email address")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Dynamic Form Based on Selection
    if selected_type == "RTI":
        show_rti_form(name, address, contact, email)
    elif selected_type == "COMPLAINT":
        show_complaint_form(name, address, contact, email)
    elif selected_type == "LEGAL":
        show_legal_notice_form(name, address, contact, email)
    elif selected_type == "APPEAL":
        show_appeal_form(name, address, contact, email)
    elif selected_type == "PERMISSION":
        show_permission_form(name, address, contact, email)
    elif selected_type == "APPLICATION":
        show_application_form(name, address, contact, email)
    else:  # CUSTOM
        show_custom_form(name, address, contact, email)

def show_rti_form(name, address, contact, email):
    """RTI Application Form"""
    st.markdown(
        "<div class='card'>"
        "<h4>RTI Application Details</h4>",
        unsafe_allow_html=True
    )
    
    department = st.text_input("Department/Authority Name", placeholder="Enter department name")
    subject = st.text_input("Subject of Information", placeholder="Enter subject")
    
    st.markdown("<div class='touch-spacing'>", unsafe_allow_html=True)
    information = st.text_area(
        "Information Required",
        placeholder="Clearly specify the information you are seeking...",
        height=150
    )
    
    time_period = st.text_input(
        "Time Period",
        placeholder="Specify the time period for which information is sought"
    )
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    if validate_and_generate("RTI Application", locals()):
        st.balloons()

def show_complaint_form(name, address, contact, email):
    """Complaint Letter Form"""
    st.markdown(
        "<div class='card'>"
        "<h4>Complaint Details</h4>",
        unsafe_allow_html=True
    )
    
    authority = st.text_input("Authority/Department Name", placeholder="Enter authority name")
    
    complaint_types = [
        "Public Service",
        "Infrastructure",
        "Government Employee",
        "Civic Issue",
        "Other"
    ]
    
    complaint_type = st.selectbox("Type of Complaint", complaint_types)
    
    st.markdown("<div class='touch-spacing'>", unsafe_allow_html=True)
    description = st.text_area(
        "Complaint Description",
        placeholder="Describe your complaint in detail...",
        height=150
    )
    
    previous_complaints = st.text_area(
        "Previous Complaints (if any)",
        placeholder="Mention any previous complaints filed regarding this issue..."
    )
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    if validate_and_generate("Complaint Letter", locals()):
        st.balloons()

def show_legal_notice_form(name, address, contact, email):
    """Legal Notice Form"""
    st.markdown(
        "<div class='card'>"
        "<h4>Legal Notice Details</h4>",
        unsafe_allow_html=True
    )
    
    recipient = st.text_input("Notice To (Name/Department)", placeholder="Enter recipient's name")
    recipient_address = st.text_area("Recipient's Address", placeholder="Enter recipient's address")
    
    st.markdown("<div class='touch-spacing'>", unsafe_allow_html=True)
    subject = st.text_input("Subject of Notice", placeholder="Enter notice subject")
    cause = st.text_area(
        "Cause of Action",
        placeholder="Describe the reason for this legal notice...",
        height=100
    )
    
    relief_sought = st.text_area(
        "Relief Sought",
        placeholder="Specify what action you want taken...",
        height=100
    )
    
    time_period = st.number_input(
        "Response Time Period (in days)",
        min_value=1,
        value=15
    )
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    if validate_and_generate("Legal Notice", locals()):
        st.balloons()

def show_appeal_form(name, address, contact, email):
    """Appeal Letter Form"""
    st.markdown(
        "<div class='card'>"
        "<h4>Appeal Details</h4>",
        unsafe_allow_html=True
    )
    
    authority = st.text_input("Appellate Authority", placeholder="Enter authority name")
    reference = st.text_input("Previous Reference/Order Number", placeholder="Enter reference number")
    
    st.markdown("<div class='touch-spacing'>", unsafe_allow_html=True)
    order_date = st.date_input("Date of Previous Order")
    
    grounds = st.text_area(
        "Grounds for Appeal",
        placeholder="Explain the reasons for your appeal...",
        height=150
    )
    
    relief = st.text_area(
        "Relief Sought",
        placeholder="Specify what you are seeking through this appeal...",
        height=100
    )
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    if validate_and_generate("Appeal Letter", locals()):
        st.balloons()

def show_permission_form(name, address, contact, email):
    """Permission Request Form"""
    st.markdown(
        "<div class='card'>"
        "<h4>Permission Request Details</h4>",
        unsafe_allow_html=True
    )
    
    authority = st.text_input("Authority Name", placeholder="Enter authority name")
    purpose = st.text_input("Purpose of Request", placeholder="Enter the purpose")
    
    st.markdown("<div class='touch-spacing'>", unsafe_allow_html=True)
    details = st.text_area(
        "Request Details",
        placeholder="Provide detailed information about your request...",
        height=150
    )
    
    duration = st.text_input("Duration (if applicable)", placeholder="Specify time period")
    location = st.text_input("Location (if applicable)", placeholder="Specify location")
    
    undertaking = st.text_area(
        "Undertaking/Declaration",
        placeholder="Any declarations or undertakings...",
        height=100
    )
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    if validate_and_generate("Permission Request", locals()):
        st.balloons()

def show_application_form(name, address, contact, email):
    """Government Application Form"""
    st.markdown(
        "<div class='card'>"
        "<h4>Application Details</h4>",
        unsafe_allow_html=True
    )
    
    department = st.text_input("Department Name", placeholder="Enter department name")
    purpose = st.text_input("Purpose of Application", placeholder="Enter purpose")
    
    application_types = [
        "License",
        "Certificate",
        "Registration",
        "Permit",
        "Other"
    ]
    
    app_type = st.selectbox("Application Type", application_types)
    
    st.markdown("<div class='touch-spacing'>", unsafe_allow_html=True)
    details = st.text_area(
        "Application Details",
        placeholder="Provide detailed information...",
        height=150
    )
    
    supporting_docs = st.text_area(
        "Supporting Documents",
        placeholder="List all supporting documents...",
        height=100
    )
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    if validate_and_generate("Government Application", locals()):
        st.balloons()

def show_custom_form(name, address, contact, email):
    """Custom Document Form"""
    st.markdown(
        "<div class='card'>"
        "<h4>Custom Document Details</h4>",
        unsafe_allow_html=True
    )
    
    title = st.text_input("Document Title", placeholder="Enter document title")
    recipient = st.text_input("Recipient/Authority", placeholder="Enter recipient name")
    
    st.markdown("<div class='touch-spacing'>", unsafe_allow_html=True)
    subject = st.text_input("Subject", placeholder="Enter subject")
    
    content = st.text_area(
        "Document Content",
        placeholder="Enter the main content of your document...",
        height=300
    )
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    if validate_and_generate("Custom Document", locals()):
        st.balloons()

def validate_and_generate(doc_type, fields):
    """Validate fields and generate document"""
    if st.button(f"Generate {doc_type}", use_container_width=True):
        # Basic validation
        required_fields = {k: v for k, v in fields.items() 
                         if k not in ['st', 'contact', 'email']}
        
        empty_fields = [k for k, v in required_fields.items() 
                       if not v or (isinstance(v, str) and not v.strip())]
        
        if empty_fields:
            st.error(
                f"Please fill in all required fields: "
                f"{', '.join(empty_fields)}"
            )
            return False
        
        try:
            with st.spinner("Generating document..."):
                # Generate document
                generated_content = generate_document(doc_type, fields)
                
                # Save to history
                timestamp = datetime.now()
                doc_name = f"{doc_type}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
                save_to_history(doc_name, doc_type, generated_content, timestamp)
                
                # Show success message
                st.success("Document generated successfully!")
                
                # Display generated document
                st.markdown(
                    "<div class='card'>"
                    "<h4>Generated Document</h4>"
                    f"<pre style='white-space: pre-wrap;'>{generated_content}</pre>"
                    "</div>",
                    unsafe_allow_html=True
                )
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📥 Download Document",
                        generated_content,
                        file_name=f"{doc_name}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    if st.button("📋 Create Another", use_container_width=True):
                        st.rerun()
                
                return True
                
        except Exception as e:
            st.error(f"Error generating document: {str(e)}")
            return False
    
    return False

if __name__ == "__main__":
    writing_assistant_page()
