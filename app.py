import streamlit as st
from datetime import datetime
from database.database import db
from utils.error_handler import logger
import plotly.graph_objects as go

st.set_page_config(
    page_title="ResearchHub Pro - Academic Research Assistant",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    db.create_tables()
    logger.info("Database initialized")
except Exception as e:
    logger.error(f"Database initialization failed: {str(e)}")

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

COLORS = {
    'dark': {
        'bg': '#0E1117', 'secondary_bg': '#1A1D29', 'card_bg': '#262730',
        'border': '#2D3139', 'text': '#FAFAFA', 'text_secondary': '#B0B3B8',
        'primary': '#6366F1', 'accent': '#10B981',
        'gradient_start': '#6366F1', 'gradient_end': '#8B5CF6',
    },
    'light': {
        'bg': '#FFFFFF', 'secondary_bg': '#F9FAFB', 'card_bg': '#FFFFFF',
        'border': '#E5E7EB', 'text': '#111827', 'text_secondary': '#6B7280',
        'primary': '#6366F1', 'accent': '#10B981',
        'gradient_start': '#6366F1', 'gradient_end': '#8B5CF6',
    }
}

theme = COLORS['dark' if st.session_state.dark_mode else 'light']

# ── Lucide SVG icon helper ────────────────────────────────────────────────────
def svg(name, size=16, color="currentColor"):
    paths = {
        "microscope":    '<path d="M6 18h8"/><path d="M3 22h18"/><path d="M14 22a7 7 0 1 0 0-14h-1"/><path d="M9 14h2"/><path d="M9 12a2 2 0 0 1-2-2V6h6v4a2 2 0 0 1-2 2Z"/><path d="M12 6V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3"/>',
        "search":        '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>',
        "folder-open":   '<path d="m6 14 1.5-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.54 6a2 2 0 0 1-1.95 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H18a2 2 0 0 1 2 2v2"/>',
        "file-text":     '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
        "bar-chart":     '<line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/>',
        "zap":           '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
        "database":      '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>',
        "save":          '<path d="M15.2 3a2 2 0 0 1 1.4.6l3.8 3.8a2 2 0 0 1 .6 1.4V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M17 21v-7a1 1 0 0 0-1-1H8a1 1 0 0 0-1 1v7"/><path d="M7 3v4a1 1 0 0 0 1 1h7"/>',
        "cpu":           '<rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>',
        "rocket":        '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
        "book-open":     '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
        "activity":      '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
        "moon":          '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
        "sun":           '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
        "trending-up":   '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
        "lightbulb":     '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
        "target":        '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
        "layout":        '<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><line x1="3" x2="21" y1="9" y2="9"/><line x1="9" x2="9" y1="21" y2="9"/>',
    }
    inner = paths.get(name, paths["search"])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
            f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{inner}</svg>')

def ic(name, size=16, color="currentColor"):
    return f'<span style="display:inline-flex;align-items:center;vertical-align:middle;margin-right:5px;">{svg(name,size,color)}</span>'
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * {{ font-family: 'Inter', sans-serif; }}
    .stApp {{ background: {theme['bg']}; color: {theme['text']}; }}
    .main-header {{
        font-size: 4.5rem; font-weight: 700; text-align: center; margin-bottom: 1rem;
        background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em; line-height: 1.1;
    }}
    .sub-header {{
        font-size: 1.25rem; text-align: center; margin-bottom: 3rem;
        color: {theme['text_secondary']}; font-weight: 400;
        max-width: 700px; margin-left: auto; margin-right: auto;
    }}
    .metric-card {{
        background: {theme['card_bg']}; border: 1px solid {theme['border']};
        border-radius: 16px; padding: 2rem 1.5rem; text-align: center;
        transition: all 0.3s ease; box-shadow: 0 1px 3px rgba(0,0,0,.1);
    }}
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(99,102,241,.15);
        border-color: {theme['primary']};
    }}
    .metric-value {{
        font-size: 3rem; font-weight: 700;
        background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: .5rem 0;
    }}
    .metric-label {{
        font-size: .875rem; color: {theme['text_secondary']}; font-weight: 500;
        text-transform: uppercase; letter-spacing: .05em;
    }}
    .feature-card {{
        background: {theme['card_bg']}; border: 1px solid {theme['border']};
        border-radius: 16px; padding: 2rem; margin: 1rem 0;
        transition: all 0.3s ease; position: relative; overflow: hidden;
    }}
    .feature-card::before {{
        content: ''; position: absolute; left: 0; top: 0; height: 100%; width: 4px;
        background: linear-gradient(180deg, {theme['gradient_start']}, {theme['gradient_end']});
        opacity: 0; transition: opacity 0.3s ease;
    }}
    .feature-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(99,102,241,.1);
        border-color: {theme['primary']};
    }}
    .feature-card:hover::before {{ opacity: 1; }}
    .feature-icon {{ margin-bottom: 1rem; }}
    .feature-title {{ font-size: 1.25rem; font-weight: 600; margin-bottom: .75rem; color: {theme['text']}; }}
    .feature-description {{ font-size: .95rem; color: {theme['text_secondary']}; line-height: 1.6; }}
    [data-testid="stSidebar"] {{
        background: {theme['secondary_bg']}; border-right: 1px solid {theme['border']};
    }}
    [data-testid="stSidebar"] .stButton > button {{
        background: {theme['card_bg']}; color: {theme['text']};
        border: 1px solid {theme['border']}; border-radius: 8px;
        font-weight: 500; transition: all .2s ease; width: 100%;
    }}
    [data-testid="stSidebar"] .stButton > button:hover {{
        background: {theme['primary']}; color: white;
        border-color: {theme['primary']}; transform: translateX(4px);
    }}
    .stat-mini {{
        background: {theme['card_bg']}; border: 1px solid {theme['border']};
        border-radius: 12px; padding: 1rem; margin: .5rem 0;
    }}
    .stat-mini-value {{ font-size: 1.75rem; font-weight: 700; color: {theme['primary']}; }}
    .stat-mini-label {{
        font-size: .8rem; color: {theme['text_secondary']};
        text-transform: uppercase; letter-spacing: .05em;
    }}
    .activity-item {{
        background: {theme['card_bg']}; border: 1px solid {theme['border']};
        border-radius: 12px; padding: 1rem 1.25rem; margin: .75rem 0;
        display: flex; align-items: center; gap: 1rem; transition: all .2s ease;
    }}
    .activity-item:hover {{ border-color: {theme['primary']}; transform: translateX(4px); }}
    .activity-icon {{
        width: 40px; height: 40px; border-radius: 10px;
        background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
        display: flex; align-items: center; justify-content: center;
        color: white; font-weight: 600; flex-shrink: 0;
    }}
    .stButton > button {{
        background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
        color: white; border: none; border-radius: 10px;
        padding: .75rem 2rem; font-weight: 600; font-size: 1rem;
        transition: all .3s ease; box-shadow: 0 4px 12px rgba(99,102,241,.3);
    }}
    .stButton > button:hover {{
        transform: translateY(-2px); box-shadow: 0 8px 20px rgba(99,102,241,.4);
    }}
    .section-header {{
        font-size: 2rem; font-weight: 700; margin: 3rem 0 1.5rem 0;
        color: {theme['text']}; display: flex; align-items: center; gap: .75rem;
    }}
    .section-header::before {{
        content: ''; width: 4px; height: 32px;
        background: linear-gradient(180deg, {theme['gradient_start']}, {theme['gradient_end']});
        border-radius: 2px;
    }}
    #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
    hr {{ border: none; height: 1px; background: {theme['border']}; margin: 2rem 0; }}
    </style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
        <div style="text-align:center;padding:1rem 0 2rem 0;">
            <div style="display:flex;align-items:center;justify-content:center;gap:8px;
                font-size:1.5rem;font-weight:700;
                background:linear-gradient(135deg,{theme['gradient_start']},{theme['gradient_end']});
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                {svg("microscope",24,theme['gradient_start'])} ResearchHub
            </div>
            <div style="font-size:.75rem;color:{theme['text_secondary']};margin-top:.25rem;">
                AI-Powered Research
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Dark/light toggle
    c1, c2 = st.columns([4, 1])
    with c1:
        mode_icon = svg("moon", 14) if st.session_state.dark_mode else svg("sun", 14)
        mode_label = "Light Mode" if st.session_state.dark_mode else "Dark Mode"
        st.markdown(f'<div style="display:flex;align-items:center;gap:6px;font-size:.875rem;font-weight:500;color:{theme["text"]};">{mode_icon}{mode_label}</div>',
                    unsafe_allow_html=True)
    with c2:
        if st.button("", key="toggle", help="Toggle theme"):
            toggle_dark_mode(); st.rerun()

    st.markdown("---")

    st.markdown(f'<p style="font-weight:600;font-size:.95rem;display:flex;align-items:center;gap:6px;">{svg("bar-chart",16)} Dashboard</p>',
                unsafe_allow_html=True)
    try:
        stats = db.get_statistics()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="stat-mini"><div class="stat-mini-value">{stats.get("total_projects",0)}</div><div class="stat-mini-label">Projects</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-mini"><div class="stat-mini-value">{stats.get("total_papers",0)}</div><div class="stat-mini-label">Papers</div></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="stat-mini"><div class="stat-mini-value">{stats.get("total_searches",0)}</div><div class="stat-mini-label">Searches</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-mini"><div class="stat-mini-value">{stats.get("total_reviews",0)}</div><div class="stat-mini-label">Reviews</div></div>', unsafe_allow_html=True)
    except:
        st.info("Initialising database…")

    st.markdown("---")

    st.markdown(f'<p style="font-weight:600;font-size:.95rem;display:flex;align-items:center;gap:6px;">{svg("zap",16)} Quick Access</p>',
                unsafe_allow_html=True)

    if st.button(f"Search Papers",     use_container_width=True): st.switch_page("pages/Search.py")
    if st.button(f"My Projects",       use_container_width=True): st.switch_page("pages/Projects.py")
    if st.button(f"Generate Review",   use_container_width=True): st.switch_page("pages/Literature_Review.py")

    st.markdown("---")

    st.markdown(f'<p style="font-weight:600;font-size:.95rem;display:flex;align-items:center;gap:6px;">{svg("activity",16)} System Status</p>',
                unsafe_allow_html=True)
    st.markdown(f"""
        <div class="stat-mini">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="color:{theme['text_secondary']};font-size:.85rem;">{svg("cpu",12)} API Status</span>
                <span style="color:{theme['accent']};font-size:.85rem;">● Online</span>
            </div>
        </div>
        <div class="stat-mini">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="color:{theme['text_secondary']};font-size:.85rem;">{svg("database",12)} Database</span>
                <span style="color:{theme['accent']};font-size:.85rem;">● Connected</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f'<div style="text-align:center;padding:1rem 0;color:{theme["text_secondary"]};font-size:.75rem;"><div style="margin-bottom:.5rem;">Version 2.0.1</div><div>© 2024 ResearchHub</div></div>',
                unsafe_allow_html=True)


# ── Main content ──────────────────────────────────────────────────────────────
def main():
    st.markdown('<div class="main-header">ResearchHub Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Transform weeks of literature review into minutes. AI-powered research assistant for academics and researchers.</div>', unsafe_allow_html=True)

    # CTA buttons
    _, c2, c3, c4, _ = st.columns([1, 1.5, 1.5, 1.5, 1])
    with c2:
        if st.button("Get Started",   key="hero_cta",  use_container_width=True): st.switch_page("pages/Search.py")
    with c3:
        if st.button("View Demo",     key="demo_cta",  use_container_width=True): st.info("Demo coming soon!")
    with c4:
        if st.button("Documentation", key="docs_cta",  use_container_width=True): st.info("Documentation coming soon!")

    st.markdown("<br>", unsafe_allow_html=True)

    # Key metrics
    c1, c2, c3, c4 = st.columns(4)
    metrics = [("10x","Faster Research"), ("2M+","Papers Indexed"), ("98%","Accuracy Rate"), ("24/7","AI Assistant")]
    for col, (val, label) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

    # Core features
    st.markdown('<div class="section-header">Core Features</div>', unsafe_allow_html=True)

    features = [
        [
            ("search",      "Intelligent Search",       "Search across multiple academic databases simultaneously. Get AI-powered summaries, identify research gaps, and extract key findings instantly."),
            ("cpu",         "AI Summarisation",         "Advanced NLP models extract key insights from papers. Understand complex research in seconds, not hours."),
        ],
        [
            ("bar-chart",   "Visual Analytics",         "Interactive charts and graphs reveal trends in your research. Citation networks, topic clusters, and temporal analysis."),
            ("file-text",   "Auto Literature Review",   "Generate publication-ready literature reviews automatically. 5–10 pages of academic-quality writing in minutes."),
        ],
        [
            ("layout",      "Smart Organisation",       "Manage projects with tags, notes, and annotations. Advanced filtering and search within your library."),
            ("save",        "Universal Export",         "Export to Word, PDF, LaTeX, Markdown, BibTeX, or JSON. Seamlessly integrate with your existing workflow."),
        ],
    ]

    cols = st.columns(3)
    for col, feature_pair in zip(cols, features):
        with col:
            for icon_name, title, desc in feature_pair:
                st.markdown(f"""
                    <div class="feature-card">
                        <div class="feature-icon">{svg(icon_name, 28, theme['primary'])}</div>
                        <div class="feature-title">{title}</div>
                        <div class="feature-description">{desc}</div>
                    </div>
                """, unsafe_allow_html=True)

    # Recent activity
    st.markdown('<div class="section-header">Recent Activity</div>', unsafe_allow_html=True)

    try:
        recent_searches = db.get_recent_searches(limit=5)
        if recent_searches:
            for search in recent_searches:
                st.markdown(f"""
                    <div class="activity-item">
                        <div class="activity-icon">{svg("search", 18, "white")}</div>
                        <div style="flex:1;">
                            <div style="font-weight:600;color:{theme['text']};">{search.query}</div>
                            <div style="font-size:.85rem;color:{theme['text_secondary']};margin-top:.25rem;">
                                {search.results_count} papers &bull; {search.created_at.strftime('%B %d, %Y at %I:%M %p')}
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="text-align:center;padding:3rem;color:{theme['text_secondary']};">
                    <div style="margin-bottom:1rem;">{svg("book-open", 48, theme['text_secondary'])}</div>
                    <div style="font-size:1.1rem;font-weight:500;">No activity yet</div>
                    <div style="margin-top:.5rem;">Start by searching for papers to see your activity here</div>
                </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown(f"""
            <div style="text-align:center;padding:3rem;color:{theme['text_secondary']};">
                <div style="margin-bottom:1rem;">{svg("rocket", 48, theme['text_secondary'])}</div>
                <div style="font-size:1.1rem;font-weight:500;">Start your research journey</div>
                <div style="margin-top:.5rem;">Begin searching to track your activity</div>
            </div>
        """, unsafe_allow_html=True)

    # Quick tips
    st.markdown('<div class="section-header">Quick Tips</div>', unsafe_allow_html=True)

    tips = [
        ("search",    "Search Best Practices",
         "Use specific keywords<br>Filter by publication year<br>Enable open access filter<br>Try different databases"),
        ("book-open", "Review Generation",
         "Process 10+ papers minimum<br>Enable PDF processing<br>Use medium detail level<br>Add custom instructions"),
        ("target",    "Project Management",
         "Use descriptive names<br>Add relevant tags<br>Take detailed notes<br>Regular backups"),
    ]

    cols = st.columns(3)
    for col, (icon_name, title, body) in zip(cols, tips):
        with col:
            st.markdown(f"""
                <div class="feature-card">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:.75rem;">
                        {svg(icon_name, 20, theme['primary'])}
                        <div class="feature-title" style="margin:0;">{title}</div>
                    </div>
                    <div class="feature-description">• {body.replace("<br>", "<br>• ")}</div>
                </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()