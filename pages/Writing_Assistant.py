# pages/2_Writing_Assistant.py
import streamlit as st
from utils import initialize_session_state, generate_document, save_to_history
from datetime import datetime

def writing_assistant_page():
    st.title("✍️ Writing Assistant")
    
    # Initialize states
    initialize_session_state()
    
    # Document type selector
    doc_type = st.selectbox(
        "What type of document do you need help with?",
        [
            "RTI Application",
            "Government Application",
            "Complaint Letter",
            "Legal Notice",
            "Appeal Letter",
            "Permission Request",
            "Custom Document"
        ]
    )
    
    # Common fields for all documents
    st.sidebar.subheader("Personal Information")
    name = st.sidebar.text_input("Your Full Name")
    address = st.sidebar.text_area("Your Address")
    contact = st.sidebar.text_input("Contact Number")
    email = st.sidebar.text_input("Email Address")
    
    # Dynamic form based on document type
    if doc_type == "RTI Application":
        rti_application_form(name, address, contact, email)
    elif doc_type == "Complaint Letter":
        complaint_letter_form(name, address, contact, email)
    elif doc_type == "Government Application":
        government_application_form(name, address, contact, email)
    elif doc_type == "Legal Notice":
        legal_notice_form(name, address, contact, email)
    elif doc_type == "Appeal Letter":
        appeal_letter_form(name, address, contact, email)
    elif doc_type == "Permission Request":
        permission_request_form(name, address, contact, email)
    else:  # Custom Document
        custom_document_form(name, address, contact, email)

