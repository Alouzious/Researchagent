import streamlit as st
from datetime import datetime
import config
from database.database import db
from agents.literature_review_agent import lit_review_agent
from utils.error_handler import logger

st.set_page_config(page_title="Literature Review", page_icon="", layout="wide")

# ── Lucide SVG icon helper ────────────────────────────────────────────────────
def svg(name, size=16, color="currentColor"):
    paths = {
        "file-text":  '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
        "settings":   '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
        "book-open":  '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
        "target":     '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
        "save":       '<path d="M15.2 3a2 2 0 0 1 1.4.6l3.8 3.8a2 2 0 0 1 .6 1.4V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M17 21v-7a1 1 0 0 0-1-1H8a1 1 0 0 0-1 1v7"/><path d="M7 3v4a1 1 0 0 0 1 1h7"/>',
        "zap":        '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
        "search":     '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>',
        "sparkles":   '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>',
        "download":   '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>',
        "refresh-cw": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
        "eye":        '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
        "folder":     '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
        "clock":      '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
        "check":      '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
    }
    inner = paths.get(name, paths["file-text"])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
            f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{inner}</svg>')

def ic(name, size=16, color="currentColor"):
    return f'<span style="display:inline-flex;align-items:center;vertical-align:middle;margin-right:5px;">{svg(name,size,color)}</span>'

def hdr(icon_name, text, level="h2", size=22):
    return (f'<{level} style="display:flex;align-items:center;gap:8px;margin-bottom:.4rem;">'
            f'{svg(icon_name,size)}{text}</{level}>')
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state.get('dark_mode', False):
    st.markdown("<style>.stApp{background:#1E1E1E;color:#E0E0E0;}</style>", unsafe_allow_html=True)

st.markdown("""
    <style>
    .review-preview{background-color:var(--background-color);padding:2rem;border-radius:10px;
        border-left:4px solid #7b1fa2;margin:1rem 0;max-height:600px;overflow-y:auto;}
    .stat-box{background-color:var(--secondary-background-color);padding:1rem;border-radius:8px;
        text-align:center;margin:.5rem 0;}
    </style>""", unsafe_allow_html=True)

if 'generated_review' not in st.session_state:
    st.session_state.generated_review = None
if 'review_papers' not in st.session_state:
    st.session_state.review_papers = []


def main():
    st.markdown(hdr("file-text", "Literature Review Generator", "h1", 28), unsafe_allow_html=True)
    st.markdown("Generate comprehensive literature reviews in minutes, powered by AI")

    with st.sidebar:
        st.markdown(hdr("settings", "Review Configuration", "h3", 18), unsafe_allow_html=True)
        st.markdown(hdr("book-open", "Paper Source", "h4", 15), unsafe_allow_html=True)
        source = st.radio("Select papers from",
            ["Recent Search","Saved Project","Custom Selection"], label_visibility="collapsed")

        selected_papers = []
        if source == "Recent Search":
            if st.session_state.get('search_results'):
                selected_papers = st.session_state.search_results
                st.success(f"{len(selected_papers)} papers from last search")
            else:
                st.warning("No recent search. Go to Search page first.")
        elif source == "Saved Project":
            projects = db.get_all_projects()
            if projects:
                selected_project_name = st.selectbox("Select project", [p.name for p in projects])
                selected_project = next(p for p in projects if p.name == selected_project_name)
                papers = db.get_project_papers(selected_project.id)
                selected_papers = [{
                    'title': p.title, 'authors': p.authors or [], 'year': p.year,
                    'abstract': p.abstract, 'abstract_summary': p.abstract_summary_medium,
                    'key_findings': p.key_findings,
                    'research_gaps': {'methodology_gaps': p.methodology_gaps,
                                      'knowledge_gaps': p.knowledge_gaps,
                                      'future_directions': p.future_directions}
                } for p in papers]
                st.success(f"{len(selected_papers)} papers from project")
            else:
                st.warning("No projects yet. Create one first.")

        st.session_state.review_papers = selected_papers
        st.divider()

        st.markdown(hdr("target", "Review Settings", "h4", 15), unsafe_allow_html=True)
        detail_level = st.select_slider("Detail Level", options=["short","medium","long"],
                                        value="medium", format_func=lambda x: x.title())
        st.caption(config.LIT_REVIEW_DETAIL_LEVELS[detail_level]["description"])
        review_type = st.selectbox("Organization Type", options=config.LIT_REVIEW_TYPES,
                                   format_func=lambda x: x.title())
        st.divider()

        st.markdown(hdr("save", "Options", "h4", 15), unsafe_allow_html=True)
        save_to_db = st.checkbox("Save to database", value=True)
        if save_to_db:
            projects = db.get_all_projects()
            if projects:
                project_names = ["None"] + [p.name for p in projects]
                selected_proj = st.selectbox("Associate with project", project_names)
                st.session_state.review_project = (
                    next(p.id for p in projects if p.name == selected_proj)
                    if selected_proj != "None" else None)
            else:
                st.session_state.review_project = None

    if not st.session_state.review_papers:
        show_getting_started()
    elif st.session_state.generated_review:
        show_review_results(st.session_state.generated_review)
    else:
        show_generation_interface(detail_level, review_type, save_to_db)


