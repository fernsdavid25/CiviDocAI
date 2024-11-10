import streamlit as st
from groq import Groq
import io
import base64
import re
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings, Document
from llama_index.readers.file import PDFReader
from llama_index.llms.groq import Groq as LlamaGroq
from llama_index.embeddings.langchain import LangchainEmbedding
from langchain_community.embeddings import HuggingFaceEmbeddings
from datetime import datetime
from PIL import Image
import gettext

# Load environment variables and configure
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

# Configure LlamaIndex
Settings.llm = LlamaGroq(api_key=groq_api_key, model="llama-3.1-70b-versatile")
lc_embed_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
Settings.embed_model = LangchainEmbedding(lc_embed_model)

def initialize_session_state():
    """Initialize all session state variables"""
    if 'chat_engines' not in st.session_state:
        st.session_state.chat_engines = {}
    if 'analyses' not in st.session_state:
        st.session_state.analyses = {}
    if 'documents' not in st.session_state:
        st.session_state.documents = {}
    if 'current_doc' not in st.session_state:
        st.session_state.current_doc = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'document_history' not in st.session_state:
        st.session_state.document_history = {}

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def process_image(image):
    """Process image using Llama vision model"""
    img_base64 = encode_image_to_base64(image)
    img_url = f"data:image/jpeg;base64,{img_base64}"
    
    completion = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Please analyze this government document and provide:
                        1. Document type and purpose
                        2. Key requirements and deadlines
                        3. Complex terms explained simply
                        4. Required actions or next steps
                        5. Important contact information or submission details"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_url
                        }
                    }
                ]
            }
        ],
        temperature=0.1,
        max_tokens=1024,
        top_p=1,
        stream=False
    )
    
    return completion.choices[0].message.content

def generate_pdf_analysis(documents):
    """Generate analysis from PDF documents using Groq"""
    try:
        # Combine all document content
        full_text = "\n".join([doc.text for doc in documents])
        
        # Generate analysis using Groq
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Please analyze this government document and provide:\n"
                        "1. Document Type and Purpose:\n"
                        "   - What kind of document is this?\n"
                        "   - What is its main purpose?\n\n"
                        "2. Key Requirements:\n"
                        "   - What are the main requirements or conditions?\n"
                        "   - What documents or information are needed?\n\n"
                        "3. Important Deadlines:\n"
                        "   - What are the key dates and deadlines?\n"
                        "   - Are there any time-sensitive requirements?\n\n"
                        "4. Complex Terms Explained:\n"
                        "   - Explain any technical or legal terms in simple language\n"
                        "   - Clarify any complex procedures\n\n"
                        "5. Required Actions:\n"
                        "   - What steps need to be taken?\n"
                        "   - What is the process to follow?\n\n"
                        "6. Contact Information:\n"
                        "   - Who to contact for queries?\n"
                        "   - Where to submit the documents?\n\n"
                        "Document content:\n" + full_text
                    )
                }
            ],
            temperature=0.1,
            max_tokens=2048,
            top_p=1
        )
        
        # Format the analysis with proper styling
        analysis = completion.choices[0].message.content

        completionsum = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Summarize the following content: " + analysis
                    )
                }
            ],
            temperature=0.1,
            max_tokens=2048,
            top_p=1
        )

        analysissum = completionsum.choices[0].message.content
        
        return analysissum
    except Exception as e:
        error_msg = "Error generating PDF analysis: " + str(e)
        raise Exception(error_msg)

def clean_llm_output(output):
    """Clean LLM output by removing HTML tags and formatting symbols"""
    # Remove HTML tags
    cleaned_text = re.sub(r'<[^>]+>', '', output)
    # Remove double asterisks
    cleaned_text = cleaned_text.replace('**', '')
    cleaned_text = cleaned_text.replace('*', '')
    # Remove extra whitespace
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()

def format_analysis_results(text):
    """Format analysis results into structured HTML"""
    # First clean the text
    cleaned_text = clean_llm_output(text)
    
    # Split into sections
    sections = []
    current_section = ""
    current_title = ""
    
    for line in cleaned_text.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('*'):
            # If we have a previous section, save it
            if current_title:
                sections.append((current_title, current_section.strip()))
            # Start new section
            parts = line.split(':', 1)
            current_title = parts[0].strip()
            current_section = parts[1].strip() if len(parts) > 1 else ""
        else:
            current_section += " " + line
    
    # Add the last section
    if current_title:
        sections.append((current_title, current_section.strip()))
    
    # Generate HTML
    html = "<div class='analysis-results'>"
    for title, content in sections:
        html += f"""
            <div class='analysis-section card' style='margin-bottom: 1rem;'>
                <h4 style='color: #60A5FA; margin-bottom: 0.5rem;'>{title}</h4>
                <p style='margin: 0;'>{content}</p>
            </div>
        """
    html += "</div>"
    
    return html

