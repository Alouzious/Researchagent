import streamlit as st
import config
from agents.cache_manager import cache
from database.database import db
from utils.error_handler import logger
import os

st.set_page_config(page_title="Settings", page_icon="", layout="wide")

# ── Lucide SVG icon helper ────────────────────────────────────────────────────
def svg(name, size=16, color="currentColor"):
    paths = {
        "settings":      '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
        "palette":       '<circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/>',
        "sliders":       '<line x1="4" x2="4" y1="21" y2="14"/><line x1="4" x2="4" y1="6" y2="3"/><line x1="12" x2="12" y1="21" y2="12"/><line x1="12" x2="12" y1="4" y2="3"/><line x1="20" x2="20" y1="21" y2="16"/><line x1="20" x2="20" y1="8" y2="3"/><line x1="1" x2="7" y1="14" y2="14"/><line x1="9" x2="15" y1="12" y2="12"/><line x1="17" x2="23" y1="16" y2="16"/>',
        "package":       '<path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
        "database":      '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>',
        "info":          '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
        "moon":          '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
        "sun":           '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
        "monitor":       '<rect width="20" height="14" x="2" y="3" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/>',
        "search":        '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>',
        "file-text":     '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
        "key":           '<path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"/><path d="m21 2-9.6 9.6"/><circle cx="7.5" cy="15.5" r="5.5"/>',
        "trash-2":       '<path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/>',
        "alert-triangle":'<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
        "bar-chart":     '<line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/>',
        "lightbulb":     '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
        "heart":         '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
        "link":          '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
        "microscope":    '<path d="M6 18h8"/><path d="M3 22h18"/><path d="M14 22a7 7 0 1 0 0-14h-1"/><path d="M9 14h2"/><path d="M9 12a2 2 0 0 1-2-2V6h6v4a2 2 0 0 1-2 2Z"/><path d="M12 6V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3"/>',
    }
    inner = paths.get(name, paths["settings"])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
            f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{inner}</svg>')

def ic(name, size=16, color="currentColor"):
    return f'<span style="display:inline-flex;align-items:center;vertical-align:middle;margin-right:5px;">{svg(name,size,color)}</span>'

def hdr(icon_name, text, level="h2", size=22, color="currentColor"):
    return (f'<{level} style="display:flex;align-items:center;gap:8px;margin-bottom:.4rem;">'
            f'{svg(icon_name,size,color)}{text}</{level}>')
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state.get('dark_mode', False):
    st.markdown("<style>.stApp{background:#1E1E1E;color:#E0E0E0;}</style>", unsafe_allow_html=True)

st.markdown("""
    <style>
    .settings-section{background-color:var(--background-color);padding:1.5rem;border-radius:10px;
        border-left:4px solid #1f77b4;margin:1rem 0;}
    .danger-zone{background-color:var(--background-color);padding:1.5rem;border-radius:10px;
        border-left:4px solid #dc3545;margin:1rem 0;}
    </style>""", unsafe_allow_html=True)


def main():
    st.markdown(hdr("settings", "Settings & Configuration", "h1", 28), unsafe_allow_html=True)
    st.markdown("Manage your application settings and preferences")

    tabs = st.tabs(["Appearance","Configuration","Cache","Database","About"])
    with tabs[0]: show_appearance_settings()
    with tabs[1]: show_configuration_settings()
    with tabs[2]: show_cache_management()
    with tabs[3]: show_database_management()
    with tabs[4]: show_about_info()


