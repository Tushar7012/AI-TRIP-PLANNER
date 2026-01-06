import streamlit as st
import requests
import datetime
import os

# Backend endpoint - use environment variable for production
BASE_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap');
    
    /* Root Variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --dark-bg: #0e1117;
        --card-bg: rgba(17, 25, 40, 0.75);
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
        --text-primary: #ffffff;
        --text-secondary: rgba(255, 255, 255, 0.7);
        --success-color: #10b981;
        --warning-color: #f59e0b;
    }
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(180deg, #0e1117 0%, #1a1f2e 50%, #0e1117 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600;
    }
    
    p, span, div, input, textarea, button {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Main Header Styling */
    .main-header {
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* Feature Cards */
    .feature-card {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
    }
    
    .feature-card h4 {
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }
    
    .feature-card p {
        color: var(--text-secondary);
        font-size: 0.875rem;
        margin: 0;
        line-height: 1.5;
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        background: var(--card-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-size: 1rem !important;
        padding: 0.875rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-secondary) !important;
    }
    
    /* Button Styling */
    .stFormSubmitButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stFormSubmitButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Response Card */
    .response-card {
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 1.5rem;
        animation: fadeInUp 0.5s ease;
    }
    
    .response-card h1 {
        font-size: 1.75rem;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    
    .response-card h2 {
        font-size: 1.4rem;
        color: #667eea;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    .response-card h3 {
        font-size: 1.2rem;
        color: var(--text-primary);
        margin-top: 1rem;
    }
    
    .response-card p, .response-card li {
        color: var(--text-secondary);
        line-height: 1.7;
    }
    
    .response-card ul, .response-card ol {
        padding-left: 1.5rem;
    }
    
    .response-card li {
        margin-bottom: 0.5rem;
    }
    
    /* Sidebar Styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: var(--card-bg) !important;
        border-right: 1px solid var(--glass-border) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: var(--text-secondary);
    }
    
    .sidebar-header {
        text-align: center;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .sidebar-header h2 {
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(16, 185, 129, 0.15);
        color: var(--success-color);
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .status-badge::before {
        content: '';
        width: 8px;
        height: 8px;
        background: var(--success-color);
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    /* Spinner customization */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
        margin: 1.5rem 0;
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 2rem;
        color: var(--text-secondary);
        font-size: 0.875rem;
        border-top: 1px solid var(--glass-border);
        margin-top: 3rem;
    }
    
    .custom-footer a {
        color: #667eea;
        text-decoration: none;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: var(--glass-bg) !important;
        border-radius: 12px !important;
        border: 1px solid var(--glass-border) !important;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 1rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
    }
    
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2>AI Travel Planner</h2>
        <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">
            Powered by LangGraph
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="status-badge">Agent Online</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("### Features")
    
    st.markdown("""
    <div class="feature-card">
        <h4>🌍 Destination Discovery</h4>
        <p>Explore attractions, restaurants, and hidden gems at your destination.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>🌤️ Weather Intelligence</h4>
        <p>Real-time weather data to plan the perfect trip timing.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>💰 Budget Planning</h4>
        <p>Smart expense calculations with currency conversion.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>🗓️ Itinerary Builder</h4>
        <p>Day-by-day travel plans customized to your preferences.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.5); font-size: 0.8rem; padding: 1rem;">
        Built with Streamlit, FastAPI & LangGraph
    </div>
    """, unsafe_allow_html=True)

# Main Content
st.markdown("""
<div class="main-header">
    <h1>AI Travel Planner</h1>
    <p>Your intelligent travel companion powered by advanced AI. Get personalized trip itineraries, 
    budget breakdowns, and local insights in seconds.</p>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input form
st.markdown("### Plan Your Next Adventure")
st.markdown("<p style='color: rgba(255,255,255,0.6); margin-bottom: 1rem;'>Tell me your destination and trip duration, and I'll create a comprehensive travel plan for you.</p>", unsafe_allow_html=True)

with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input(
        "Destination",
        placeholder="e.g., Plan a 5-day trip to Tokyo with a budget of $2000",
        label_visibility="collapsed"
    )
    submit_button = st.form_submit_button("Generate Travel Plan")

if submit_button and user_input.strip():
    try:
        with st.spinner("🌍 Researching your destination and crafting your perfect itinerary..."):
            payload = {"question": user_input}
            response = requests.post(f"{BASE_URL}/query", json=payload, timeout=120)

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            
            # Display the response in a styled card
            st.markdown(f"""
            <div class="response-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h1 style="margin: 0;">Your Travel Plan</h1>
                    <span style="color: rgba(255,255,255,0.5); font-size: 0.875rem;">
                        Generated on {datetime.datetime.now().strftime('%B %d, %Y at %H:%M')}
                    </span>
                </div>
                <div class="custom-divider"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Render the markdown content
            st.markdown(answer)
            
            # Disclaimer
            st.markdown("""
            <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); 
                        border-radius: 12px; padding: 1rem; margin-top: 1.5rem;">
                <p style="color: #f59e0b; margin: 0; font-size: 0.875rem;">
                    <strong>Disclaimer:</strong> This travel plan was generated by AI. Please verify all information, 
                    especially prices, operating hours, and travel requirements before your trip.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"Failed to generate travel plan: {response.text}")

    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again with a simpler query.")
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the backend server. Please ensure the API is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Sample queries section
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

st.markdown("### Try These Queries")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <p style="color: white; font-weight: 500;">"Plan a romantic 4-day trip to Paris"</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <p style="color: white; font-weight: 500;">"Budget-friendly 7 days in Thailand"</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <p style="color: white; font-weight: 500;">"Adventure trip to New Zealand for 10 days"</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="custom-footer">
    <p>Created by <strong>Tushar Das</strong> | AI Travel Planner v1.0</p>
    <p style="margin-top: 0.5rem;">Powered by LangGraph, FastAPI, and Streamlit</p>
</div>
""", unsafe_allow_html=True)