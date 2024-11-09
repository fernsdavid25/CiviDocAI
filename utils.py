# utils.py
import streamlit as st
from groq import Groq
import io
import base64
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings, Document
from llama_index.readers.file import PDFReader
from llama_index.llms.groq import Groq as LlamaGroq
from llama_index.embeddings.langchain import LangchainEmbedding
from langchain_community.embeddings import HuggingFaceEmbeddings
from datetime import datetime

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