def process_captured_image(picture):
    """Process image captured from camera with mobile-friendly UI"""
    try:
        # Show processing status
        status_placeholder = st.empty()
        status_placeholder.markdown(
            "<div class='status-badge status-warning'>"
            "📸 Processing captured image..."
            "</div>",
            unsafe_allow_html=True
        )
        
        # Process the image
        image = Image.open(picture)
        
        # Display the captured image with proper mobile sizing
        st.image(
            image,
            caption="Captured Document",
            use_column_width=True  # Makes image responsive
        )
        
        # Process image with AI
        with st.spinner("Analyzing document..."):
            analysis = process_image(image)
        
        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"captured_image_{timestamp}"
        
        # Save results
        st.session_state.analyses[filename] = {
            'type': 'image/jpeg',
            'analysis': analysis,
            'timestamp': datetime.datetime.now()
        }
        
        # Create chat engine
        st.session_state.chat_engines[filename] = create_chat_engine(analysis)
        
        # Save to history
        save_to_history(
            filename,
            'Captured Image',
            analysis,
            datetime.datetime.now()
        )
        
        # Update status to success
        status_placeholder.markdown(
            "<div class='status-badge status-success'>"
            "✅ Image analyzed successfully!"
            "</div>",
            unsafe_allow_html=True
        )
        
        # Display analysis results
        st.markdown(
            "<div class='card'>"
            "<h4>Analysis Results</h4>"
            f"<div style='margin: 1rem 0;'>{analysis}</div>"
            "</div>",
            unsafe_allow_html=True
        )
        
        # Mobile-friendly action buttons
        st.markdown("<div class='touch-spacing'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💬 Start Chat", use_container_width=True):
                st.session_state.current_doc = filename
                st.switch_page("pages/2_💬_Document_Chat.py")
        with col2:
            if st.button("📸 New Capture", use_container_width=True):
                st.rerun()
                
        st.markdown("</div>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(
            "❌ Error processing image\n"
            f"Details: {str(e)}"
        )

def process_pdf(pdf_file):
    """Process PDF document using LlamaIndex"""
    temp_dir = "temp_docs"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, "temp.pdf")
    
    with open(temp_path, "wb") as f:
        f.write(pdf_file.getvalue())
    
    try:
        reader = PDFReader()
        documents = reader.load_data(temp_path)
        return documents
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(temp_dir) and not os.listdir(temp_dir):
            os.rmdir(temp_dir)

def create_chat_engine(content):
    """Create chat engine from document content"""
    if isinstance(content, str):
        documents = [Document(text=content)]
    else:
        documents = content
    
    index = VectorStoreIndex.from_documents(documents)
    return index.as_chat_engine(chat_mode="condense_question", verbose=True)

def generate_document(doc_type, fields):
    """Generate government documents based on type and fields"""
    prompt = f"""Generate a formal {doc_type} with the following details:
    
    {fields}
    
    Please format this as a proper official document following standard government formatting."""
    
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=2048,
        top_p=1
    )
    
    return completion.choices[0].message.content

def save_to_history(doc_name, doc_type, content, timestamp=None):
    """Save document to history with metadata"""
    if timestamp is None:
        timestamp = datetime.now()
    
    st.session_state.document_history[doc_name] = {
        'type': doc_type,
        'content': content,
        'timestamp': timestamp,
        'status': 'Processed'
    }

def get_document_history():
    """Retrieve document history sorted by timestamp"""
    history = st.session_state.document_history
    return dict(sorted(
        history.items(),
        key=lambda x: x[1]['timestamp'],
        reverse=True
    ))

def delete_from_history(doc_name):
    """Delete document from history"""
    if doc_name in st.session_state.document_history:
        del st.session_state.document_history[doc_name]
        if doc_name in st.session_state.chat_engines:
            del st.session_state.chat_engines[doc_name]
        if doc_name in st.session_state.analyses:
            del st.session_state.analyses[doc_name]
        if st.session_state.current_doc == doc_name:
            st.session_state.current_doc = None

def format_timestamp(timestamp):
    """Format timestamp for display"""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")