def show_appearance_settings():
    st.markdown(hdr("palette", "Appearance Settings", "h2", 22), unsafe_allow_html=True)
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown(hdr("moon", "Dark Mode", "h3", 18), unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1: st.write("Toggle between light and dark themes")
    with c2:
        current_mode = "Dark" if st.session_state.get('dark_mode', False) else "Light"
        if st.button(f"Switch to {'Light' if current_mode == 'Dark' else 'Dark'}", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.get('dark_mode', False); st.rerun()
    st.caption(f"Current mode: **{current_mode}**")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown(hdr("monitor", "UI Preferences", "h3", 18), unsafe_allow_html=True)
    st.info("Additional UI customisation options coming soon!")
    st.markdown('</div>', unsafe_allow_html=True)


def show_configuration_settings():
    st.markdown(hdr("sliders", "Configuration Settings", "h2", 22), unsafe_allow_html=True)

    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown(hdr("search", "Search Defaults", "h3", 18), unsafe_allow_html=True)
    st.number_input("Default number of papers", min_value=1,
        max_value=config.MAX_PAPER_LIMIT, value=config.DEFAULT_PAPER_LIMIT)
    st.selectbox("Default summary level", options=list(config.SUMMARY_LEVELS.keys()),
        index=list(config.SUMMARY_LEVELS.keys()).index(config.DEFAULT_SUMMARY_LEVEL),
        format_func=lambda x: f"{x.title()} - {config.SUMMARY_LEVELS[x]['description']}")
    st.checkbox("Process PDFs by default", value=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown(hdr("file-text", "Literature Review Defaults", "h3", 18), unsafe_allow_html=True)
    st.selectbox("Default review type", options=config.LIT_REVIEW_TYPES,
        index=config.LIT_REVIEW_TYPES.index(config.DEFAULT_LIT_REVIEW_TYPE),
        format_func=lambda x: x.title())
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown(hdr("key", "API Configuration", "h3", 18), unsafe_allow_html=True)
    groq_status = "Configured" if config.GROQ_API_KEY else "Not configured"
    sem_status  = "Configured" if config.SEMANTIC_SCHOLAR_API_KEY else "Optional (not set)"
    st.markdown(f'{ic("key",14)} **Groq API Key:** {groq_status}', unsafe_allow_html=True)
    st.markdown(f'{ic("key",14)} **Semantic Scholar API Key:** {sem_status}', unsafe_allow_html=True)
    st.info("API keys are configured in the `.env` file. See documentation for setup instructions.")
    st.markdown('</div>', unsafe_allow_html=True)


def show_cache_management():
    st.markdown(hdr("package", "Cache Management", "h2", 22), unsafe_allow_html=True)
    try:
        cache_stats = cache.get_cache_stats()
        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        st.markdown(hdr("bar-chart", "Cache Statistics", "h3", 18), unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Topic Searches",  cache_stats['topic_cache_files'])
        c2.metric("Cached Papers",   cache_stats['paper_cache_files'])
        c3.metric("Total Size",      f"{cache_stats['total_size_mb']:.2f} MB")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        st.markdown(hdr("sliders", "Cache Actions", "h3", 18), unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Clear Expired Cache**")
            st.caption(f"Remove items older than {config.CACHE_EXPIRY_DAYS} days")
            if st.button("Clear Expired", use_container_width=True):
                removed = cache.clear_expired_cache()
                st.success(f"Removed {sum(removed.values())} expired items"); st.rerun()
        with c2:
            st.write("**Clear All Cache**")
            st.caption("Remove all cached data")
            if st.button("Clear All", type="secondary", use_container_width=True):
                if st.session_state.get('confirm_clear_cache'):
                    removed = cache.clear_all_cache()
                    st.success(f"Cleared {sum(removed.values())} items")
                    st.session_state.confirm_clear_cache = False; st.rerun()
                else:
                    st.session_state.confirm_clear_cache = True
                    st.warning("Click again to confirm")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        st.markdown(hdr("lightbulb", "Cache Benefits", "h3", 18), unsafe_allow_html=True)
        st.markdown("""
- **Faster searches:** Repeated queries return instantly
- **Reduced API calls:** Saves rate limits
- **Lower costs:** Fewer API requests
- **Offline access:** View cached results without internet

**Best practice:** Clear expired cache periodically to free up space.
""")
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading cache statistics: {str(e)}")
        logger.error(f"Cache stats error: {str(e)}")


def show_database_management():
    st.markdown(hdr("database", "Database Management", "h2", 22), unsafe_allow_html=True)
    try:
        stats = db.get_statistics()
        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        st.markdown(hdr("bar-chart", "Database Statistics", "h3", 18), unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Projects", stats['total_projects'])
        c2.metric("Papers",   stats['total_papers'])
        c3.metric("Searches", stats['total_searches'])
        c4.metric("With PDFs", stats['papers_with_pdf'])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        st.markdown(hdr("info", "Database Information", "h3", 18), unsafe_allow_html=True)
        database_url = os.getenv('DATABASE_URL', 'sqlite:///./research_agent.db')
        db_type = "PostgreSQL" if database_url.startswith('postgresql') else "SQLite"
        st.write(f"**Type:** {db_type}")
        st.write(f"**Location:** {'Cloud (PostgreSQL)' if db_type == 'PostgreSQL' else 'Local (SQLite)'}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="danger-zone">', unsafe_allow_html=True)
        st.markdown(hdr("alert-triangle", "Danger Zone", "h3", 18, "#dc3545"), unsafe_allow_html=True)
        st.warning("These actions are irreversible!")
        if st.button("Reset Database", type="secondary"):
            st.error("This feature is disabled for safety. Delete the database file manually to reset.")
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading database statistics: {str(e)}")
        logger.error(f"Database stats error: {str(e)}")


def show_about_info():
    st.markdown(hdr("info", "About AI Research Agent", "h2", 22), unsafe_allow_html=True)

    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown(hdr("microscope", "Application Information", "h3", 18), unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Version:** 2.0.0 (Phase 2)")
        st.write("**Release:** December 2024")
        st.write("**License:** MIT (Open Source)")
    with c2:
        st.write("**Platform:** Streamlit")
        st.write("**AI Model:** LLaMA 3.1 (via Groq)")
        st.write("**Database:** PostgreSQL / SQLite")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown(hdr("lightbulb", "Features", "h3", 18), unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""**Search & Analysis:**
- Multi-database search (Semantic Scholar, ArXiv)
- AI-powered summaries
- Research gap identification
- Key findings extraction
- Automatic deduplication""")
    with c2:
        st.markdown("""**Organisation & Export:**
- Project management
- Literature review generator
- 7 export formats
- Notes and annotations
- Search history""")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown(hdr("heart", "Credits & Acknowledgments", "h3", 18), unsafe_allow_html=True)
    st.markdown("""**Built with:**
- [Streamlit](https://streamlit.io) — Web framework
- [Groq](https://groq.com) — Fast LLM inference
- [Semantic Scholar](https://www.semanticscholar.org) — Academic search API
- [ArXiv](https://arxiv.org) — Preprint repository""")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown(hdr("link", "Useful Links", "h3", 18), unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Documentation**")
        st.markdown("- [User Guide](#)\n- [API Docs](#)\n- [FAQ](#)")
    with c2:
        st.markdown("**Community**")
        st.markdown("- [GitHub](#)\n- [Discord](#)\n- [Forum](#)")
    with c3:
        st.markdown("**Support**")
        st.markdown("- [Report Bug](#)\n- [Request Feature](#)\n- [Contact](#)")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f'{ic("microscope",14)} ResearchHub — Making research accessible to everyone', unsafe_allow_html=True)
    st.caption("© 2025 — Open Source Project")


if __name__ == "__main__":
    main()