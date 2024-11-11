import streamlit as st
from PIL import Image
import datetime
from theme import apply_dark_theme, show_page_header, show_footer
from utils import (
    process_image, 
    process_pdf, 
    initialize_session_state, 
    create_chat_engine,
    save_to_history,
    generate_pdf_analysis,
    process_captured_image,
    format_analysis_results
)

# Page config
st.set_page_config(
    page_title="Document Analysis |  CiviDoc AI",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Apply dark theme
st.markdown(apply_dark_theme(), unsafe_allow_html=True)

def document_analysis_page():
    # Initialize states
    initialize_session_state()
    
    # Header
    st.markdown(show_page_header(
        "📝 Document Analysis",
        "Upload or capture documents for instant analysis"
    ), unsafe_allow_html=True)
    
    # Main content tabs - Mobile friendly
    tabs = st.tabs([
        "📤 Upload ",
        "📸 Capture",
        "📊 Results"
    ])
    
    with tabs[0]:
        st.markdown(
            "<div class='card'>"
            "<h3>Upload Documents</h3>"
            "<p style='margin-bottom: 2rem;'>Support for PDF, JPG, JPEG, and PNG files.</p>"
            "<div class='status-badge status-success'>Multiple files supported</div>"
            "</div>",
            unsafe_allow_html=True
        )
        
        # Mobile-friendly file uploader
        uploaded_files = st.file_uploader(
            "Drop files or tap to browse",
            type=["jpg", "jpeg", "png", "pdf"],
            accept_multiple_files=True,
            key="doc_uploader"
        )
        
        if uploaded_files:
            st.markdown(
                f"<div class='status-badge status-success' style='margin: 1rem 0;'>"
                f"📎 {len(uploaded_files)} file(s) uploaded"
                f"</div>",
                unsafe_allow_html=True
            )
            
            # File list - Mobile friendly
            st.markdown(
                "<div class='card'>"
                "<h4>Selected Files:</h4>"
                "<div class='touch-spacing'>",
                unsafe_allow_html=True
            )
            
            for file in uploaded_files:
                st.markdown(
                    f"<div style='display: flex; align-items: center; padding: 0.5rem 0;'>"
                    f"<span style='margin-right: 0.5rem;'>📄</span>{file.name}"
                    f"</div>",
                    unsafe_allow_html=True
                )
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Analysis button - Touch friendly
            if st.button("🔍 Analyze Documents", use_container_width=True):
                process_uploaded_files(uploaded_files)
    
    with tabs[1]:
        st.markdown(
            "<div class='card'>"
            "<h3>Capture Document</h3>"
            "<p>Take a clear photo of your document using your camera.</p>"
            "</div>",
            unsafe_allow_html=True
        )
        
        # Mobile-optimized camera input
        picture = st.camera_input(
            "📸 Tap to capture",
            help="Make sure the document is well-lit and clearly visible"
        )
        
        if picture:
            st.markdown(
                "<div class='status-badge status-success' style='margin: 1rem 0;'>"
                "📸 Image captured successfully"
                "</div>",
                unsafe_allow_html=True
            )
            
            # Analysis button - Touch friendly
            if st.button("🔍 Analyze Photo", use_container_width=True):
                process_captured_image(picture)
    
    with tabs[2]:
        display_analysis_results()

def process_uploaded_files(files):
    """Process multiple uploaded files with mobile-friendly progress tracking"""
    progress_text = "Processing documents..."
    total_files = len(files)
    
    # Progress tracking
    progress_placeholder = st.empty()
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, uploaded_file in enumerate(files, 1):
        try:
            # Update progress
            progress_placeholder.markdown(
                f"<div style='text-align: center; margin: 1rem 0;'>"
                f"Processing file {idx} of {total_files}"
                f"</div>",
                unsafe_allow_html=True
            )
            
            status_text.markdown(
                f"<div class='status-badge status-warning'>"
                f"📝 Processing: {uploaded_file.name}"
                f"</div>",
                unsafe_allow_html=True
            )
            
            if uploaded_file.type in ['image/jpeg', 'image/png']:
                # Process image
                image = Image.open(uploaded_file)
                analysis = process_image(image)
                
                # Save results
                st.session_state.analyses[uploaded_file.name] = {
                    'type': uploaded_file.type,
                    'analysis': analysis,
                    'timestamp': datetime.datetime.now()
                }
                
                # Create chat engine
                st.session_state.chat_engines[uploaded_file.name] = create_chat_engine(analysis)
                
            elif uploaded_file.type == 'application/pdf':
                # Process PDF
                documents = process_pdf(uploaded_file)
                analysis = generate_pdf_analysis(documents)
                
                # Save results
                st.session_state.analyses[uploaded_file.name] = {
                    'type': uploaded_file.type,
                    'analysis': analysis,
                    'timestamp': datetime.datetime.now()
                }
                
                # Create chat engine
                st.session_state.chat_engines[uploaded_file.name] = create_chat_engine(documents)
            
            # Update progress
            progress_bar.progress(idx/total_files)
            
            # Save to history
            save_to_history(
                uploaded_file.name,
                uploaded_file.type.split('/')[1].upper(),
                analysis,
                datetime.datetime.now()
            )
            
        except Exception as e:
            st.error(
                f"❌ Error processing {uploaded_file.name}\n"
                f"Details: {str(e)}"
            )
    
    # Clear progress indicators
    progress_placeholder.empty()
    progress_bar.empty()
    
    # Show completion message
    status_text.markdown(
        "<div class='status-badge status-success' style='margin: 1rem 0;'>"
        "✅ All documents processed successfully!"
        "</div>",
        unsafe_allow_html=True
    )
    
    
def display_analysis_results():
    """Display analysis results with mobile-friendly layout"""
    if st.session_state.analyses:
        
        # Display results
        if st.session_state.analyses:
            for filename, data in st.session_state.analyses.items():
                st.markdown(
                    f"<div class='card'>"
                    f"<div style='display: flex; justify-content: space-between; align-items: center;'>"
                    f"<h4>{filename}</h4>"
                    f"<div class='status-badge status-success'>{data['type'].split('/')[1].upper()}</div>"
                    f"</div>"
                    f"<hr style='margin: 0.5rem 0;'>"
                    f"{(data['analysis'])}" # Use the formatting function
                    f"<div class='touch-spacing'>"
                    f"</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
    else:
        st.markdown(
            "<div class='card' style='text-align: center;'>"
            "<h3>No Documents Analyzed</h3>"
            "<p>Upload or capture documents to see analysis results here.</p>"
            "</div>",
            unsafe_allow_html=True
        )
        

if __name__ == "__main__":
    document_analysis_page()