def rti_application_form(name, address, contact, email):
    st.subheader("RTI Application Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        department = st.text_input("Department/Authority Name")
        subject = st.text_input("Subject of Information")
    with col2:
        state = st.selectbox("State", ["Select State", "Maharashtra", "Delhi", "Karnataka", "Other"])
        time_period = st.text_input("Time Period of Information")
    
    information = st.text_area("Information Required (Be specific)")
    
    if st.button("Generate RTI Application"):
        if not all([name, address, department, subject, information]):
            st.error("Please fill in all required fields")
            return
        
        fields = {
            "name": name,
            "address": address,
            "contact": contact,
            "email": email,
            "department": department,
            "subject": subject,
            "information": information,
            "time_period": time_period,
            "state": state
        }
        
        generate_and_save_document("RTI Application", fields)

def complaint_letter_form(name, address, contact, email):
    st.subheader("Complaint Letter Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        authority = st.text_input("Authority/Department Name")
        complaint_type = st.selectbox(
            "Type of Complaint",
            ["Public Service", "Infrastructure", "Government Employee", "Other"]
        )
    with col2:
        location = st.text_input("Location of Issue")
        date_of_incident = st.date_input("Date of Incident")
    
    description = st.text_area("Complaint Details")
    previous_complaints = st.text_area("Previous Complaints (if any)")
    
    if st.button("Generate Complaint Letter"):
        if not all([name, address, authority, description]):
            st.error("Please fill in all required fields")
            return
        
        fields = {
            "name": name,
            "address": address,
            "contact": contact,
            "email": email,
            "authority": authority,
            "complaint_type": complaint_type,
            "location": location,
            "date_of_incident": str(date_of_incident),
            "description": description,
            "previous_complaints": previous_complaints
        }
        
        generate_and_save_document("Complaint Letter", fields)

def government_application_form(name, address, contact, email):
    st.subheader("Government Application Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        department = st.text_input("Department Name")
        purpose = st.text_input("Purpose of Application")
    with col2:
        application_type = st.selectbox(
            "Application Type",
            ["License", "Certificate", "Permission", "Registration", "Other"]
        )
    
    details = st.text_area("Application Details")
    supporting_docs = st.text_area("List of Supporting Documents")
    
    if st.button("Generate Application"):
        if not all([name, address, department, purpose, details]):
            st.error("Please fill in all required fields")
            return
        
        fields = {
            "name": name,
            "address": address,
            "contact": contact,
            "email": email,
            "department": department,
            "purpose": purpose,
            "application_type": application_type,
            "details": details,
            "supporting_docs": supporting_docs
        }
        
        generate_and_save_document("Government Application", fields)

def legal_notice_form(name, address, contact, email):
    st.subheader("Legal Notice Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        recipient = st.text_input("Notice To (Name/Department)")
        recipient_address = st.text_area("Recipient Address")
    with col2:
        notice_subject = st.text_input("Subject of Notice")
        cause_of_action = st.text_input("Cause of Action")
    
    grievance = st.text_area("Details of Grievance")
    relief_sought = st.text_area("Relief Sought")
    time_period = st.number_input("Response Time Period (in days)", min_value=1, value=15)
    
    if st.button("Generate Legal Notice"):
        if not all([name, address, recipient, recipient_address, grievance]):
            st.error("Please fill in all required fields")
            return
        
        fields = {
            "sender_name": name,
            "sender_address": address,
            "contact": contact,
            "email": email,
            "recipient": recipient,
            "recipient_address": recipient_address,
            "notice_subject": notice_subject,
            "cause_of_action": cause_of_action,
            "grievance": grievance,
            "relief_sought": relief_sought,
            "time_period": time_period
        }
        
        generate_and_save_document("Legal Notice", fields)

def appeal_letter_form(name, address, contact, email):
    st.subheader("Appeal Letter Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        authority = st.text_input("Appellate Authority")
        previous_ref = st.text_input("Previous Reference/Order Number")
    with col2:
        order_date = st.date_input("Date of Previous Order")
        appeal_type = st.selectbox(
            "Type of Appeal",
            ["Service Matter", "Administrative Decision", "Penalty", "Other"]
        )
    
    grounds = st.text_area("Grounds for Appeal")
    relief = st.text_area("Relief Sought")
    
    if st.button("Generate Appeal Letter"):
        if not all([name, address, authority, grounds]):
            st.error("Please fill in all required fields")
            return
        
        fields = {
            "name": name,
            "address": address,
            "contact": contact,
            "email": email,
            "authority": authority,
            "previous_ref": previous_ref,
            "order_date": str(order_date),
            "appeal_type": appeal_type,
            "grounds": grounds,
            "relief": relief
        }
        
        generate_and_save_document("Appeal Letter", fields)

def permission_request_form(name, address, contact, email):
    st.subheader("Permission Request Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        authority = st.text_input("Authority Name")
        purpose = st.text_input("Purpose of Request")
    with col2:
        duration = st.text_input("Duration (if applicable)")
        location = st.text_input("Location (if applicable)")
    
    details = st.text_area("Request Details")
    undertaking = st.text_area("Undertaking/Declaration")
    
    if st.button("Generate Permission Request"):
        if not all([name, address, authority, purpose, details]):
            st.error("Please fill in all required fields")
            return
        
        fields = {
            "name": name,
            "address": address,
            "contact": contact,
            "email": email,
            "authority": authority,
            "purpose": purpose,
            "duration": duration,
            "location": location,
            "details": details,
            "undertaking": undertaking
        }
        
        generate_and_save_document("Permission Request", fields)

def custom_document_form(name, address, contact, email):
    st.subheader("Custom Document Generator")
    
    document_title = st.text_input("Document Title")
    recipient = st.text_input("Recipient/Authority")
    subject = st.text_input("Subject")
    content = st.text_area("Document Content", height=300)
    
    if st.button("Generate Custom Document"):
        if not all([name, address, document_title, content]):
            st.error("Please fill in all required fields")
            return
        
        fields = {
            "name": name,
            "address": address,
            "contact": contact,
            "email": email,
            "document_title": document_title,
            "recipient": recipient,
            "subject": subject,
            "content": content
        }
        
        generate_and_save_document("Custom Document", fields)

def generate_and_save_document(doc_type, fields):
    try:
        with st.spinner("Generating document..."):
            # Generate document
            generated_content = generate_document(doc_type, fields)
            
            # Save to history
            timestamp = datetime.now()
            doc_name = f"{doc_type}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
            save_to_history(doc_name, doc_type, generated_content, timestamp)
            
            # Display result
            st.success("Document generated successfully!")
            
            # Display the generated document
            with st.expander("Generated Document", expanded=True):
                st.markdown(generated_content)
            
            # Download button
            st.download_button(
                label="Download Document",
                data=generated_content.encode(),
                file_name=f"{doc_name}.txt",
                mime="text/plain"
            )
            
            # Navigation options
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Generate Another Document"):
                    st.rerun()
            with col2:
                if st.button("View Document History"):
                    st.switch_page("pages/4_Document_History.py")
                    
    except Exception as e:
        st.error(f"Error generating document: {str(e)}")

if __name__ == "__main__":
    writing_assistant_page()