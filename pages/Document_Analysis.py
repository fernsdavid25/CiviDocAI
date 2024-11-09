# pages/1_Document_Analysis.py
import streamlit as st
from PIL import Image
import datetime
from utils import (
    process_image, 
    process_pdf, 
    initialize_session_state, 
    create_chat_engine,
    save_to_history,
    client
)

def document_analysis_page():
    st.title("📑 Document Analysis")
    
    # Initialize states
    initialize_session_state()
    
    # Create tabs for different analysis options
    tab1, tab2, tab3 = st.tabs([
        "Upload Documents", 
        "Capture Document",
        "Analysis Results"
    ])
    
    with tab1:
        st.header("Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload government documents",
            type=["jpg", "jpeg", "png", "pdf"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.write(f"Number of files uploaded: {len(uploaded_files)}")
            
            if st.button("Analyze Documents", key="analyze_docs"):
                with st.spinner("Processing documents..."):
                    process_uploaded_files(uploaded_files)
    
    with tab2:
        st.header("Capture Document")
        picture = st.camera_input("Take a picture of the document")
        if picture:
            if st.button("Analyze Captured Image", key="analyze_capture"):
                process_captured_image(picture)
    
    with tab3:
        display_analysis_results()

def process_uploaded_files(files):
    """Process multiple uploaded files"""
    results = {}
    errors = {}
    
    for uploaded_file in files:
        try:
            if uploaded_file.type in ['image/jpeg', 'image/png']:
                # Process image
                image = Image.open(uploaded_file)
                analysis = process_image(image)
                
                # Save results
                st.session_state.analyses[uploaded_file.name] = {
                    'type': uploaded_file.type,
                    'analysis': analysis
                }
                
                # Create chat engine for the document
                st.session_state.chat_engines[uploaded_file.name] = create_chat_engine(analysis)
                
                # Save to history
                save_to_history(
                    uploaded_file.name,
                    'Image Document',
                    analysis,
                    datetime.datetime.now()
                )
                
                results[uploaded_file.name] = analysis
                
            elif uploaded_file.type == 'application/pdf':
                # Process PDF
                documents = process_pdf(uploaded_file)
                
                # Generate analysis summary from PDF content
                analysis_prompt = """
                Please analyze this document and provide:
                1. Document type and purpose
                2. Key requirements and deadlines
                3. Complex terms explained simply
                4. Required actions or next steps
                5. Important contact information or submission details
                
                Document content:
                """
                
                # Combine all document content for analysis
                full_text = "\n".join([doc.text for doc in documents])
                
                # Generate analysis using Groq
                completion = client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": analysis_prompt + full_text
                        }
                    ],
                    temperature=0.1,
                    max_tokens=2048,
                    top_p=1
                )
                
                analysis = completion.choices[0].message.content
                
                # Save results
                st.session_state.analyses[uploaded_file.name] = {
                    'type': uploaded_file.type,
                    'analysis': analysis
                }
                
                # Create chat engine for the document
                st.session_state.chat_engines[uploaded_file.name] = create_chat_engine(documents)
                
                # Save to history
                save_to_history(
                    uploaded_file.name,
                    'PDF Document',
                    analysis,
                    datetime.datetime.now()
                )
                
                results[uploaded_file.name] = analysis
                
        except Exception as e:
            errors[uploaded_file.name] = str(e)
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
    
    # Display results
    if results:
        st.success(f"Successfully processed {len(results)} files")
    if errors:
        st.error(f"Failed to process {len(errors)} files")

def display_analysis_results():
    """Display analysis results for all processed documents"""
    if st.session_state.analyses:
        st.header("Analysis Results")
        
        # Group by document type
        images = {k: v for k, v in st.session_state.analyses.items() 
                 if v['type'] in ['image/jpeg', 'image/png']}
        pdfs = {k: v for k, v in st.session_state.analyses.items() 
               if v['type'] == 'application/pdf'}
        
        # Display image analyses
        if images:
            with st.expander("Image Analyses", expanded=True):
                for filename, data in images.items():
                    col1, col2 = st.columns([5,1])
                    with col1:
                        st.markdown(f"**{filename}**")
                        st.markdown(data['analysis'])
                    with col2:
                        if st.button("Chat", key=f"chat_{filename}"):
                            st.session_state.current_doc = filename
                            st.switch_page("pages/3_Document_Chat.py")
                    st.divider()
        
        # Display PDF analyses
        if pdfs:
            with st.expander("PDF Analyses", expanded=True):
                for filename, data in pdfs.items():
                    col1, col2 = st.columns([5,1])
                    with col1:
                        st.markdown(f"**{filename}**")
                        st.markdown(data['analysis'])
                    with col2:
                        if st.button("Chat", key=f"chat_{filename}_pdf"):
                            st.session_state.current_doc = filename
                            st.switch_page("pages/3_Document_Chat.py")
                    st.divider()
    else:
        st.info("No documents analyzed yet. Upload or capture documents to begin analysis.")

def process_captured_image(picture):
    """Process image captured from camera"""
    try:
        with st.spinner("Analyzing captured image..."):
            # Process the image
            image = Image.open(picture)
            analysis = process_image(image)
            
            # Generate timestamp for unique filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"captured_image_{timestamp}"
            
            # Save results
            st.session_state.analyses[filename] = {
                'type': 'image/jpeg',
                'analysis': analysis
            }
            
            # Create chat engine for the document
            st.session_state.chat_engines[filename] = create_chat_engine(analysis)
            
            # Save to history
            save_to_history(
                filename,
                'Captured Image',
                analysis,
                datetime.datetime.now()
            )
            
            st.success("Image analyzed successfully!")
            
            # Display the analysis
            with st.expander("Analysis Results", expanded=True):
                st.markdown(analysis)
                
    except Exception as e:
        st.error(f"Error processing captured image: {str(e)}")

def display_analysis_results():
    """Display analysis results for all processed documents"""
    if st.session_state.analyses:
        st.header("Analysis Results")
        
        # Group by document type
        images = {k: v for k, v in st.session_state.analyses.items() 
                 if v['type'] in ['image/jpeg', 'image/png']}
        pdfs = {k: v for k, v in st.session_state.analyses.items() 
               if v['type'] == 'application/pdf'}
        
        # Display image analyses
        if images:
            with st.expander("Image Analyses", expanded=True):
                for filename, data in images.items():
                    st.markdown(f"**{filename}**")
                    st.markdown(data['analysis'])
                    
                    col1, col2 = st.columns([4, 1])
                    with col2:
                        if st.button("Chat", key=f"chat_{filename}"):
                            st.session_state.current_doc = filename
                            st.switch_page("pages/3_Document_Chat.py")
                    st.divider()
        
        # Display PDF analyses
        if pdfs:
            with st.expander("PDF Analyses", expanded=True):
                for filename, data in pdfs.items():
                    st.markdown(f"**{filename}**")
                    st.markdown(data['analysis'])
                    
                    col1, col2 = st.columns([4, 1])
                    with col2:
                        if st.button("Chat", key=f"chat_{filename}_pdf"):
                            st.session_state.current_doc = filename
                            st.switch_page("pages/3_Document_Chat.py")
                    st.divider()
    else:
        st.info("No documents analyzed yet. Upload or capture documents to begin analysis.")

if __name__ == "__main__":
    document_analysis_page()