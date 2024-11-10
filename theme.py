
def apply_dark_theme():
    return (
        "<style>"
        # Base styles
        "body { background-color: #0F172A; color: #E2E8F0; }"
        ".main { padding: 0rem 1rem; }"
        
        # Button styles
        ".stButton>button {"
        "    width: 100%;"
        "    padding: 1rem;"
        "    font-size: 1.1em;"
        "    border-radius: 10px;"
        "    background-color: #1E293B;"
        "    color: #E2E8F0;"
        "    border: 1px solid #3B82F6;"
        "    box-shadow: 0 2px 5px rgba(0,0,0,0.3);"
        "    transition: all 0.2s ease;"
        "}"
        ".stButton>button:hover {"
        "    transform: translateY(-2px);"
        "    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);"
        "    border-color: #60A5FA;"
        "    background-color: #2D3748;"
        "}"
        
        # Card styles
        ".card {"
        "    padding: 1.5rem;"
        "    border-radius: 10px;"
        "    background-color: #1E293B;"
        "    margin-bottom: 1rem;"
        "    border: 1px solid #2D3748;"
        "    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"
        "    transition: all 0.2s ease;"
        "}"
        ".card:hover {"
        "    border-color: #3B82F6;"
        "    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);"
        "    transform: translateY(-2px);"
        "}"
        
        # Typography
        "h1, h2, h3, h4, h5, h6 { color: #60A5FA; }"
        "h1 { font-size: 2.5em; font-weight: 700; }"
        "h2 { font-size: 2em; font-weight: 600; }"
        "h3 { font-size: 1.5em; font-weight: 600; }"
        "p { line-height: 1.6; }"
        
        # Form elements
        ".stTextInput>div>div>input,"
        ".stTextArea>div>div>textarea,"
        ".stSelectbox>div>div>select {"
        "    background-color: #1E293B;"
        "    color: #E2E8F0;"
        "    border: 1px solid #3B82F6;"
        "    border-radius: 8px;"
        "}"
        
        # File uploader
        ".stFileUploader>div>button {"
        "    background-color: #1E293B;"
        "    color: #E2E8F0;"
        "    border: 1px dashed #3B82F6;"
        "    border-radius: 8px;"
        "}"
        ".stFileUploader>div>button:hover {"
        "    border-color: #60A5FA;"
        "    background-color: #2D3748;"
        "}"
        
        # Expander
        ".streamlit-expanderHeader {"
        "    background-color: #1E293B;"
        "    color: #E2E8F0;"
        "    border-radius: 8px;"
        "}"
        ".streamlit-expanderContent {"
        "    background-color: #1E293B;"
        "    border: 1px solid #2D3748;"
        "    border-radius: 0 0 8px 8px;"
        "}"
        
        # Tabs
        ".stTabs [data-baseweb='tab-list'] {"
        "    gap: 30px;"
        "    background-color: #1E293B;"
        "    padding: 1.5rem;"
        "    border-radius: 8px;"
        "}"
        ".stTabs [data-baseweb='tab'] {"
        "    height: 40px;"
        "    padding: 1.5rem;"
        "    background-color: #2D3748;"
        "    border-radius: 8px;"
        "    color: #E2E8F0;"
        "    border: 1px solid #3B82F6;"
        "}"
        ".stTabs [aria-selected='true'] {"
        "    background-color: #3B82F6;"
        "}"
        
        # Chat elements
        ".chat-message {"
        "    padding: 1rem;"
        "    margin: 0.5rem 0;"
        "    border-radius: 8px;"
        "    background-color: #1E293B;"
        "    border: 1px solid #2D3748;"
        "}"
        ".user-message {"
        "    background-color: #2D3748;"
        "    border-color: #3B82F6;"
        "}"
        
        # Status indicators
        ".status-badge {"
        "    display: inline-block;"
        "    padding: 0.25rem 0.75rem;"
        "    border-radius: 9999px;"
        "    font-size: 0.875rem;"
        "    font-weight: 500;"
        "    text-align: center;"
        "}"
        ".status-success { background-color: #065F46; color: #6EE7B7; }"
        ".status-warning { background-color: #92400E; color: #FCD34D; }"
        ".status-error { background-color: #991B1B; color: #FCA5A5; }"
        
        # Tooltips
        ".tooltip {"
        "    position: relative;"
        "    display: inline-block;"
        "}"
        ".tooltip .tooltiptext {"
        "    visibility: hidden;"
        "    background-color: #2D3748;"
        "    color: #E2E8F0;"
        "    text-align: center;"
        "    padding: 0.5rem;"
        "    border-radius: 6px;"
        "    border: 1px solid #3B82F6;"
        "    position: absolute;"
        "    z-index: 1;"
        "    bottom: 125%;"
        "    left: 50%;"
        "    transform: translateX(-50%);"
        "    opacity: 0;"
        "    transition: opacity 0.2s;"
        "}"
        ".tooltip:hover .tooltiptext {"
        "    visibility: visible;"
        "    opacity: 1;"
        "}"
        
        # Progress indicators
        ".progress-bar {"
        "    width: 100%;"
        "    height: 8px;"
        "    background-color: #2D3748;"
        "    border-radius: 4px;"
        "    overflow: hidden;"
        "}"
        ".progress-bar-fill {"
        "    height: 100%;"
        "    background-color: #3B82F6;"
        "    transition: width 0.3s ease;"
        "}"
        
        # Custom scrollbar
        "::-webkit-scrollbar { width: 8px; height: 8px; }"
        "::-webkit-scrollbar-track { background: #1E293B; }"
        "::-webkit-scrollbar-thumb { background: #3B82F6; border-radius: 4px; }"
        "::-webkit-scrollbar-thumb:hover { background: #60A5FA; }"
        
        # Animations
        "@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }"
        ".fade-in { animation: fadeIn 0.3s ease-in; }"
        
        # Footer
        ".footer {"
        "    text-align: center;"
        "    color: #94A3B8;"
        "    padding: 2rem 1rem;"
        "    margin-top: 2rem;"
        "    border-top: 1px solid #2D3748;"
        "}"
        "</style>"
    )

def show_page_header(title, description=None):
    header_html = (
        "<div style='background-color: #1E293B; padding: 2rem; "+
        "border-radius: 10px; margin-bottom: 2rem;'>"+
        "<h1 style='color: #60A5FA; margin-bottom: 0.5rem;'>" + title + "</h1>"
    )
    if description:
        header_html += (
            "<p style='color: #E2E8F0; font-size: 1.1em;'>" + description + "</p>"
        )
    header_html += "</div>"
    return header_html

def show_footer():
    return (
        "<div class='footer'>"
        "    <p>Need help? Contact our support team</p>"
        "    <p style='font-size: 0.8em; margin-top: 0.5rem;'>"
        "        CiviDoc AI © 2024"
        "    </p>"
        "</div>"
    )
