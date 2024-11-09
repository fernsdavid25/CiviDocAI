# Home.py
import streamlit as st
from theme import apply_dark_theme, show_page_header, show_footer

# Page config
st.set_page_config(
    page_title="CiviDoc AI",
    page_icon="🏛️",
    layout="centered",
    initial_sidebar_state="expanded"  # Collapsed by default on mobile
)

# Apply dark theme
st.markdown(apply_dark_theme(), unsafe_allow_html=True)

def main():
    # Header
    st.markdown(show_page_header(
        "🏛️ CiviDoc AI",
        "Your AI-powered companion for all government document needs"
    ), unsafe_allow_html=True)
    
    # Quick Access Section - Mobile Friendly Cards
    st.markdown(
        "<div class='grid'>"  # Uses the responsive grid system
        
        "<div class='card' onclick='void(0)'>"  # Added onclick for better touch feedback
        "<div style='text-align: center;'>"
        "<h3 style='margin-bottom: 0.5rem;'>📝 Document Analysis</h3>"
        "<p style='margin-bottom: 1rem;'>Upload and understand government documents instantly</p>"
        "<div class='status-badge status-success'>Ready to Use</div>"
        "</div>"
        "</div>"
        
        "<div class='card' onclick='void(0)'>"
        "<div style='text-align: center;'>"
        "<h3 style='margin-bottom: 0.5rem;'>✍️ Writing Assistant</h3>"
        "<p style='margin-bottom: 1rem;'>Create professional government documents effortlessly</p>"
        "<div class='status-badge status-success'>Ready to Use</div>"
        "</div>"
        "</div>"
        
        "<div class='card' onclick='void(0)'>"
        "<div style='text-align: center;'>"
        "<h3 style='margin-bottom: 0.5rem;'>💬 Document Chat</h3>"
        "<p style='margin-bottom: 1rem;'>Get instant answers about your documents</p>"
        "<div class='status-badge status-success'>Ready to Use</div>"
        "</div>"
        "</div>"
        
        "</div>",
        unsafe_allow_html=True
    )
    
    # Quick Action Buttons - Touch Friendly
    st.markdown("<div class='touch-spacing'>", unsafe_allow_html=True)
    if st.button("📝 Start Document Analysis", use_container_width=True):
        st.switch_page("pages/Document_Analysis.py")
    if st.button("✍️ Create New Document", use_container_width=True):
        st.switch_page("pages/Writing_Assistant.py")
    if st.button("💬 Open Document Chat", use_container_width=True):
        st.switch_page("pages/Document_Chat.py")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Features Section - Responsive Grid
    st.markdown("<h3 style='margin: 1.5rem 0 1rem;'>🌟 Key Features</h3>", unsafe_allow_html=True)
    
    # Features grid with improved mobile layout
    st.markdown(
        "<div class='grid'>"
        
        # Document Analysis Card
        "<div class='card'>"
        "<h3 style='margin-bottom: 0.75rem;'>📑 Document Analysis</h3>"
        "<div class='touch-spacing'>"
        "<p>✓ Instant document understanding</p>"
        "<p>✓ Complex term explanations</p>"
        "<p>✓ Form filling guidance</p>"
        "<p>✓ Requirement extraction</p>"
        "<p>✓ Deadline tracking</p>"
        "</div>"
        "</div>"
        
        # Writing Assistant Card
        "<div class='card'>"
        "<h3 style='margin-bottom: 0.75rem;'>✍️ Writing Assistant</h3>"
        "<div class='touch-spacing'>"
        "<p>✓ RTI application generator</p>"
        "<p>✓ Complaint letter creator</p>"
        "<p>✓ Legal notice drafting</p>"
        "<p>✓ Appeal letter formatting</p>"
        "<p>✓ Custom document templates</p>"
        "</div>"
        "</div>"
        
        # Interactive Help Card
        "<div class='card'>"
        "<h3 style='margin-bottom: 0.75rem;'>💬 Interactive Help</h3>"
        "<div class='touch-spacing'>"
        "<p>✓ Real-time document chat</p>"
        "<p>✓ Context-aware responses</p>"
        "<p>✓ Procedure explanations</p>"
        "<p>✓ Multi-document support</p>"
        "<p>✓ Instant clarifications</p>"
        "</div>"
        "</div>"
        
        # Document Management Card
        "<div class='card'>"
        "<h3 style='margin-bottom: 0.75rem;'>📚 Document Management</h3>"
        "<div class='touch-spacing'>"
        "<p>✓ Secure document storage</p>"
        "<p>✓ Version tracking</p>"
        "<p>✓ Easy organization</p>"
        "<p>✓ Quick retrieval</p>"
        "<p>✓ Status monitoring</p>"
        "</div>"
        "</div>"
        
        "</div>",
        unsafe_allow_html=True
    )
    
    # How It Works Section - Mobile Friendly Steps
    st.markdown("<h3 style='margin: 1.5rem 0 1rem;'>🔄 How It Works</h3>", unsafe_allow_html=True)
    
    st.markdown(
        "<div class='grid'>"  # Responsive grid
        
        # Step 1
        "<div class='card' style='text-align: center;'>"
        "<h4 style='margin-bottom: 0.5rem;'>1. Upload</h4>"
        "<p style='margin-bottom: 0.75rem;'>Upload your government documents or start creating new ones</p>"
        "<div class='progress-bar'><div class='progress-bar-fill' style='width: 25%;'></div></div>"
        "</div>"
        
        # Step 2
        "<div class='card' style='text-align: center;'>"
        "<h4 style='margin-bottom: 0.5rem;'>2. Process</h4>"
        "<p style='margin-bottom: 0.75rem;'>Our AI analyzes and processes your documents instantly</p>"
        "<div class='progress-bar'><div class='progress-bar-fill' style='width: 50%;'></div></div>"
        "</div>"
        
        # Step 3
        "<div class='card' style='text-align: center;'>"
        "<h4 style='margin-bottom: 0.5rem;'>3. Understand</h4>"
        "<p style='margin-bottom: 0.75rem;'>Get clear explanations and guidance for your documents</p>"
        "<div class='progress-bar'><div class='progress-bar-fill' style='width: 75%;'></div></div>"
        "</div>"
        
        # Step 4
        "<div class='card' style='text-align: center;'>"
        "<h4 style='margin-bottom: 0.5rem;'>4. Act</h4>"
        "<p style='margin-bottom: 0.75rem;'>Take action with confidence using our recommendations</p>"
        "<div class='progress-bar'><div class='progress-bar-fill' style='width: 100%;'></div></div>"
        "</div>"
        
        "</div>",
        unsafe_allow_html=True
    )
    
    # Additional Information - Mobile Friendly Layout
    st.markdown("<div class='grid'>", unsafe_allow_html=True)
    
    # Who Is This For Section
    st.markdown(
        "<div class='card'>"
        "<h3 style='margin-bottom: 0.75rem;'>🎯 Who Is This For?</h3>"
        "<div class='touch-spacing'>"
        "<p>• Citizens dealing with government procedures</p>"
        "<p>• RTI applicants and activists</p>"
        "<p>• Legal professionals</p>"
        "<p>• Government service seekers</p>"
        "<p>• Anyone needing document assistance</p>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )
    
    # Security & Privacy Section
    st.markdown(
        "<div class='card'>"
        "<h3 style='margin-bottom: 0.75rem;'>🛡️ Security & Privacy</h3>"
        "<div class='touch-spacing'>"
        "<p>• End-to-end encryption</p>"
        "<p>• Secure document processing</p>"
        "<p>• No permanent storage</p>"
        "<p>• Privacy-first approach</p>"
        "<p>• Regular security updates</p>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown(show_footer(), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
