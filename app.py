
import streamlit as st
from datetime import datetime
from database.database import db
from utils.error_handler import logger
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="ResearchHub Pro - Academic Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database on startup
try:
    db.create_tables()
    logger.info("Database initialized")
except Exception as e:
    logger.error(f"Database initialization failed: {str(e)}")

# Initialize session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Color schemes
COLORS = {
    'dark': {
        'bg': '#0E1117',
        'secondary_bg': '#1A1D29',
        'card_bg': '#262730',
        'border': '#2D3139',
        'text': '#FAFAFA',
        'text_secondary': '#B0B3B8',
        'primary': '#6366F1',
        'primary_hover': '#7C3AED',
        'accent': '#10B981',
        'gradient_start': '#6366F1',
        'gradient_end': '#8B5CF6',
    },
    'light': {
        'bg': '#FFFFFF',
        'secondary_bg': '#F9FAFB',
        'card_bg': '#FFFFFF',
        'border': '#E5E7EB',
        'text': '#111827',
        'text_secondary': '#6B7280',
        'primary': '#6366F1',
        'primary_hover': '#7C3AED',
        'accent': '#10B981',
        'gradient_start': '#6366F1',
        'gradient_end': '#8B5CF6',
    }
}

theme = COLORS['dark' if st.session_state.dark_mode else 'light']