def show_getting_started():
    st.info("Welcome to the Literature Review Generator!")
    st.markdown("""
### How It Works
1. **Select Papers** — choose from your recent search or a saved project
2. **Configure** — pick detail level and organisation type
3. **Generate** — AI creates a comprehensive literature review
4. **Export** — download in Word, PDF, LaTeX, Markdown and more

### What You Get
- Introduction with context and scope
- Thematic analysis of papers
- Methodological approaches overview
- Synthesis of key findings
- Research gaps and future directions
- Conclusion and references

**Time savings:** write in 10 minutes what takes 30–50 hours manually!
""")
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(hdr("search", "Start with Search", "h3", 18), unsafe_allow_html=True)
        st.write("Search for papers and generate a review from the results")
        if st.button("Go to Search", use_container_width=True): st.switch_page("pages/Search.py")
    with c2:
        st.markdown(hdr("folder", "Use Existing Project", "h3", 18), unsafe_allow_html=True)
        st.write("Generate a review from papers in your projects")
        if st.button("Go to Projects", use_container_width=True): st.switch_page("pages/Projects.py")


def show_generation_interface(detail_level, review_type, save_to_db):
    papers = st.session_state.review_papers
    st.markdown(hdr("book-open", f"Selected Papers ({len(papers)})", "h2", 22), unsafe_allow_html=True)

    papers_with_summaries = sum(1 for p in papers if p.get('abstract_summary') or p.get('abstract'))
    papers_with_gaps = sum(1 for p in papers if p.get('research_gaps'))
    quality_score = int((papers_with_summaries / len(papers)) * 100)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Papers", len(papers))
    c2.metric("With Summaries", papers_with_summaries)
    c3.metric("With Gap Analysis", papers_with_gaps)
    c4.metric("Quality Score", f"{quality_score}%")

    if quality_score < 50:
        st.warning("Low quality score. Consider processing PDFs for better results.")

    with st.expander("View Paper List"):
        for i, p in enumerate(papers[:10], 1):
            st.write(f"{i}. **{p.get('title','Untitled')}** ({p.get('year','N/A')})")
        if len(papers) > 10:
            st.write(f"... and {len(papers)-10} more")

    st.divider()
    st.markdown(hdr("settings", "Review Configuration", "h2", 22), unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.markdown("**Detail Level**"); st.markdown(detail_level.title())
        st.caption(config.LIT_REVIEW_DETAIL_LEVELS[detail_level]["description"])
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.markdown("**Organisation**"); st.markdown(review_type.title())
        st.caption("How papers will be organised")
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        est_words = config.LIT_REVIEW_DETAIL_LEVELS[detail_level]["target_words"]
        est_pages = est_words // 250
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.markdown("**Estimated Output**"); st.markdown(f"{est_pages}–{est_pages+2} pages")
        st.caption(f"~{est_words} words")
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown(hdr("zap", "Generate Review", "h2", 22), unsafe_allow_html=True)
    topic = st.text_input("Review Topic / Title",
                          placeholder="e.g., Machine Learning for Drug Discovery",
                          help="Used as the title and focus of the review")

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        if st.button("Generate Literature Review", type="primary", use_container_width=True):
            if not topic:
                st.error("Please enter a review topic")
            elif len(papers) < 3:
                st.error("Need at least 3 papers to generate a review")
            else:
                generate_review(topic, papers, detail_level, review_type, save_to_db)
    with c3:
        st.markdown(f'{ic("clock",14)} Est. time: 1–2 min', unsafe_allow_html=True)


def generate_review(topic, papers, detail_level, review_type, save_to_db):
    with st.spinner("Generating literature review… This may take 1–2 minutes…"):
        progress_bar = st.progress(0); status_text = st.empty()
        try:
            status_text.text("Detecting themes across papers…"); progress_bar.progress(20)
            status_text.text("Writing literature review sections…"); progress_bar.progress(40)
            review_result = lit_review_agent.generate_review(
                papers=papers, query=topic, detail_level=detail_level,
                review_type=review_type, project_id=st.session_state.get('review_project'),
                save_to_db=save_to_db)
            progress_bar.progress(80); status_text.text("Finalising review…")
            progress_bar.progress(100); status_text.text("Review generated successfully!")
            st.session_state.generated_review = review_result; st.rerun()
        except Exception as e:
            st.error(f"Generation failed: {str(e)}")
            logger.error(f"Literature review generation error: {str(e)}")


def show_review_results(review_result):
    st.markdown(hdr("check", "Literature Review Generated!", "h2", 22), unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Word Count",     f"{review_result['word_count']:,}")
    c2.metric("Estimated Pages", review_result['page_estimate'])
    c3.metric("Papers Included", review_result['papers_count'])
    c4.metric("Reading Time",   f"{review_result['word_count']//200} min")

    st.divider()
    st.markdown(hdr("download", "Export Review", "h2", 22), unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("Word",     use_container_width=True): export_review(review_result, "word")
    with c2:
        if st.button("PDF",      use_container_width=True): export_review(review_result, "pdf")
    with c3:
        if st.button("Markdown", use_container_width=True): export_review(review_result, "markdown")
    with c4:
        if st.button("LaTeX",    use_container_width=True): export_review(review_result, "latex")
    with c5:
        if st.button("New Review", use_container_width=True):
            st.session_state.generated_review = None; st.rerun()

    st.divider()
    st.markdown(hdr("eye", "Review Preview", "h2", 22), unsafe_allow_html=True)
    st.markdown('<div class="review-preview">', unsafe_allow_html=True)
    st.markdown(review_result['content'])
    st.markdown('</div>', unsafe_allow_html=True)


def export_review(review_result, format_type):
    try:
        if format_type == "markdown":
            st.download_button("Download Markdown", review_result['markdown_content'],
                file_name="literature_review.md", mime="text/markdown")
        elif format_type == "latex":
            st.download_button("Download LaTeX", review_result['latex_content'],
                file_name="literature_review.tex", mime="text/plain")
        elif format_type == "word":
            doc = lit_review_agent.export_review(review_result['content'], format="word")
            st.download_button("Download Word", doc, file_name="literature_review.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        elif format_type == "pdf":
            pdf = lit_review_agent.export_review(review_result['content'], format="pdf")
            st.download_button("Download PDF", pdf, file_name="literature_review.pdf", mime="application/pdf")
        st.success("Export ready!")
    except Exception as e:
        st.error(f"Export failed: {str(e)}"); logger.error(f"Review export error: {str(e)}")


if __name__ == "__main__":
    main()