# Enhanced CSS with modern design
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp {{
        background: {theme['bg']};
        color: {theme['text']};
    }}
    
    /* Header Styles */
    .main-header {{
        font-size: 4.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }}
    
    .sub-header {{
        font-size: 1.25rem;
        text-align: center;
        margin-bottom: 3rem;
        color: {theme['text_secondary']};
        font-weight: 400;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }}
    
    /* Metric Cards */
    .metric-card {{
        background: {theme['card_bg']};
        border: 1px solid {theme['border']};
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }}
    
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(99, 102, 241, 0.15);
        border-color: {theme['primary']};
    }}
    
    .metric-value {{
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }}
    
    .metric-label {{
        font-size: 0.875rem;
        color: {theme['text_secondary']};
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    /* Feature Cards */
    .feature-card {{
        background: {theme['card_bg']};
        border: 1px solid {theme['border']};
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .feature-card::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 4px;
        background: linear-gradient(180deg, {theme['gradient_start']}, {theme['gradient_end']});
        opacity: 0;
        transition: opacity 0.3s ease;
    }}
    
    .feature-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(99, 102, 241, 0.1);
        border-color: {theme['primary']};
    }}
    
    .feature-card:hover::before {{
        opacity: 1;
    }}
    
    .feature-icon {{
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }}
    
    .feature-title {{
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        color: {theme['text']};
    }}
    
    .feature-description {{
        font-size: 0.95rem;
        color: {theme['text_secondary']};
        line-height: 1.6;
    }}
    
    /* Sidebar Enhancements */
    [data-testid="stSidebar"] {{
        background: {theme['secondary_bg']};
        border-right: 1px solid {theme['border']};
    }}
    
    [data-testid="stSidebar"] .stButton > button {{
        background: {theme['card_bg']};
        color: {theme['text']};
        border: 1px solid {theme['border']};
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
        width: 100%;
    }}
    
    [data-testid="stSidebar"] .stButton > button:hover {{
        background: {theme['primary']};
        color: white;
        border-color: {theme['primary']};
        transform: translateX(4px);
    }}
    
    /* Stats Display */
    .stat-mini {{
        background: {theme['card_bg']};
        border: 1px solid {theme['border']};
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }}
    
    .stat-mini-value {{
        font-size: 1.75rem;
        font-weight: 700;
        color: {theme['primary']};
    }}
    
    .stat-mini-label {{
        font-size: 0.8rem;
        color: {theme['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    /* Activity Timeline */
    .activity-item {{
        background: {theme['card_bg']};
        border: 1px solid {theme['border']};
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.2s ease;
    }}
    
    .activity-item:hover {{
        border-color: {theme['primary']};
        transform: translateX(4px);
    }}
    
    .activity-icon {{
        width: 40px;
        height: 40px;
        border-radius: 10px;
        background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
    }}
    
    /* CTA Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
    }}
    
    /* Dark Mode Toggle */
    .dark-mode-toggle {{
        position: relative;
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: {theme['card_bg']};
        border: 1px solid {theme['border']};
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
        margin-bottom: 1.5rem;
    }}
    
    .toggle-label {{
        font-size: 0.875rem;
        font-weight: 500;
        color: {theme['text']};
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    /* Progress Bar */
    .progress-container {{
        width: 100%;
        height: 8px;
        background: {theme['border']};
        border-radius: 4px;
        overflow: hidden;
        margin: 0.5rem 0;
    }}
    
    .progress-bar {{
        height: 100%;
        background: linear-gradient(90deg, {theme['gradient_start']}, {theme['gradient_end']});
        border-radius: 4px;
        transition: width 0.3s ease;
    }}
    
    /* Section Headers */
    .section-header {{
        font-size: 2rem;
        font-weight: 700;
        margin: 3rem 0 1.5rem 0;
        color: {theme['text']};
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }}
    
    .section-header::before {{
        content: '';
        width: 4px;
        height: 32px;
        background: linear-gradient(180deg, {theme['gradient_start']}, {theme['gradient_end']});
        border-radius: 2px;
    }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Divider */
    hr {{
        border: none;
        height: 1px;
        background: {theme['border']};
        margin: 2rem 0;
    }}
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Logo/Brand
    st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0 2rem 0;">
            <div style="font-size: 2rem; font-weight: 700; background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']}); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                ResearchHub
            </div>
            <div style="font-size: 0.75rem; color: {theme['text_secondary']}; margin-top: 0.25rem;">
                AI-Powered Research
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Dark mode toggle
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"""
            <div class="toggle-label">
                {'🌙' if not st.session_state.dark_mode else '☀️'} 
                {'Dark Mode' if not st.session_state.dark_mode else 'Light Mode'}
            </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("", key="toggle", help="Toggle theme"):
            toggle_dark_mode()
            st.rerun()
    
    st.markdown("---")
    
    # Quick stats with enhanced design
    st.markdown("### 📊 Dashboard")
    try:
        stats = db.get_statistics()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="stat-mini">
                    <div class="stat-mini-value">{stats.get('total_projects', 0)}</div>
                    <div class="stat-mini-label">Projects</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="stat-mini">
                    <div class="stat-mini-value">{stats.get('total_papers', 0)}</div>
                    <div class="stat-mini-label">Papers</div>
                </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="stat-mini">
                    <div class="stat-mini-value">{stats.get('total_searches', 0)}</div>
                    <div class="stat-mini-label">Searches</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="stat-mini">
                    <div class="stat-mini-value">{stats.get('total_reviews', 0)}</div>
                    <div class="stat-mini-label">Reviews</div>
                </div>
            """, unsafe_allow_html=True)
    except:
        st.info("🔄 Initializing database...")
    
    st.markdown("---")
    
    # Quick navigation with icons
    st.markdown("### 🚀 Quick Access")
    
    if st.button("🔍  Search Papers", use_container_width=True):
        st.switch_page("pages/Search.py")
    
    if st.button("📂  My Projects", use_container_width=True):
        st.switch_page("pages/Projects.py")
    
    if st.button("📝  Generate Review", use_container_width=True):
        st.switch_page("pages/Literature_Review.py")
    
    if st.button("📊  Analytics", use_container_width=True):
        st.switch_page("pages/Analytics.py")
    
    st.markdown("---")
    
    # System Status
    st.markdown("### ⚡ System Status")
    st.markdown(f"""
        <div class="stat-mini">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: {theme['text_secondary']}; font-size: 0.85rem;">API Status</span>
                <span style="color: {theme['accent']}; font-size: 0.85rem;">● Online</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="stat-mini">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: {theme['text_secondary']}; font-size: 0.85rem;">Database</span>
                <span style="color: {theme['accent']}; font-size: 0.85rem;">● Connected</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Footer
    st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0; color: {theme['text_secondary']}; font-size: 0.75rem;">
            <div style="margin-bottom: 0.5rem;">Version 2.0.1</div>
            <div>© 2024 ResearchHub</div>
        </div>
    """, unsafe_allow_html=True)

# Main content
def main():
    # Hero section
    st.markdown('<div class="main-header">ResearchHub Pro</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Transform weeks of literature review into minutes. AI-powered research assistant for academics and researchers.</div>',
        unsafe_allow_html=True
    )
    
    # CTA Row
    col1, col2, col3, col4, col5 = st.columns([1, 1.5, 1.5, 1.5, 1])
    
    with col2:
        if st.button("🚀  Get Started", key="hero_cta", use_container_width=True):
            st.switch_page("pages/Search.py")
    
    with col3:
        if st.button("📚  View Demo", key="demo_cta", use_container_width=True):
            st.info("Demo coming soon!")
    
    with col4:
        if st.button("📖  Documentation", key="docs_cta", use_container_width=True):
            st.info("Documentation coming soon!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">10x</div>
                <div class="metric-label">Faster Research</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">2M+</div>
                <div class="metric-label">Papers Indexed</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">98%</div>
                <div class="metric-label">Accuracy Rate</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">24/7</div>
                <div class="metric-label">AI Assistant</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Main features
    st.markdown('<div class="section-header">Core Features</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Intelligent Search</div>
                <div class="feature-description">
                    Search across multiple academic databases simultaneously. 
                    Get AI-powered summaries, identify research gaps, and extract key findings instantly.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">AI Summarization</div>
                <div class="feature-description">
                    Advanced NLP models extract key insights from papers. 
                    Understand complex research in seconds, not hours.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Visual Analytics</div>
                <div class="feature-description">
                    Interactive charts and graphs reveal trends in your research. 
                    Citation networks, topic clusters, and temporal analysis.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">📝</div>
                <div class="feature-title">Auto Literature Review</div>
                <div class="feature-description">
                    Generate publication-ready literature reviews automatically. 
                    5-10 pages of academic-quality writing in minutes.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">🗂️</div>
                <div class="feature-title">Smart Organization</div>
                <div class="feature-description">
                    Manage projects with tags, notes, and annotations. 
                    Advanced filtering and search within your library.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">💾</div>
                <div class="feature-title">Universal Export</div>
                <div class="feature-description">
                    Export to Word, PDF, LaTeX, Markdown, BibTeX, or JSON. 
                    Seamlessly integrate with your existing workflow.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Recent activity
    st.markdown('<div class="section-header">Recent Activity</div>', unsafe_allow_html=True)
    
    try:
        recent_searches = db.get_recent_searches(limit=5)
        if recent_searches:
            for idx, search in enumerate(recent_searches):
                st.markdown(f"""
                    <div class="activity-item">
                        <div class="activity-icon">🔍</div>
                        <div style="flex: 1;">
                            <div style="font-weight: 600; color: {theme['text']};">{search.query}</div>
                            <div style="font-size: 0.85rem; color: {theme['text_secondary']}; margin-top: 0.25rem;">
                                {search.results_count} papers • {search.created_at.strftime('%B %d, %Y at %I:%M %p')}
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="text-align: center; padding: 3rem; color: {theme['text_secondary']};">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📚</div>
                    <div style="font-size: 1.1rem; font-weight: 500;">No activity yet</div>
                    <div style="margin-top: 0.5rem;">Start by searching for papers to see your activity here</div>
                </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
            <div style="text-align: center; padding: 3rem; color: {theme['text_secondary']};">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🚀</div>
                <div style="font-size: 1.1rem; font-weight: 500;">Start your research journey</div>
                <div style="margin-top: 0.5rem;">Begin searching to track your activity</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Tips section
    st.markdown('<div class="section-header">Quick Tips</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-title">💡 Search Best Practices</div>
                <div class="feature-description">
                    • Use specific keywords<br>
                    • Filter by publication year<br>
                    • Enable open access filter<br>
                    • Try different databases
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-title">📖 Review Generation</div>
                <div class="feature-description">
                    • Process 10+ papers minimum<br>
                    • Enable PDF processing<br>
                    • Use medium detail level<br>
                    • Add custom instructions
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-title">🎯 Project Management</div>
                <div class="feature-description">
                    • Use descriptive names<br>
                    • Add relevant tags<br>
                    • Take detailed notes<br>
                    • Regular backups
                </div>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()































# import streamlit as st
# from datetime import datetime
# from database.database import db
# from utils.error_handler import logger

# # Page configuration
# st.set_page_config(
#     page_title="ResearchHub Pro - Academic Research Assistant",
#     page_icon="🎓",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Initialize database on startup
# try:
#     db.create_tables()
#     logger.info("Database initialized")
# except Exception as e:
#     logger.error(f"Database initialization failed: {str(e)}")

# # Initialize session state for dark mode
# if 'dark_mode' not in st.session_state:
#     st.session_state.dark_mode = False

# # Dark mode toggle function
# def toggle_dark_mode():
#     st.session_state.dark_mode = not st.session_state.dark_mode

# # Apply dark mode CSS
# if st.session_state.dark_mode:
#     st.markdown("""
#         <style>
#         @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
#         * {
#             font-family: 'Poppins', sans-serif;
#         }
        
#         .stApp {
#             background: #0f1419;
#             color: #e4e6eb;
#         }
        
#         .stMarkdown, .stText {
#             color: #e4e6eb;
#         }
        
#         .stButton>button {
#             background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
#             color: #ffffff;
#             border: none;
#             border-radius: 8px;
#             padding: 0.6rem 1.2rem;
#             font-weight: 500;
#             transition: all 0.3s ease;
#             font-size: 0.95rem;
#         }
        
#         .stButton>button:hover {
#             background: linear-gradient(135deg, #00e5ff 0%, #00aaff 100%);
#             box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
#         }
        
#         .stTextInput>div>div>input, .stSelectbox>div>div>select {
#             background-color: #1a1f2e;
#             color: #e4e6eb;
#             border: 1px solid #2d3748;
#             border-radius: 8px;
#             padding: 0.6rem;
#         }
        
#         .metric-card {
#             background: #1a1f2e;
#             border: 1px solid #2d3748;
#         }
        
#         .feature-card {
#             background: #1a1f2e;
#             border-left: 3px solid #00d4ff;
#         }
        
#         [data-testid="stSidebar"] {
#             background: #1a1f2e;
#         }
        
#         [data-testid="stSidebar"] .stButton>button {
#             background: transparent;
#             border: 1px solid #2d3748;
#             color: #e4e6eb;
#         }
        
#         [data-testid="stSidebar"] .stButton>button:hover {
#             background: #2d3748;
#             border: 1px solid #00d4ff;
#         }
        
#         .toggle-button {
#             background: #2d3748;
#             color: #e4e6eb;
#             border: 1px solid #4a5568;
#             border-radius: 6px;
#             padding: 0.4rem 0.8rem;
#             cursor: pointer;
#             font-size: 0.85rem;
#         }
#         </style>
#     """, unsafe_allow_html=True)
# else:
#     st.markdown("""
#         <style>
#         @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
#         * {
#             font-family: 'Poppins', sans-serif;
#         }
        
#         .stApp {
#             background: #f8f9fa;
#             color: #2d3748;
#         }
        
#         .stMarkdown, .stText {
#             color: #2d3748;
#         }
        
#         .stButton>button {
#             background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
#             color: #ffffff;
#             border: none;
#             border-radius: 8px;
#             padding: 0.6rem 1.2rem;
#             font-weight: 500;
#             transition: all 0.3s ease;
#             font-size: 0.95rem;
#         }
        
#         .stButton>button:hover {
#             background: linear-gradient(135deg, #ff7b7b 0%, #ff6a7f 100%);
#             box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
#         }
        
#         .stTextInput>div>div>input, .stSelectbox>div>div>select {
#             background-color: #ffffff;
#             color: #2d3748;
#             border: 2px solid #e2e8f0;
#             border-radius: 8px;
#             padding: 0.6rem;
#         }
        
#         .metric-card {
#             background: #ffffff;
#             border: 1px solid #e2e8f0;
#         }
        
#         .feature-card {
#             background: #ffffff;
#             border-left: 3px solid #ff6b6b;
#         }
        
#         [data-testid="stSidebar"] {
#             background: #ffffff;
#             border-right: 1px solid #e2e8f0;
#         }
        
#         [data-testid="stSidebar"] .stButton>button {
#             background: #f7fafc;
#             border: 1px solid #e2e8f0;
#             color: #2d3748;
#         }
        
#         [data-testid="stSidebar"] .stButton>button:hover {
#             background: #edf2f7;
#             border: 1px solid #cbd5e0;
#         }
        
#         .toggle-button {
#             background: #edf2f7;
#             color: #2d3748;
#             border: 1px solid #cbd5e0;
#             border-radius: 6px;
#             padding: 0.4rem 0.8rem;
#             cursor: pointer;
#             font-size: 0.85rem;
#         }
#         </style>
#     """, unsafe_allow_html=True)

# # Common CSS
# st.markdown("""
#     <style>
#     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
#     .main-header {
#         font-size: 2.8rem;
#         font-weight: 700;
#         text-align: center;
#         margin-bottom: 0.5rem;
#         letter-spacing: -0.5px;
#     }
    
#     .sub-header {
#         font-size: 1.15rem;
#         text-align: center;
#         margin-bottom: 2.5rem;
#         opacity: 0.75;
#         font-weight: 400;
#     }
    
#     .metric-card {
#         padding: 1.5rem 1rem;
#         border-radius: 12px;
#         margin: 0.5rem 0;
#         text-align: center;
#         transition: transform 0.2s ease;
#     }
    
#     .metric-card:hover {
#         transform: translateY(-3px);
#     }
    
#     .metric-value {
#         font-size: 2.2rem;
#         font-weight: 700;
#         margin: 0.4rem 0;
#     }
    
#     .metric-label {
#         font-size: 0.85rem;
#         opacity: 0.7;
#         font-weight: 500;
#         text-transform: uppercase;
#         letter-spacing: 0.5px;
#     }
    
#     .feature-card {
#         padding: 1.5rem;
#         border-radius: 12px;
#         margin: 0.8rem 0;
#         transition: transform 0.2s ease;
#     }
    
#     .feature-card:hover {
#         transform: translateX(3px);
#     }
    
#     .feature-title {
#         font-size: 1.15rem;
#         font-weight: 600;
#         margin-bottom: 0.6rem;
#     }
    
#     .feature-text {
#         font-size: 0.9rem;
#         line-height: 1.5;
#         opacity: 0.8;
#     }
    
#     .cta-section {
#         border-radius: 16px;
#         padding: 2rem 1rem;
#         margin: 2rem 0;
#     }
    
#     .footer {
#         margin-top: 3rem;
#         padding: 1.5rem 0;
#         border-top: 1px solid rgba(0, 0, 0, 0.1);
#     }
    
#     .footer-content {
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         flex-wrap: wrap;
#         gap: 1rem;
#     }
    
#     .footer-section {
#         flex: 1;
#         min-width: 200px;
#     }
    
#     .footer-title {
#         font-size: 0.95rem;
#         font-weight: 600;
#         margin-bottom: 0.5rem;
#     }
    
#     .footer-link {
#         display: inline-block;
#         margin-right: 1rem;
#         margin-bottom: 0.3rem;
#         opacity: 0.7;
#         transition: opacity 0.2s ease;
#         text-decoration: none;
#         font-size: 0.85rem;
#     }
    
#     .footer-link:hover {
#         opacity: 1;
#     }
    
#     .footer-copyright {
#         text-align: center;
#         padding-top: 1rem;
#         margin-top: 1rem;
#         border-top: 1px solid rgba(0, 0, 0, 0.05);
#         opacity: 0.6;
#         font-size: 0.8rem;
#     }
    
#     hr {
#         border: none;
#         height: 1px;
#         background: rgba(0, 0, 0, 0.1);
#         margin: 1.5rem 0;
#     }
    
#     .activity-item {
#         border-radius: 10px;
#         padding: 0.9rem;
#         margin: 0.4rem 0;
#         transition: all 0.2s ease;
#     }
    
#     .activity-item:hover {
#         transform: translateX(3px);
#     }
    
#     .section-title {
#         font-size: 1.8rem;
#         font-weight: 600;
#         margin-bottom: 1.5rem;
#     }
    
#     .cta-icon {
#         font-size: 2.5rem;
#         margin-bottom: 0.8rem;
#         display: block;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Sidebar
# with st.sidebar:
#     # Logo/Title
#     if st.session_state.dark_mode:
#         st.markdown("""
#             <div style="text-align: center; padding: 1rem 0;">
#                 <h1 style="font-size: 1.5rem; font-weight: 700; margin: 0; color: #00d4ff;">
#                     <i class="fas fa-microscope"></i> ResearchHub Pro
#                 </h1>
#                 <p style="margin: 0.3rem 0 0 0; opacity: 0.6; font-size: 0.8rem;">Research Made Simple</p>
#             </div>
#         """, unsafe_allow_html=True)
#     else:
#         st.markdown("""
#             <div style="text-align: center; padding: 1rem 0;">
#                 <h1 style="font-size: 1.5rem; font-weight: 700; margin: 0; color: #ff6b6b;">
#                     <i class="fas fa-microscope"></i> ResearchHub Pro
#                 </h1>
#                 <p style="margin: 0.3rem 0 0 0; opacity: 0.6; font-size: 0.8rem;">Research Made Simple</p>
#             </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown("---")
    
#     # Dark mode toggle
#     st.markdown('<p style="font-weight: 500; font-size: 0.9rem; margin-bottom: 0.5rem;">🌓 Theme</p>', unsafe_allow_html=True)
#     if st.button("🌙 Toggle Dark/Light Mode", on_click=toggle_dark_mode, key="dark_mode_toggle", use_container_width=True):
#         pass
    
#     st.markdown("---")
    
#     # Quick stats
#     st.markdown('<p style="font-weight: 600; font-size: 1rem; margin-bottom: 0.8rem;">📊 Statistics</p>', unsafe_allow_html=True)
#     try:
#         stats = db.get_statistics()
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Projects", stats.get('total_projects', 0))
#             st.metric("Searches", stats.get('total_searches', 0))
#         with col2:
#             st.metric("Papers", stats.get('total_papers', 0))
#     except:
#         st.info("📂 Database not initialized")
    
#     st.markdown("---")
    
#     # Quick navigation
#     st.markdown('<p style="font-weight: 600; font-size: 1rem; margin-bottom: 0.8rem;">⚡ Quick Access</p>', unsafe_allow_html=True)
#     if st.button("🔍 Search Papers", use_container_width=True, key="nav_search"):
#         st.switch_page("pages/Search.py")
#     if st.button("📁 My Projects", use_container_width=True, key="nav_projects"):
#         st.switch_page("pages/Projects.py")
#     if st.button("📄 Generate Review", use_container_width=True, key="nav_review"):
#         st.switch_page("pages/Literature_Review.py")
    
#     st.markdown("---")
    
#     # Footer
#     st.markdown("""
#         <div style="text-align: center; padding: 0.5rem 0; opacity: 0.5;">
#             <p style="margin: 0; font-size: 0.75rem;">Version 2.0.1</p>
#         </div>
#     """, unsafe_allow_html=True)


# # Main content
# def main():
#     # Hero section
#     if st.session_state.dark_mode:
#         st.markdown('<div class="main-header" style="color: #00d4ff;"><i class="fas fa-microscope"></i> ResearchHub Pro</div>', unsafe_allow_html=True)
#     else:
#         st.markdown('<div class="main-header" style="color: #ff6b6b;"><i class="fas fa-microscope"></i> ResearchHub Pro</div>', unsafe_allow_html=True)
    
#     st.markdown(
#         '<div class="sub-header">AI-Powered Academic Research Assistant for Modern Researchers</div>',
#         unsafe_allow_html=True
#     )
    
#     # Key metrics
#     col1, col2, col3, col4 = st.columns(4)
    
#     metric_color = "#00d4ff" if st.session_state.dark_mode else "#ff6b6b"
    
#     with col1:
#         st.markdown(f"""
#             <div class="metric-card">
#                 <i class="fas fa-bolt" style="font-size: 1.8rem; margin-bottom: 0.4rem; color: {metric_color};"></i>
#                 <div class="metric-value" style="color: {metric_color};">200x</div>
#                 <div class="metric-label">Faster Reviews</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown(f"""
#             <div class="metric-card">
#                 <i class="fas fa-database" style="font-size: 1.8rem; margin-bottom: 0.4rem; color: {metric_color};"></i>
#                 <div class="metric-value" style="color: {metric_color};">2</div>
#                 <div class="metric-label">Databases</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col3:
#         st.markdown(f"""
#             <div class="metric-card">
#                 <i class="fas fa-file-export" style="font-size: 1.8rem; margin-bottom: 0.4rem; color: {metric_color};"></i>
#                 <div class="metric-value" style="color: {metric_color};">7</div>
#                 <div class="metric-label">Export Formats</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col4:
#         st.markdown(f"""
#             <div class="metric-card">
#                 <i class="fas fa-check-circle" style="font-size: 1.8rem; margin-bottom: 0.4rem; color: {metric_color};"></i>
#                 <div class="metric-value" style="color: {metric_color};">90%</div>
#                 <div class="metric-label">Publication Ready</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown("---")
    
#     # Main features
#     st.markdown(f'<h2 class="section-title"><i class="fas fa-star" style="color: {metric_color};"></i> Core Features</h2>', unsafe_allow_html=True)
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown(f"""
#             <div class="feature-card">
#                 <div class="feature-title">
#                     <i class="fas fa-search" style="color: {metric_color}; margin-right: 0.5rem;"></i>Smart Search
#                 </div>
#                 <p class="feature-text">Search across Semantic Scholar and ArXiv simultaneously. 
#                 AI-powered summaries, research gap analysis, and key findings extraction.</p>
#             </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown(f"""
#             <div class="feature-card">
#                 <div class="feature-title">
#                     <i class="fas fa-folder-open" style="color: {metric_color}; margin-right: 0.5rem;"></i>Project Management
#                 </div>
#                 <p class="feature-text">Organize papers into projects. Add notes, tags, and annotations. 
#                 Track your research progress effortlessly.</p>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown(f"""
#             <div class="feature-card">
#                 <div class="feature-title">
#                     <i class="fas fa-file-alt" style="color: {metric_color}; margin-right: 0.5rem;"></i>Literature Review Generator
#                 </div>
#                 <p class="feature-text">Generate comprehensive, publication-ready literature reviews in minutes. 
#                 5-10 pages of academic-quality writing automatically.</p>
#             </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown(f"""
#             <div class="feature-card">
#                 <div class="feature-title">
#                     <i class="fas fa-download" style="color: {metric_color}; margin-right: 0.5rem;"></i>Universal Export
#                 </div>
#                 <p class="feature-text">Export to Word, PDF, LaTeX, Markdown, BibTeX, CSV, or JSON. 
#                 Ready for any workflow or publication.</p>
#             </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown("---")
    
#     # Call to action
#     bg_color = "rgba(0, 212, 255, 0.05)" if st.session_state.dark_mode else "rgba(255, 107, 107, 0.05)"
#     st.markdown(f'<div class="cta-section" style="background: {bg_color};">', unsafe_allow_html=True)
#     st.markdown(f'<h2 class="section-title" style="text-align: center;"><i class="fas fa-rocket" style="color: {metric_color};"></i> Get Started in 3 Steps</h2>', unsafe_allow_html=True)
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.markdown(f'<div style="text-align: center;"><i class="fas fa-search cta-icon" style="color: {metric_color};"></i></div>', unsafe_allow_html=True)
#         st.markdown("#### 1. Search")
#         st.write("Find papers from multiple academic databases.")
#         if st.button("Start Searching →", key="cta_search", use_container_width=True):
#             st.switch_page("pages/Search.py")
    
#     with col2:
#         st.markdown(f'<div style="text-align: center;"><i class="fas fa-folder-plus cta-icon" style="color: {metric_color};"></i></div>', unsafe_allow_html=True)
#         st.markdown("#### 2. Organize")
#         st.write("Save papers to projects and manage your research.")
#         if st.button("Create Project →", key="cta_project", use_container_width=True):
#             st.switch_page("pages/Projects.py")
    
#     with col3:
#         st.markdown(f'<div style="text-align: center;"><i class="fas fa-magic cta-icon" style="color: {metric_color};"></i></div>', unsafe_allow_html=True)
#         st.markdown("#### 3. Generate")
#         st.write("Create literature reviews in minutes, not weeks.")
#         if st.button("Generate Review →", key="cta_review", use_container_width=True):
#             st.switch_page("pages/Literature_Review.py")
    
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     st.markdown("---")
    
#     # Recent activity
#     st.markdown(f'<h2 class="section-title"><i class="fas fa-history" style="color: {metric_color};"></i> Recent Activity</h2>', unsafe_allow_html=True)
    
#     activity_bg = "rgba(0, 212, 255, 0.05)" if st.session_state.dark_mode else "rgba(255, 107, 107, 0.05)"
    
#     try:
#         recent_searches = db.get_recent_searches(limit=5)
#         if recent_searches:
#             for search in recent_searches:
#                 st.markdown(f"""
#                     <div class="activity-item" style="background: {activity_bg};">
#                         <div style="display: flex; justify-content: space-between; align-items: center; gap: 1rem;">
#                             <div style="flex: 2;">
#                                 <i class="fas fa-search" style="color: {metric_color}; margin-right: 0.5rem;"></i>
#                                 <strong>{search.query}</strong>
#                             </div>
#                             <div style="flex: 1; text-align: center;">
#                                 <i class="fas fa-file-alt" style="color: {metric_color}; margin-right: 0.3rem;"></i>
#                                 {search.results_count} papers
#                             </div>
#                             <div style="flex: 0.8; text-align: right;">
#                                 <i class="fas fa-clock" style="color: {metric_color}; margin-right: 0.3rem;"></i>
#                                 {search.created_at.strftime('%m/%d')}
#                             </div>
#                         </div>
#                     </div>
#                 """, unsafe_allow_html=True)
#         else:
#             st.info("📭 No recent searches. Start by searching for papers!")
#     except Exception as e:
#         st.info("🚀 Start searching to see your activity here.")
    
#     st.markdown("---")
    
#     # Tips & Tricks
#     with st.expander("💡 Tips & Best Practices"):
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown("""
#             **🔍 Search Tips:**
#             - Use specific keywords for better results
#             - Filter by year for recent papers
#             - Enable "Open Access Only" for free PDFs
            
#             **📁 Project Management:**
#             - Use descriptive project names
#             - Add tags for easy filtering
#             - Take notes as you read
#             """)
        
#         with col2:
#             st.markdown("""
#             **📄 Literature Reviews:**
#             - Process at least 10 papers for best results
#             - Enable PDF processing for deeper analysis
#             - Medium detail level works best
            
#             **💾 Export Options:**
#             - Word: Best for editing
#             - LaTeX: Best for academic publishing
#             - BibTeX: Best for reference managers
#             """)
    
#     # Footer
#     st.markdown('<div class="footer">', unsafe_allow_html=True)
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.markdown(f"""
#             <div class="footer-section">
#                 <div class="footer-title" style="color: {metric_color};">
#                     <i class="fas fa-microscope"></i> ResearchHub Pro
#                 </div>
#                 <p style="opacity: 0.7; font-size: 0.85rem;">
#                     AI-driven tools for academic excellence
#                 </p>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("""
#             <div class="footer-section">
#                 <div class="footer-title">Resources</div>
#                 <a href="#" class="footer-link">Documentation</a>
#                 <a href="#" class="footer-link">API Guide</a>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col3:
#         st.markdown("""
#             <div class="footer-section">
#                 <div class="footer-title">Support</div>
#                 <a href="#" class="footer-link"><i class="fab fa-github"></i> GitHub</a>
#                 <a href="#" class="footer-link"><i class="fas fa-envelope"></i> Contact</a>
#             </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown("""
#         <div class="footer-copyright">
#             <p style="margin: 0;">
#                 © 2024 ResearchHub Pro • Made for researchers worldwide 🌍
#             </p>
#         </div>
#     """, unsafe_allow_html=True)
    
#     st.markdown('</div>', unsafe_allow_html=True)


# if __name__ == "__main__":
#     main()




























# import streamlit as st
# from datetime import datetime
# from database.database import db
# from utils.error_handler import logger

# # Page configuration
# st.set_page_config(
#     page_title="ResearchHub Pro - Academic Research Assistant",
#     page_icon="🔬",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Initialize database on startup
# try:
#     db.create_tables()
#     logger.info("Database initialized")
# except Exception as e:
#     logger.error(f"Database initialization failed: {str(e)}")

# # Initialize session state for dark mode
# if 'dark_mode' not in st.session_state:
#     st.session_state.dark_mode = False

# # Dark mode toggle function
# def toggle_dark_mode():
#     st.session_state.dark_mode = not st.session_state.dark_mode

# # Apply dark mode CSS
# if st.session_state.dark_mode:
#     st.markdown("""
#         <style>
#         /* Dark mode styles */
#         .stApp {
#             background-color: #1E1E1E;
#             color: #E0E0E0;
#         }
#         .stMarkdown, .stText {
#             color: #E0E0E0;
#         }
#         .stButton>button {
#             background-color: #2D2D2D;
#             color: #E0E0E0;
#             border: 1px solid #404040;
#         }
#         .stButton>button:hover {
#             background-color: #3D3D3D;
#             border: 1px solid #505050;
#         }
#         .stTextInput>div>div>input {
#             background-color: #2D2D2D;
#             color: #E0E0E0;
#             border: 1px solid #404040;
#         }
#         .stSelectbox>div>div>select {
#             background-color: #2D2D2D;
#             color: #E0E0E0;
#         }
#         .metric-card {
#             background-color: #2D2D2D;
#             border: 1px solid #404040;
#         }
#         .feature-card {
#             background-color: #2D2D2D;
#             border-left: 4px solid #4A9EFF;
#         }
#         </style>
#     """, unsafe_allow_html=True)
# else:
#     st.markdown("""
#         <style>
#         /* Light mode styles */
#         .stApp {
#             background-color: #FFFFFF;
#             color: #1E1E1E;
#         }
#         .metric-card {
#             background-color: #F8F9FA;
#             border: 1px solid #E0E0E0;
#         }
#         .feature-card {
#             background-color: #F8F9FA;
#             border-left: 4px solid #1f77b4;
#         }
#         </style>
#     """, unsafe_allow_html=True)

# # Common CSS
# st.markdown("""
#     <style>
#     .main-header {
#         font-size: 3rem;
#         font-weight: bold;
#         text-align: center;
#         margin-bottom: 1rem;
#         background: linear-gradient(90deg, #1f77b4, #4A9EFF);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#     }
#     .sub-header {
#         font-size: 1.3rem;
#         text-align: center;
#         margin-bottom: 2rem;
#         opacity: 0.8;
#     }
#     .metric-card {
#         padding: 1.5rem;
#         border-radius: 10px;
#         margin: 0.5rem 0;
#         text-align: center;
#     }
#     .metric-value {
#         font-size: 2.5rem;
#         font-weight: bold;
#         margin: 0.5rem 0;
#     }
#     .metric-label {
#         font-size: 1rem;
#         opacity: 0.7;
#     }
#     .feature-card {
#         padding: 1.5rem;
#         border-radius: 10px;
#         margin: 1rem 0;
#     }
#     .feature-title {
#         font-size: 1.3rem;
#         font-weight: bold;
#         margin-bottom: 0.5rem;
#     }
#     .cta-button {
#         font-size: 1.2rem;
#         padding: 1rem 2rem;
#         border-radius: 8px;
#         font-weight: bold;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Sidebar
# with st.sidebar:
#     st.image("https://via.placeholder.com/150x50/1f77b4/FFFFFF?text=Research+AI", use_container_width=True)
    
#     st.markdown("---")
    
#     # Dark mode toggle
#     col1, col2 = st.columns([3, 1])
#     with col1:
#         st.write("🌙 Dark Mode")
#     with col2:
#         st.button("Toggle", on_click=toggle_dark_mode, key="dark_mode_toggle")
    
#     st.markdown("---")
    
#     # Quick stats
#     st.subheader("📊 Quick Stats")
#     try:
#         stats = db.get_statistics()
#         st.metric("Projects", stats.get('total_projects', 0))
#         st.metric("Papers", stats.get('total_papers', 0))
#         st.metric("Searches", stats.get('total_searches', 0))
#     except:
#         st.info("Database not initialized")
    
#     st.markdown("---")
    
#     # Quick navigation
#     st.subheader("🚀 Quick Access")
#     if st.button("🔍 Search Papers", use_container_width=True):
#         st.switch_page("pages/Search.py")
#     if st.button("📚 My Projects", use_container_width=True):
#         st.switch_page("pages/Projects.py")
#     if st.button("📝 Generate Review", use_container_width=True):
#         st.switch_page("pages/Literature_Review.py")
    
#     st.markdown("---")
    
#     # Footer
#     st.caption("🔬 AI ResearchHub v2.0")
#     # st.caption("Phase 2 - Production Ready")


# # Main content
# def main():
#     # Hero section
#     st.markdown('<div class="main-header">🔬ResearchHub</div>', unsafe_allow_html=True)
#     st.markdown(
#         '<div class="sub-header">Your AI-Powered Research Assistant for Academic Excellence</div>',
#         unsafe_allow_html=True
#     )
    
#     # Key metrics
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         st.markdown("""
#             <div class="metric-card">
#                 <div class="metric-value">200x</div>
#                 <div class="metric-label">Faster Reviews</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("""
#             <div class="metric-card">
#                 <div class="metric-value">2</div>
#                 <div class="metric-label">Databases</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col3:
#         st.markdown("""
#             <div class="metric-card">
#                 <div class="metric-value">7</div>
#                 <div class="metric-label">Export Formats</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col4:
#         st.markdown("""
#             <div class="metric-card">
#                 <div class="metric-value">90%</div>
#                 <div class="metric-label">Publication Ready</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown("---")
    
#     # Main features
#     st.header("✨ What You Can Do")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown("""
#             <div class="feature-card">
#                 <div class="feature-title">🔍 Smart Search</div>
#                 <p>Search across Semantic Scholar and ArXiv simultaneously. 
#                 AI-powered summaries, research gap analysis, and key findings extraction.</p>
#             </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown("""
#             <div class="feature-card">
#                 <div class="feature-title">📚 Project Management</div>
#                 <p>Organize papers into projects. Add notes, tags, and annotations. 
#                 Track your research progress effortlessly.</p>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("""
#             <div class="feature-card">
#                 <div class="feature-title">📝 Literature Review Generator</div>
#                 <p>Generate comprehensive, publication-ready literature reviews in minutes. 
#                 5-10 pages of academic-quality writing automatically.</p>
#             </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown("""
#             <div class="feature-card">
#                 <div class="feature-title">💾 Universal Export</div>
#                 <p>Export to Word, PDF, LaTeX, Markdown, BibTeX, CSV, or JSON. 
#                 Ready for any workflow or publication.</p>
#             </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown("---")
    
#     # Call to action
#     st.header("🚀 Get Started")
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.subheader("1️⃣ Search")
#         st.write("Find papers on any topic from multiple academic databases.")
#         if st.button("Start Searching →", key="cta_search", use_container_width=True):
#             st.switch_page("pages/Search.py")
    
#     with col2:
#         st.subheader("2️⃣ Organize")
#         st.write("Save papers to projects, add notes, and manage your research.")
#         if st.button("Create Project →", key="cta_project", use_container_width=True):
#             st.switch_page("pages/Projects.py")
    
#     with col3:
#         st.subheader("3️⃣ Generate")
#         st.write("Create literature reviews in minutes, not weeks.")
#         if st.button("Generate Review →", key="cta_review", use_container_width=True):
#             st.switch_page("pages/Literature_Review.py")
    
#     st.markdown("---")
    
#     # Recent activity
#     st.header("📈 Recent Activity")
    
#     try:
#         recent_searches = db.get_recent_searches(limit=5)
#         if recent_searches:
#             for search in recent_searches:
#                 col1, col2, col3 = st.columns([3, 1, 1])
#                 with col1:
#                     st.write(f"🔍 **{search.query}**")
#                 with col2:
#                     st.write(f"📄 {search.results_count} papers")
#                 with col3:
#                     st.write(f"🕐 {search.created_at.strftime('%m/%d')}")
#         else:
#             st.info("No recent searches. Start by searching for papers!")
#     except Exception as e:
#         st.info("Start searching to see your activity here.")
    
#     st.markdown("---")
    
#     # Tips & Tricks
#     with st.expander("💡 Tips & Tricks"):
#         st.markdown("""
#         ### Getting the Best Results:
        
#         1. **Search Tips:**
#            - Use specific keywords: "machine learning drug discovery" > "AI healthcare"
#            - Filter by year for recent papers
#            - Enable "Open Access Only" for free PDFs
        
#         2. **Literature Reviews:**
#            - Process at least 10 papers for best results
#            - Enable PDF processing for deeper analysis
#            - Medium detail level works best for most cases
        
#         3. **Projects:**
#            - Use descriptive names: "PhD Chapter 2" > "Papers"
#            - Add tags for easy filtering
#            - Take notes as you read
        
#         4. **Export:**
#            - Word: Best for editing
#            - LaTeX: Best for academic publishing
#            - Markdown: Best for note-taking apps
#            - BibTeX: Best for reference managers
#         """)
    
#     # Footer
#     st.markdown("---")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.markdown("🔬 **ResearchHub**")
#         st.caption("Version 2.0")
#     with col2:
#         st.markdown("📚 **Documentation**")
#         st.caption("[User Guide](#) | [API Docs](#)")
#     with col3:
#         st.markdown("💬 **Support**")
#         st.caption("[GitHub Issues](#) | [Discord](#)")


# if __name__ == "__main__":
#     main()





































# import streamlit as st
# from datetime import datetime
# import config
# from research_agent import research_agent
# from agents.cache_manager import cache
# from utils.error_handler import logger


# # Page configuration
# st.set_page_config(
#     page_title="AI Research Agent | Academic Paper Analysis",
#     page_icon="🔬",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Enhanced Custom CSS with Font Awesome Icons
# st.markdown("""
#     <style>
#     /* Import Google Fonts and Font Awesome */
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
#     @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
#     /* Global Styles */
#     * {
#         font-family: 'Inter', sans-serif;
#     }
    
#     /* Main container padding */
#     .block-container {
#         padding-top: 2rem;
#         padding-bottom: 3rem;
#     }
    
#     /* Header Section */
#     .main-header {
#         font-size: 2.8rem;
#         font-weight: 700;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         text-align: center;
#         margin-bottom: 0.5rem;
#         letter-spacing: -0.5px;
#     }
    
#     .logo-container {
#         text-align: center;
#         margin-bottom: 1rem;
#     }
    
#     .logo-icon {
#         font-size: 3.5rem;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#     }
    
#     .sub-header {
#         font-size: 1.1rem;
#         text-align: center;
#         color: #64748b;
#         margin-bottom: 2.5rem;
#         font-weight: 400;
#     }
    
#     /* Paper Card */
#     .paper-card {
#         background: linear-gradient(to bottom, #ffffff 0%, #f8fafc 100%);
#         padding: 2rem;
#         border-radius: 16px;
#         border: 1px solid #e2e8f0;
#         margin-bottom: 2rem;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
#         transition: all 0.3s ease;
#     }
    
#     .paper-card:hover {
#         box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
#         transform: translateY(-2px);
#     }
    
#     /* Status Badges */
#     .status-success {
#         color: #16a34a;
#         font-weight: 600;
#         background: #dcfce7;
#         padding: 2px 8px;
#         border-radius: 6px;
#     }
    
#     .status-failed {
#         color: #dc2626;
#         font-weight: 600;
#         background: #fee2e2;
#         padding: 2px 8px;
#         border-radius: 6px;
#     }
    
#     .status-pending {
#         color: #ca8a04;
#         font-weight: 600;
#         background: #fef3c7;
#         padding: 2px 8px;
#         border-radius: 6px;
#     }
    
#     /* Metric Cards */
#     .metric-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 1rem;
#         border-radius: 12px;
#         color: white;
#         text-align: center;
#         margin-bottom: 0.5rem;
#     }
    
#     /* Buttons */
#     .stButton>button {
#         border-radius: 10px;
#         font-weight: 500;
#         transition: all 0.3s ease;
#         border: none;
#     }
    
#     .stButton>button:hover {
#         transform: translateY(-1px);
#         box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
#     }
    
#     /* Sidebar */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
#     }
    
#     [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
#         color: #1e293b;
#         font-weight: 600;
#         font-size: 1.3rem;
#     }
    
#     [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
#         color: #475569;
#         font-weight: 600;
#         font-size: 1.1rem;
#         margin-top: 1rem;
#     }
    
#     /* Input Fields */
#     .stTextInput>div>div>input {
#         border-radius: 10px;
#         border: 2px solid #e2e8f0;
#         padding: 0.75rem;
#         font-size: 1rem;
#     }
    
#     .stTextInput>div>div>input:focus {
#         border-color: #667eea;
#         box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
#     }
    
#     /* Tabs */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 8px;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         border-radius: 8px 8px 0 0;
#         padding: 10px 20px;
#         font-weight: 500;
#     }
    
#     /* Expander */
#     .streamlit-expanderHeader {
#         border-radius: 10px;
#         background-color: #f8fafc;
#         font-weight: 500;
#     }
    
#     /* Alert Boxes */
#     .stAlert {
#         border-radius: 10px;
#         border: none;
#     }
    
#     /* Footer */
#     .footer {
#         position: relative;
#         bottom: 0;
#         width: 100%;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         text-align: center;
#         padding: 2rem 1rem;
#         margin-top: 4rem;
#         border-radius: 16px 16px 0 0;
#     }
    
#     .footer-content {
#         max-width: 1200px;
#         margin: 0 auto;
#     }
    
#     .footer-links {
#         display: flex;
#         justify-content: center;
#         gap: 2rem;
#         margin-top: 1rem;
#         flex-wrap: wrap;
#     }
    
#     .footer-link {
#         color: rgba(255, 255, 255, 0.9);
#         text-decoration: none;
#         font-weight: 500;
#         transition: all 0.3s ease;
#     }
    
#     .footer-link:hover {
#         color: white;
#         text-decoration: none;
#     }
    
#     /* Metadata badges */
#     .metadata-badge {
#         display: inline-block;
#         background: #f1f5f9;
#         color: #475569;
#         padding: 4px 12px;
#         border-radius: 20px;
#         font-size: 0.85rem;
#         margin-right: 8px;
#         margin-bottom: 8px;
#         font-weight: 500;
#     }
    
#     /* Paper index badge */
#     .paper-index {
#         display: inline-block;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         padding: 6px 14px;
#         border-radius: 10px;
#         font-weight: 600;
#         margin-right: 12px;
#         font-size: 1rem;
#     }
    
#     /* Error container */
#     .error-container {
#         background: #fef2f2;
#         border-left: 4px solid #dc2626;
#         padding: 1rem;
#         border-radius: 8px;
#         margin: 1rem 0;
#     }
    
#     /* Success container */
#     .success-container {
#         background: #f0fdf4;
#         border-left: 4px solid #16a34a;
#         padding: 1rem;
#         border-radius: 8px;
#         margin: 1rem 0;
#     }
    
#     /* Section dividers */
#     hr {
#         margin: 2rem 0;
#         border: none;
#         height: 1px;
#         background: linear-gradient(to right, transparent, #e2e8f0, transparent);
#     }
    
#     /* Icon styling */
#     .fa-icon {
#         margin-right: 8px;
#     }
    
#     .section-header {
#         display: flex;
#         align-items: center;
#         gap: 10px;
#         margin-bottom: 1rem;
#     }
    
#     .section-header i {
#         color: #667eea;
#         font-size: 1.2rem;
#     }
#     </style>
# """, unsafe_allow_html=True)


# def main():
#     # Logo and Header
#     st.markdown("""
#         <div class="logo-container">
#             <div class="logo-icon">
#                 <i class="fas fa-microscope"></i>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)
    
#     st.markdown('<div class="main-header">AI Research Agent</div>', unsafe_allow_html=True)
#     st.markdown(
#         '<div class="sub-header">Intelligently search, analyze, and extract insights from academic papers</div>',
#         unsafe_allow_html=True
#     )
    
#     # Sidebar configuration
#     with st.sidebar:
#         st.markdown('<h2><i class="fas fa-cog fa-icon"></i>Configuration</h2>', unsafe_allow_html=True)
        
#         # Search settings
#         st.markdown('<h3><i class="fas fa-search fa-icon"></i>Search Settings</h3>', unsafe_allow_html=True)
#         limit = st.slider(
#             "Number of papers",
#             min_value=1,
#             max_value=config.MAX_PAPER_LIMIT,
#             value=config.DEFAULT_PAPER_LIMIT,
#             help="Maximum number of papers to retrieve"
#         )
        
#         # Summary detail level
#         summary_level = st.selectbox(
#             "Summary Detail",
#             options=list(config.SUMMARY_LEVELS.keys()),
#             index=list(config.SUMMARY_LEVELS.keys()).index(config.DEFAULT_SUMMARY_LEVEL),
#             format_func=lambda x: f"{x.title()} - {config.SUMMARY_LEVELS[x]['description']}",
#             help="Choose how detailed the summaries should be"
#         )
        
#         # PDF processing
#         process_pdfs = st.checkbox(
#             "📄 Process PDFs",
#             value=True,
#             help="Download and analyze full paper PDFs (slower but more detailed)"
#         )
        
#         st.divider()
        
#         # Advanced filters
#         st.markdown('<h3><i class="fas fa-filter fa-icon"></i>Advanced Filters</h3>', unsafe_allow_html=True)
        
#         col1, col2 = st.columns(2)
#         with col1:
#             year_from = st.number_input(
#                 "Year from",
#                 min_value=1900,
#                 max_value=datetime.now().year,
#                 value=None,
#                 help="Filter papers from this year onwards"
#             )
#         with col2:
#             year_to = st.number_input(
#                 "Year to",
#                 min_value=1900,
#                 max_value=datetime.now().year,
#                 value=None,
#                 help="Filter papers up to this year"
#             )
        
#         open_access_only = st.checkbox(
#             "🔓 Open Access Only",
#             value=False,
#             help="Only show papers with freely available PDFs"
#         )
        
#         st.divider()
        
#         # Cache management
#         st.markdown('<h3><i class="fas fa-database fa-icon"></i>Cache Management</h3>', unsafe_allow_html=True)
#         cache_stats = cache.get_cache_stats()
        
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Topics", cache_stats.get("topic_cache_files", 0))
#             st.metric("Papers", cache_stats.get("paper_cache_files", 0))
#         with col2:
#             st.metric("Size", f"{cache_stats.get('total_size_mb', 0):.1f} MB")
        
#         st.markdown("")
#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("Clear Expired", use_container_width=True):
#                 removed = cache.clear_expired_cache()
#                 st.success(f"✓ Removed {sum(removed.values())} items")
#         with col2:
#             if st.button("Clear All", use_container_width=True):
#                 removed = cache.clear_all_cache()
#                 st.success(f"✓ Cleared {sum(removed.values())} items")
        
#         # Sidebar footer
#         st.divider()
#         st.markdown("""
#             <div style='text-align: center; color: #64748b; font-size: 0.85rem; padding: 1rem 0;'>
#                 <p><strong><i class="fas fa-microscope"></i> AI Research Agent</strong></p>
#                 <p>v1.0.0</p>
#             </div>
#         """, unsafe_allow_html=True)
    
#     # Main content
#     st.divider()
    
#     # Search input with improved layout
#     st.markdown('<div class="section-header"><i class="fas fa-search"></i><h3 style="margin: 0;">Search Academic Papers</h3></div>', unsafe_allow_html=True)
#     col1, col2 = st.columns([5, 1])
#     with col1:
#         query = st.text_input(
#             "Enter your research topic",
#             placeholder="e.g., 'machine learning for drug discovery'",
#             label_visibility="collapsed",
#             key="search_input"
#         )
#     with col2:
#         search_button = st.button("Search", type="primary", use_container_width=True)
    
#     # Example queries
#     with st.expander("💡 Example Queries", expanded=False):
#         st.markdown("Click any example to search:")
#         examples = [
#             "AI for antimicrobial resistance detection",
#             "climate change impact on biodiversity",
#             "quantum computing algorithms",
#             "CRISPR gene editing applications",
#             "renewable energy storage solutions"
#         ]
#         cols = st.columns(2)
#         for idx, example in enumerate(examples):
#             with cols[idx % 2]:
#                 if st.button(f"→ {example}", key=example, use_container_width=True):
#                     st.session_state.query = example
#                     st.rerun()
    
#     # Process search
#     if search_button or (query and st.session_state.get("query") == query):
#         if not query:
#             st.markdown("""
#                 <div class="error-container">
#                     <strong><i class="fas fa-exclamation-triangle"></i> Input Required</strong><br>
#                     Please enter a research topic to begin your search.
#                 </div>
#             """, unsafe_allow_html=True)
#             return
        
#         st.session_state.query = query
        
#         with st.spinner(f"Searching for papers on '{query}'..."):
#             try:
#                 papers = research_agent.search_and_analyze(
#                     query=query,
#                     limit=limit,
#                     summary_level=summary_level,
#                     process_pdfs=process_pdfs,
#                     year_from=year_from,
#                     year_to=year_to,
#                     open_access_only=open_access_only
#                 )
                
#                 if not papers:
#                     st.markdown("""
#                         <div class="error-container">
#                             <strong><i class="fas fa-times-circle"></i> No Results Found</strong><br>
#                             No papers found for your query. Try different keywords or adjust your filters.
#                         </div>
#                     """, unsafe_allow_html=True)
#                     return
                
#                 st.markdown(f"""
#                     <div class="success-container">
#                         <strong><i class="fas fa-check-circle"></i> Search Complete</strong><br>
#                         Found and analyzed <strong>{len(papers)}</strong> papers matching your query.
#                     </div>
#                 """, unsafe_allow_html=True)
                
#                 # Display results
#                 display_results(papers, summary_level)
                
#             except Exception as e:
#                 st.markdown(f"""
#                     <div class="error-container">
#                         <strong><i class="fas fa-exclamation-circle"></i> Error Occurred</strong><br>
#                         {str(e)}
#                     </div>
#                 """, unsafe_allow_html=True)
#                 logger.error(f"Search failed: {str(e)}")
    
#     # Footer
#     render_footer()


# def display_results(papers, summary_level):
#     """Display search results in a nice format"""
    
#     st.divider()
#     st.markdown(f'<div class="section-header"><i class="fas fa-chart-bar"></i><h2 style="margin: 0;">Results ({len(papers)} papers)</h2></div>', unsafe_allow_html=True)
    
#     # Add filter/sort options
#     col1, col2, col3 = st.columns([2, 2, 2])
#     with col1:
#         sort_by = st.selectbox(
#             "Sort by",
#             ["Relevance", "Year (Newest)", "Year (Oldest)", "Citations"],
#             key="sort_by"
#         )
    
#     # Sort papers
#     if sort_by == "Year (Newest)":
#         papers = sorted(papers, key=lambda x: x.get("year", 0), reverse=True)
#     elif sort_by == "Year (Oldest)":
#         papers = sorted(papers, key=lambda x: x.get("year", 0))
#     elif sort_by == "Citations":
#         papers = sorted(papers, key=lambda x: x.get("citation_count", 0), reverse=True)
    
#     st.markdown("")
    
#     # Display each paper
#     for i, paper in enumerate(papers, 1):
#         display_paper_card(paper, i, summary_level)


# def display_paper_card(paper, index, summary_level):
#     """Display a single paper in a card format"""
    
#     with st.container():
#         st.markdown(f'<div class="paper-card">', unsafe_allow_html=True)
        
#         # Header with title and metadata
#         col1, col2 = st.columns([5, 1])
#         with col1:
#             st.markdown(f"""
#                 <span class="paper-index">{index}</span>
#                 <strong style="font-size: 1.3rem; color: #1e293b;">{paper['title']}</strong>
#             """, unsafe_allow_html=True)
            
#             st.markdown("")
            
#             # Metadata row
#             authors_str = ", ".join(paper['authors'][:3])
#             if len(paper['authors']) > 3:
#                 authors_str += f" et al."
            
#             st.markdown(f"**<i class='fas fa-users'></i> Authors:** {authors_str}", unsafe_allow_html=True)
            
#             # Metadata badges
#             pdf_icon = "fa-file-pdf" if paper['has_pdf'] else "fa-lock"
#             pdf_text = "PDF Available" if paper['has_pdf'] else "PDF Unavailable"
            
#             st.markdown(f"""
#                 <div style="margin-top: 0.5rem;">
#                     <span class="metadata-badge"><i class="far fa-calendar"></i> {paper['year']}</span>
#                     <span class="metadata-badge"><i class="fas fa-book"></i> {paper['venue']}</span>
#                     <span class="metadata-badge"><i class="fas fa-quote-right"></i> {paper['citation_count']} citations</span>
#                     <span class="metadata-badge"><i class="fas {pdf_icon}"></i> {pdf_text}</span>
#                 </div>
#             """, unsafe_allow_html=True)
        
#         with col2:
#             st.markdown(f"[<i class='fas fa-external-link-alt'></i> View Paper]({paper['url']})", unsafe_allow_html=True)
        
#         st.markdown("")
        
#         # Tabs for different views
#         tab1, tab2, tab3, tab4, tab5 = st.tabs([
#             "📝 Summary", 
#             "🔬 Research Gaps", 
#             "💡 Key Findings", 
#             "📋 Citation", 
#             "⚡ Status"
#         ])
        
#         # Summary tab
#         with tab1:
#             st.markdown('<h4><i class="fas fa-align-left"></i> Abstract Summary</h4>', unsafe_allow_html=True)
#             st.write(paper.get("abstract_summary", "No summary available"))
            
#             if paper.get("pdf_summary"):
#                 st.markdown('<h4><i class="fas fa-file-alt"></i> Full Paper Summary</h4>', unsafe_allow_html=True)
#                 st.write(paper["pdf_summary"])
        
#         # Research Gaps tab
#         with tab2:
#             if paper.get("research_gaps"):
#                 gaps = paper["research_gaps"]
                
#                 st.markdown('<h4><i class="fas fa-wrench"></i> Methodology Gaps</h4>', unsafe_allow_html=True)
#                 st.write(gaps.get("methodology_gaps", "No analysis available"))
                
#                 st.markdown('<h4><i class="fas fa-book-open"></i> Knowledge Gaps</h4>', unsafe_allow_html=True)
#                 st.write(gaps.get("knowledge_gaps", "No analysis available"))
                
#                 st.markdown('<h4><i class="fas fa-rocket"></i> Future Directions</h4>', unsafe_allow_html=True)
#                 st.write(gaps.get("future_directions", "No analysis available"))
#             else:
#                 st.info("ℹ️ Research gap analysis not available (PDF not processed)")
        
#         # Key Findings tab
#         with tab3:
#             if paper.get("key_findings"):
#                 st.write(paper["key_findings"])
#             else:
#                 st.info("ℹ️ Key findings not available (PDF not processed)")
        
#         # Citation tab
#         with tab4:
#             citation = research_agent.generate_citation(paper, "APA")
#             st.code(citation, language=None)
#             if st.button(f"📋 Copy Citation", key=f"copy_{index}"):
#                 st.toast("✓ Citation copied to clipboard!")
        
#         # Status tab
#         with tab5:
#             status = paper.get("processing_status", {})
#             st.markdown("**<i class='fas fa-info-circle'></i> Processing Status:**", unsafe_allow_html=True)
#             st.markdown("")
#             for key, value in status.items():
#                 if value == "success":
#                     st.markdown(f'<i class="fas fa-check-circle" style="color: #16a34a;"></i> {key.replace("_", " ").title()}: <span class="status-success">SUCCESS</span>', unsafe_allow_html=True)
#                 elif value == "failed":
#                     st.markdown(f'<i class="fas fa-times-circle" style="color: #dc2626;"></i> {key.replace("_", " ").title()}: <span class="status-failed">FAILED</span>', unsafe_allow_html=True)
#                 elif value == "pending":
#                     st.markdown(f'<i class="fas fa-clock" style="color: #ca8a04;"></i> {key.replace("_", " ").title()}: <span class="status-pending">PENDING</span>', unsafe_allow_html=True)
#                 else:
#                     st.markdown(f'<i class="fas fa-circle" style="font-size: 0.5rem; color: #64748b;"></i> {key.replace("_", " ").title()}: {value.upper()}', unsafe_allow_html=True)
            
#             if paper.get("pdf_error"):
#                 st.markdown(f"""
#                     <div class="error-container" style="margin-top: 1rem;">
#                         <strong><i class="fas fa-exclamation-triangle"></i> PDF Error:</strong> {paper['pdf_error']}
#                     </div>
#                 """, unsafe_allow_html=True)
        
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("")


# def render_footer():
#     """Render the footer section"""
#     st.markdown("""
#         <div class="footer">
#             <div class="footer-content">
#                 <h3 style="margin-bottom: 0.5rem;">
#                     <i class="fas fa-microscope"></i> AI Research Agent
#                 </h3>
#                 <p style="opacity: 0.9; margin-bottom: 1rem;">
#                     Empowering researchers with AI-driven insights
#                 </p>
#                 <div class="footer-links">
#                     <a href="#" class="footer-link"><i class="fas fa-info-circle"></i> About</a>
#                     <a href="#" class="footer-link"><i class="fas fa-book"></i> Documentation</a>
#                     <a href="#" class="footer-link"><i class="fas fa-code"></i> API</a>
#                     <a href="#" class="footer-link"><i class="fas fa-life-ring"></i> Support</a>
#                     <a href="#" class="footer-link"><i class="fas fa-shield-alt"></i> Privacy Policy</a>
#                 </div>
#                 <p style="margin-top: 1.5rem; opacity: 0.8; font-size: 0.9rem;">
#                     <i class="far fa-copyright"></i> 2024 AI Research Agent. All rights reserved.
#                 </p>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)


# if __name__ == "__main__":
#     main()










































# import streamlit as st
# from datetime import datetime
# import config
# from research_agent import research_agent
# from agents.cache_manager import cache
# from utils.error_handler import logger


# # Page configuration
# st.set_page_config(
#     page_title="AI Research Agent | Academic Paper Analysis",
#     page_icon="🔬",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Enhanced Custom CSS
# st.markdown("""
#     <style>
#     /* Import Google Fonts */
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
#     /* Global Styles */
#     * {
#         font-family: 'Inter', sans-serif;
#     }
    
#     /* Main container padding */
#     .block-container {
#         padding-top: 2rem;
#         padding-bottom: 3rem;
#     }
    
#     /* Header Section */
#     .main-header {
#         font-size: 2.8rem;
#         font-weight: 700;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         text-align: center;
#         margin-bottom: 0.5rem;
#         letter-spacing: -0.5px;
#     }
    
#     .logo-container {
#         text-align: center;
#         margin-bottom: 1rem;
#     }
    
#     .logo-icon {
#         font-size: 3.5rem;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#     }
    
#     .sub-header {
#         font-size: 1.1rem;
#         text-align: center;
#         color: #64748b;
#         margin-bottom: 2.5rem;
#         font-weight: 400;
#     }
    
#     /* Paper Card */
#     .paper-card {
#         background: linear-gradient(to bottom, #ffffff 0%, #f8fafc 100%);
#         padding: 2rem;
#         border-radius: 16px;
#         border: 1px solid #e2e8f0;
#         margin-bottom: 2rem;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
#         transition: all 0.3s ease;
#     }
    
#     .paper-card:hover {
#         box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
#         transform: translateY(-2px);
#     }
    
#     /* Status Badges */
#     .status-success {
#         color: #16a34a;
#         font-weight: 600;
#         background: #dcfce7;
#         padding: 2px 8px;
#         border-radius: 6px;
#     }
    
#     .status-failed {
#         color: #dc2626;
#         font-weight: 600;
#         background: #fee2e2;
#         padding: 2px 8px;
#         border-radius: 6px;
#     }
    
#     .status-pending {
#         color: #ca8a04;
#         font-weight: 600;
#         background: #fef3c7;
#         padding: 2px 8px;
#         border-radius: 6px;
#     }
    
#     /* Metric Cards */
#     .metric-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 1rem;
#         border-radius: 12px;
#         color: white;
#         text-align: center;
#         margin-bottom: 0.5rem;
#     }
    
#     /* Buttons */
#     .stButton>button {
#         border-radius: 10px;
#         font-weight: 500;
#         transition: all 0.3s ease;
#         border: none;
#     }
    
#     .stButton>button:hover {
#         transform: translateY(-1px);
#         box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
#     }
    
#     /* Sidebar */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
#     }
    
#     [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
#         color: #1e293b;
#         font-weight: 600;
#         font-size: 1.3rem;
#     }
    
#     [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
#         color: #475569;
#         font-weight: 600;
#         font-size: 1.1rem;
#         margin-top: 1rem;
#     }
    
#     /* Input Fields */
#     .stTextInput>div>div>input {
#         border-radius: 10px;
#         border: 2px solid #e2e8f0;
#         padding: 0.75rem;
#         font-size: 1rem;
#     }
    
#     .stTextInput>div>div>input:focus {
#         border-color: #667eea;
#         box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
#     }
    
#     /* Tabs */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 8px;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         border-radius: 8px 8px 0 0;
#         padding: 10px 20px;
#         font-weight: 500;
#     }
    
#     /* Expander */
#     .streamlit-expanderHeader {
#         border-radius: 10px;
#         background-color: #f8fafc;
#         font-weight: 500;
#     }
    
#     /* Alert Boxes */
#     .stAlert {
#         border-radius: 10px;
#         border: none;
#     }
    
#     /* Footer */
#     .footer {
#         position: relative;
#         bottom: 0;
#         width: 100%;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         text-align: center;
#         padding: 2rem 1rem;
#         margin-top: 4rem;
#         border-radius: 16px 16px 0 0;
#     }
    
#     .footer-content {
#         max-width: 1200px;
#         margin: 0 auto;
#     }
    
#     .footer-links {
#         display: flex;
#         justify-content: center;
#         gap: 2rem;
#         margin-top: 1rem;
#         flex-wrap: wrap;
#     }
    
#     .footer-link {
#         color: rgba(255, 255, 255, 0.9);
#         text-decoration: none;
#         font-weight: 500;
#         transition: all 0.3s ease;
#     }
    
#     .footer-link:hover {
#         color: white;
#         text-decoration: none;
#     }
    
#     /* Metadata badges */
#     .metadata-badge {
#         display: inline-block;
#         background: #f1f5f9;
#         color: #475569;
#         padding: 4px 12px;
#         border-radius: 20px;
#         font-size: 0.85rem;
#         margin-right: 8px;
#         margin-bottom: 8px;
#         font-weight: 500;
#     }
    
#     /* Paper index badge */
#     .paper-index {
#         display: inline-block;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         padding: 6px 14px;
#         border-radius: 10px;
#         font-weight: 600;
#         margin-right: 12px;
#         font-size: 1rem;
#     }
    
#     /* Error container */
#     .error-container {
#         background: #fef2f2;
#         border-left: 4px solid #dc2626;
#         padding: 1rem;
#         border-radius: 8px;
#         margin: 1rem 0;
#     }
    
#     /* Success container */
#     .success-container {
#         background: #f0fdf4;
#         border-left: 4px solid #16a34a;
#         padding: 1rem;
#         border-radius: 8px;
#         margin: 1rem 0;
#     }
    
#     /* Section dividers */
#     hr {
#         margin: 2rem 0;
#         border: none;
#         height: 1px;
#         background: linear-gradient(to right, transparent, #e2e8f0, transparent);
#     }
#     </style>
# """, unsafe_allow_html=True)


# def main():
#     # Logo and Header
#     st.markdown("""
#         <div class="logo-container">
#             <div class="logo-icon">🔬</div>
#         </div>
#     """, unsafe_allow_html=True)
    
#     st.markdown('<div class="main-header">AI Research Agent</div>', unsafe_allow_html=True)
#     st.markdown(
#         '<div class="sub-header">Intelligently search, analyze, and extract insights from academic papers</div>',
#         unsafe_allow_html=True
#     )
    
#     # Sidebar configuration
#     with st.sidebar:
#         st.markdown("## ⚙️ Configuration")
        
#         # Search settings
#         st.markdown("### 🔍 Search Settings")
#         limit = st.slider(
#             "Number of papers",
#             min_value=1,
#             max_value=config.MAX_PAPER_LIMIT,
#             value=config.DEFAULT_PAPER_LIMIT,
#             help="Maximum number of papers to retrieve"
#         )
        
#         # Summary detail level
#         summary_level = st.selectbox(
#             "Summary Detail",
#             options=list(config.SUMMARY_LEVELS.keys()),
#             index=list(config.SUMMARY_LEVELS.keys()).index(config.DEFAULT_SUMMARY_LEVEL),
#             format_func=lambda x: f"{x.title()} - {config.SUMMARY_LEVELS[x]['description']}",
#             help="Choose how detailed the summaries should be"
#         )
        
#         # PDF processing
#         process_pdfs = st.checkbox(
#             "📄 Process PDFs",
#             value=True,
#             help="Download and analyze full paper PDFs (slower but more detailed)"
#         )
        
#         st.divider()
        
#         # Advanced filters
#         st.markdown("### 🎯 Advanced Filters")
        
#         col1, col2 = st.columns(2)
#         with col1:
#             year_from = st.number_input(
#                 "Year from",
#                 min_value=1900,
#                 max_value=datetime.now().year,
#                 value=None,
#                 help="Filter papers from this year onwards"
#             )
#         with col2:
#             year_to = st.number_input(
#                 "Year to",
#                 min_value=1900,
#                 max_value=datetime.now().year,
#                 value=None,
#                 help="Filter papers up to this year"
#             )
        
#         open_access_only = st.checkbox(
#             "🔓 Open Access Only",
#             value=False,
#             help="Only show papers with freely available PDFs"
#         )
        
#         st.divider()
        
#         # Cache management
#         st.markdown("### 💾 Cache Management")
#         cache_stats = cache.get_cache_stats()
        
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("📚 Topics", cache_stats.get("topic_cache_files", 0))
#             st.metric("📄 Papers", cache_stats.get("paper_cache_files", 0))
#         with col2:
#             st.metric("💿 Size", f"{cache_stats.get('total_size_mb', 0):.1f} MB")
        
#         st.markdown("")
#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("🗑️ Clear Expired", use_container_width=True):
#                 removed = cache.clear_expired_cache()
#                 st.success(f"✅ Removed {sum(removed.values())} items")
#         with col2:
#             if st.button("🧹 Clear All", use_container_width=True):
#                 removed = cache.clear_all_cache()
#                 st.success(f"✅ Cleared {sum(removed.values())} items")
        
#         # Sidebar footer
#         st.divider()
#         st.markdown("""
#             <div style='text-align: center; color: #64748b; font-size: 0.85rem; padding: 1rem 0;'>
#                 <p><strong>AI Research Agent</strong></p>
#                 <p>v1.0.0</p>
#             </div>
#         """, unsafe_allow_html=True)
    
#     # Main content
#     st.divider()
    
#     # Search input with improved layout
#     st.markdown("### 🔍 Search Academic Papers")
#     col1, col2 = st.columns([5, 1])
#     with col1:
#         query = st.text_input(
#             "Enter your research topic",
#             placeholder="e.g., 'machine learning for drug discovery'",
#             label_visibility="collapsed",
#             key="search_input"
#         )
#     with col2:
#         search_button = st.button("🔎 Search", type="primary", use_container_width=True)
    
#     # Example queries
#     with st.expander("💡 Example Queries", expanded=False):
#         st.markdown("Click any example to search:")
#         examples = [
#             "AI for antimicrobial resistance detection",
#             "climate change impact on biodiversity",
#             "quantum computing algorithms",
#             "CRISPR gene editing applications",
#             "renewable energy storage solutions"
#         ]
#         cols = st.columns(2)
#         for idx, example in enumerate(examples):
#             with cols[idx % 2]:
#                 if st.button(f"🔹 {example}", key=example, use_container_width=True):
#                     st.session_state.query = example
#                     st.rerun()
    
#     # Process search
#     if search_button or (query and st.session_state.get("query") == query):
#         if not query:
#             st.markdown("""
#                 <div class="error-container">
#                     <strong>⚠️ Input Required</strong><br>
#                     Please enter a research topic to begin your search.
#                 </div>
#             """, unsafe_allow_html=True)
#             return
        
#         st.session_state.query = query
        
#         with st.spinner(f"🔄 Searching for papers on '{query}'..."):
#             try:
#                 papers = research_agent.search_and_analyze(
#                     query=query,
#                     limit=limit,
#                     summary_level=summary_level,
#                     process_pdfs=process_pdfs,
#                     year_from=year_from,
#                     year_to=year_to,
#                     open_access_only=open_access_only
#                 )
                
#                 if not papers:
#                     st.markdown("""
#                         <div class="error-container">
#                             <strong>❌ No Results Found</strong><br>
#                             No papers found for your query. Try different keywords or adjust your filters.
#                         </div>
#                     """, unsafe_allow_html=True)
#                     return
                
#                 st.markdown(f"""
#                     <div class="success-container">
#                         <strong>✅ Search Complete</strong><br>
#                         Found and analyzed <strong>{len(papers)}</strong> papers matching your query.
#                     </div>
#                 """, unsafe_allow_html=True)
                
#                 # Display results
#                 display_results(papers, summary_level)
                
#             except Exception as e:
#                 st.markdown(f"""
#                     <div class="error-container">
#                         <strong>❌ Error Occurred</strong><br>
#                         {str(e)}
#                     </div>
#                 """, unsafe_allow_html=True)
#                 logger.error(f"Search failed: {str(e)}")
    
#     # Footer
#     render_footer()


# def display_results(papers, summary_level):
#     """Display search results in a nice format"""
    
#     st.divider()
#     st.markdown(f"## 📊 Results ({len(papers)} papers)")
    
#     # Add filter/sort options
#     col1, col2, col3 = st.columns([2, 2, 2])
#     with col1:
#         sort_by = st.selectbox(
#             "📈 Sort by",
#             ["Relevance", "Year (Newest)", "Year (Oldest)", "Citations"],
#             key="sort_by"
#         )
    
#     # Sort papers
#     if sort_by == "Year (Newest)":
#         papers = sorted(papers, key=lambda x: x.get("year", 0), reverse=True)
#     elif sort_by == "Year (Oldest)":
#         papers = sorted(papers, key=lambda x: x.get("year", 0))
#     elif sort_by == "Citations":
#         papers = sorted(papers, key=lambda x: x.get("citation_count", 0), reverse=True)
    
#     st.markdown("")
    
#     # Display each paper
#     for i, paper in enumerate(papers, 1):
#         display_paper_card(paper, i, summary_level)


# def display_paper_card(paper, index, summary_level):
#     """Display a single paper in a card format"""
    
#     with st.container():
#         st.markdown(f'<div class="paper-card">', unsafe_allow_html=True)
        
#         # Header with title and metadata
#         col1, col2 = st.columns([5, 1])
#         with col1:
#             st.markdown(f"""
#                 <span class="paper-index">{index}</span>
#                 <strong style="font-size: 1.3rem; color: #1e293b;">{paper['title']}</strong>
#             """, unsafe_allow_html=True)
            
#             st.markdown("")
            
#             # Metadata row
#             authors_str = ", ".join(paper['authors'][:3])
#             if len(paper['authors']) > 3:
#                 authors_str += f" et al."
            
#             st.markdown(f"**✍️ Authors:** {authors_str}")
            
#             # Metadata badges
#             st.markdown(f"""
#                 <div style="margin-top: 0.5rem;">
#                     <span class="metadata-badge">📅 {paper['year']}</span>
#                     <span class="metadata-badge">📚 {paper['venue']}</span>
#                     <span class="metadata-badge">📊 {paper['citation_count']} citations</span>
#                     <span class="metadata-badge">{'📄 PDF Available' if paper['has_pdf'] else '🔒 PDF Unavailable'}</span>
#                 </div>
#             """, unsafe_allow_html=True)
        
#         with col2:
#             st.markdown(f"[🔗 View Paper]({paper['url']})")
        
#         st.markdown("")
        
#         # Tabs for different views
#         tabs = st.tabs(["📝 Summary", "🔬 Research Gaps", "💡 Key Findings", "📋 Citation", "⚡ Status"])
        
#         # Summary tab
#         with tabs[0]:
#             st.markdown("#### Abstract Summary")
#             st.write(paper.get("abstract_summary", "No summary available"))
            
#             if paper.get("pdf_summary"):
#                 st.markdown("#### Full Paper Summary")
#                 st.write(paper["pdf_summary"])
        
#         # Research Gaps tab
#         with tabs[1]:
#             if paper.get("research_gaps"):
#                 gaps = paper["research_gaps"]
                
#                 st.markdown("#### 🔧 Methodology Gaps")
#                 st.write(gaps.get("methodology_gaps", "No analysis available"))
                
#                 st.markdown("#### 📖 Knowledge Gaps")
#                 st.write(gaps.get("knowledge_gaps", "No analysis available"))
                
#                 st.markdown("#### 🚀 Future Directions")
#                 st.write(gaps.get("future_directions", "No analysis available"))
#             else:
#                 st.info("ℹ️ Research gap analysis not available (PDF not processed)")
        
#         # Key Findings tab
#         with tabs[2]:
#             if paper.get("key_findings"):
#                 st.write(paper["key_findings"])
#             else:
#                 st.info("ℹ️ Key findings not available (PDF not processed)")
        
#         # Citation tab
#         with tabs[3]:
#             citation = research_agent.generate_citation(paper, "APA")
#             st.code(citation, language=None)
#             if st.button(f"📋 Copy Citation", key=f"copy_{index}"):
#                 st.toast("✅ Citation copied to clipboard!")
        
#         # Status tab
#         with tabs[4]:
#             status = paper.get("processing_status", {})
#             st.markdown("**Processing Status:**")
#             st.markdown("")
#             for key, value in status.items():
#                 if value == "success":
#                     st.markdown(f'✅ {key.replace("_", " ").title()}: <span class="status-success">SUCCESS</span>', unsafe_allow_html=True)
#                 elif value == "failed":
#                     st.markdown(f'❌ {key.replace("_", " ").title()}: <span class="status-failed">FAILED</span>', unsafe_allow_html=True)
#                 elif value == "pending":
#                     st.markdown(f'⏳ {key.replace("_", " ").title()}: <span class="status-pending">PENDING</span>', unsafe_allow_html=True)
#                 else:
#                     st.markdown(f'• {key.replace("_", " ").title()}: {value.upper()}')
            
#             if paper.get("pdf_error"):
#                 st.markdown(f"""
#                     <div class="error-container" style="margin-top: 1rem;">
#                         <strong>PDF Error:</strong> {paper['pdf_error']}
#                     </div>
#                 """, unsafe_allow_html=True)
        
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.markdown("")


# def render_footer():
#     """Render the footer section"""
#     st.markdown("""
#         <div class="footer">
#             <div class="footer-content">
#                 <h3 style="margin-bottom: 0.5rem;">🔬 AI Research Agent</h3>
#                 <p style="opacity: 0.9; margin-bottom: 1rem;">
#                     Empowering researchers with AI-driven insights
#                 </p>
#                 <div class="footer-links">
#                     <a href="#" class="footer-link">About</a>
#                     <a href="#" class="footer-link">Documentation</a>
#                     <a href="#" class="footer-link">API</a>
#                     <a href="#" class="footer-link">Support</a>
#                     <a href="#" class="footer-link">Privacy Policy</a>
#                 </div>
#                 <p style="margin-top: 1.5rem; opacity: 0.8; font-size: 0.9rem;">
#                     © 2024 AI Research Agent. All rights reserved.
#                 </p>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)


# if __name__ == "__main__":
#     main()


































# import streamlit as st
# from datetime import datetime
# import config
# from research_agent import research_agent
# from agents.cache_manager import cache
# from utils.error_handler import logger


# # Page configuration
# st.set_page_config(
#     page_title="AI Research Agent",
#     page_icon="🔬",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for better UI
# st.markdown("""
#     <style>
#     .main-header {
#         font-size: 3rem;
#         font-weight: bold;
#         color: #1f77b4;
#         text-align: center;
#         margin-bottom: 1rem;
#     }
#     .sub-header {
#         font-size: 1.2rem;
#         text-align: center;
#         color: #666;
#         margin-bottom: 2rem;
#     }
#     .paper-card {
#         background-color: #f8f9fa;
#         padding: 1.5rem;
#         border-radius: 10px;
#         border-left: 4px solid #1f77b4;
#         margin-bottom: 1.5rem;
#     }
#     .status-success {
#         color: #28a745;
#         font-weight: bold;
#     }
#     .status-failed {
#         color: #dc3545;
#         font-weight: bold;
#     }
#     .status-pending {
#         color: #ffc107;
#         font-weight: bold;
#     }
#     </style>
# """, unsafe_allow_html=True)


# def main():
#     # Header
#     st.markdown('<div class="main-header">AI Research Agent</div>', unsafe_allow_html=True)
#     st.markdown(
#         '<div class="sub-header">Intelligently search, analyze, and extract insights from academic papers</div>',
#         unsafe_allow_html=True
#     )
    
#     # Sidebar configuration
#     with st.sidebar:
#         st.header("Configuration")
        
#         # Search settings
#         st.subheader("Search Settings")
#         limit = st.slider(
#             "Number of papers",
#             min_value=1,
#             max_value=config.MAX_PAPER_LIMIT,
#             value=config.DEFAULT_PAPER_LIMIT,
#             help="Maximum number of papers to retrieve"
#         )
        
#         # Summary detail level
#         summary_level = st.selectbox(
#             "Summary Detail",
#             options=list(config.SUMMARY_LEVELS.keys()),
#             index=list(config.SUMMARY_LEVELS.keys()).index(config.DEFAULT_SUMMARY_LEVEL),
#             format_func=lambda x: f"{x.title()} - {config.SUMMARY_LEVELS[x]['description']}",
#             help="Choose how detailed the summaries should be"
#         )
        
#         # PDF processing
#         process_pdfs = st.checkbox(
#             "Process PDFs",
#             value=True,
#             help="Download and analyze full paper PDFs (slower but more detailed)"
#         )
        
#         st.divider()
        
#         # Advanced filters
#         st.subheader("Advanced Filters")
        
#         col1, col2 = st.columns(2)
#         with col1:
#             year_from = st.number_input(
#                 "Year from",
#                 min_value=1900,
#                 max_value=datetime.now().year,
#                 value=None,
#                 help="Filter papers from this year onwards"
#             )
#         with col2:
#             year_to = st.number_input(
#                 "Year to",
#                 min_value=1900,
#                 max_value=datetime.now().year,
#                 value=None,
#                 help="Filter papers up to this year"
#             )
        
#         open_access_only = st.checkbox(
#             "Open Access Only",
#             value=False,
#             help="Only show papers with freely available PDFs"
#         )
        
#         st.divider()
        
#         # Cache management
#         st.subheader("Cache Management")
#         cache_stats = cache.get_cache_stats()
#         # st.metric("Cached Topics", cache_stats["topic_cache_file"])
#         # st.metric("Cached Papers", cache_stats["paper_cache_file"])
#         st.metric("Cached Topics", cache_stats.get("topic_cache_files", 0))
#         st.metric("Cached Papers", cache_stats.get("paper_cache_files", 0))
#         st.metric("Total Cache Size", f"{cache_stats.get('total_size_mb', 0)} MB")
        
#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("Clear Expired", use_container_width=True):
#                 removed = cache.clear_expired_cache()
#                 st.success(f"Removed {sum(removed.values())} expired items")
#         with col2:
#             if st.button("Clear All", use_container_width=True):
#                 removed = cache.clear_all_cache()
#                 st.success(f"Cleared {sum(removed.values())} items")
    
#     # Main content
#     st.divider()
    
#     # Search input
#     col1, col2 = st.columns([4, 1])
#     with col1:
#         query = st.text_input(
#             "Enter your research topic",
#             placeholder="e.g., 'machine learning for drug discovery'",
#             label_visibility="collapsed"
#         )
#     with col2:
#         search_button = st.button("Search Papers", type="primary", use_container_width=True)
    
#     # Example queries
#     with st.expander("Example Queries"):
#         examples = [
#             "AI for antimicrobial resistance detection",
#             "climate change impact on biodiversity",
#             "quantum computing algorithms",
#             "CRISPR gene editing applications",
#             "renewable energy storage solutions"
#         ]
#         for example in examples:
#             if st.button(example, key=example):
#                 st.session_state.query = example
#                 st.rerun()
    
#     # Process search
#     if search_button or (query and st.session_state.get("query") == query):
#         if not query:
#             st.warning("Please enter a research topic")
#             return
        
#         st.session_state.query = query
        
#         with st.spinner(f"Searching for papers on '{query}'..."):
#             try:
#                 papers = research_agent.search_and_analyze(
#                     query=query,
#                     limit=limit,
#                     summary_level=summary_level,
#                     process_pdfs=process_pdfs,
#                     year_from=year_from,
#                     year_to=year_to,
#                     open_access_only=open_access_only
#                 )
                
#                 if not papers:
#                     st.error("No papers found for your query. Try different keywords.")
#                     return
                
#                 st.success(f"Found and analyzed {len(papers)} papers")
                
#                 # Display results
#                 display_results(papers, summary_level)
                
#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")
#                 logger.error(f"Search failed: {str(e)}")


# def display_results(papers, summary_level):
#     """Display search results in a nice format"""
    
#     st.divider()
#     st.header(f"Results ({len(papers)} papers)")
    
#     # Add filter/sort options
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         sort_by = st.selectbox(
#             "Sort by",
#             ["Relevance", "Year (Newest)", "Year (Oldest)", "Citations"],
#             key="sort_by"
#         )
    
#     # Sort papers
#     if sort_by == "Year (Newest)":
#         papers = sorted(papers, key=lambda x: x.get("year", 0), reverse=True)
#     elif sort_by == "Year (Oldest)":
#         papers = sorted(papers, key=lambda x: x.get("year", 0))
#     elif sort_by == "Citations":
#         papers = sorted(papers, key=lambda x: x.get("citation_count", 0), reverse=True)
    
#     # Display each paper
#     for i, paper in enumerate(papers, 1):
#         display_paper_card(paper, i, summary_level)


# def display_paper_card(paper, index, summary_level):
#     """Display a single paper in a card format"""
    
#     with st.container():
#         st.markdown(f'<div class="paper-card">', unsafe_allow_html=True)
        
#         # Header with title and metadata
#         col1, col2 = st.columns([4, 1])
#         with col1:
#             st.markdown(f"### {index}. {paper['title']}")
            
#             # Metadata row
#             authors_str = ", ".join(paper['authors'][:3])
#             if len(paper['authors']) > 3:
#                 authors_str += f" et al. ({len(paper['authors'])} authors)"
            
#             st.markdown(f"**Authors:** {authors_str}")
#             st.markdown(f"**Year:** {paper['year']} | **Venue:** {paper['venue']} | " +
#                        f"**Citations:** {paper['citation_count']} | " +
#                        f"**PDF:** {'Available' if paper['has_pdf'] else 'Not available'}")
        
#         with col2:
#             st.markdown(f"[View Paper]({paper['url']})")
        
#         # Tabs for different views
#         tabs = st.tabs(["Summary", "Research Gaps", "Key Findings", "Citation", "Status"])
        
#         # Summary tab
#         with tabs[0]:
#             st.markdown("#### Abstract Summary")
#             st.write(paper.get("abstract_summary", "No summary available"))
            
#             if paper.get("pdf_summary"):
#                 st.markdown("#### Full Paper Summary")
#                 st.write(paper["pdf_summary"])
        
#         # Research Gaps tab
#         with tabs[1]:
#             if paper.get("research_gaps"):
#                 gaps = paper["research_gaps"]
                
#                 st.markdown("#### Methodology Gaps")
#                 st.write(gaps.get("methodology_gaps", "No analysis available"))
                
#                 st.markdown("#### Knowledge Gaps")
#                 st.write(gaps.get("knowledge_gaps", "No analysis available"))
                
#                 st.markdown("#### Future Directions")
#                 st.write(gaps.get("future_directions", "No analysis available"))
#             else:
#                 st.info("Research gap analysis not available (PDF not processed)")
        
#         # Key Findings tab
#         with tabs[2]:
#             if paper.get("key_findings"):
#                 st.write(paper["key_findings"])
#             else:
#                 st.info("Key findings not available (PDF not processed)")
        
#         # Citation tab
#         with tabs[3]:
#             citation = research_agent.generate_citation(paper, "APA")
#             st.code(citation, language=None)
#             if st.button(f"Copy Citation", key=f"copy_{index}"):
#                 st.toast("Citation copied to clipboard!")
        
#         # Status tab
#         with tabs[4]:
#             status = paper.get("processing_status", {})
#             st.markdown("**Processing Status:**")
#             for key, value in status.items():
#                 status_class = f"status-{value}" if value in ["success", "failed", "pending"] else ""
#                 st.markdown(f"- {key.replace('_', ' ').title()}: " +
#                            f'<span class="{status_class}">{value.upper()}</span>',
#                            unsafe_allow_html=True)
            
#             if paper.get("pdf_error"):
#                 st.error(f"PDF Error: {paper['pdf_error']}")
        
#         st.markdown('</div>', unsafe_allow_html=True)
#         st.divider()


# if __name__ == "__main__":
#     main()
