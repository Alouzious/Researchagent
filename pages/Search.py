import streamlit as st
from datetime import datetime
import config
from database import database
from research_agent import research_agent
from agents.cache_manager import cache
from agents.export_agent import export_agent
from database.database import db
from utils.error_handler import logger
import io

st.set_page_config(page_title="Search Papers", page_icon="", layout="wide")

# ── Lucide SVG icon helper ────────────────────────────────────────────────────
def svg(name, size=16, color="currentColor"):
    paths = {
        "search":     '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>',
        "settings":   '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
        "sliders":    '<line x1="4" x2="4" y1="21" y2="14"/><line x1="4" x2="4" y1="6" y2="3"/><line x1="12" x2="12" y1="21" y2="12"/><line x1="12" x2="12" y1="4" y2="3"/><line x1="20" x2="20" y1="21" y2="16"/><line x1="20" x2="20" y1="8" y2="3"/><line x1="1" x2="7" y1="14" y2="14"/><line x1="9" x2="15" y1="12" y2="12"/><line x1="17" x2="23" y1="16" y2="16"/>',
        "filter":     '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>',
        "save":       '<path d="M15.2 3a2 2 0 0 1 1.4.6l3.8 3.8a2 2 0 0 1 .6 1.4V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M17 21v-7a1 1 0 0 0-1-1H8a1 1 0 0 0-1 1v7"/><path d="M7 3v4a1 1 0 0 0 1 1h7"/>',
        "package":    '<path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
        "book-open":  '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
        "lightbulb":  '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
        "download":   '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>',
        "file-text":  '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
        "link":       '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    }
    inner = paths.get(name, paths["search"])
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
    .paper-card{background-color:var(--background-color);padding:1.5rem;border-radius:10px;
        border-left:4px solid #1f77b4;margin-bottom:1.5rem;box-shadow:0 2px 4px rgba(0,0,0,.1);}
    .source-badge{display:inline-block;padding:.2rem .5rem;border-radius:8px;font-size:.75rem;margin-right:.5rem;}
    .source-semantic{background:#e3f2fd;color:#1976d2;}
    .source-arxiv{background:#f3e5f5;color:#7b1fa2;}
    </style>""", unsafe_allow_html=True)

if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'current_project' not in st.session_state:
    st.session_state.current_project = None


def main():
    st.markdown(hdr("search", "Search Academic Papers", "h1", 28), unsafe_allow_html=True)
    st.markdown("Search across multiple databases with AI-powered analysis")

    with st.sidebar:
        st.markdown(hdr("settings", "Search Configuration", "h3", 18), unsafe_allow_html=True)
        st.subheader("Databases")
        use_semantic_scholar = st.checkbox("Semantic Scholar", value=True)
        use_arxiv = st.checkbox("ArXiv", value=True)
        databases = []
        if use_semantic_scholar: databases.append('semantic_scholar')
        if use_arxiv:            databases.append('arxiv')

        st.divider()
        st.markdown(hdr("sliders", "Settings", "h3", 16), unsafe_allow_html=True)
        limit = st.slider("Number of papers", 1, config.MAX_PAPER_LIMIT, 10)
        summary_level = st.selectbox(
            "Summary Detail", options=list(config.SUMMARY_LEVELS.keys()), index=1,
            format_func=lambda x: f"{x.title()} - {config.SUMMARY_LEVELS[x]['description']}")
        process_pdfs = st.checkbox("Process PDFs", value=True)

        st.divider()
        st.markdown(hdr("filter", "Filters", "h3", 16), unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: year_from = st.number_input("Year from", min_value=1900, max_value=2025, value=None)
        with c2: year_to   = st.number_input("Year to",   min_value=1900, max_value=2025, value=None)
        open_access_only = st.checkbox("Open Access Only", value=False)

        st.divider()
        st.markdown(hdr("save", "Save Results", "h3", 16), unsafe_allow_html=True)
        projects = db.get_all_projects()
        project_options = ["Don't save"] + [f"{p.name} (ID: {p.id})" for p in projects]
        selected_project = st.selectbox("Save to project", project_options)
        if selected_project != "Don't save":
            st.session_state.current_project = int(selected_project.split("ID: ")[1].rstrip(")"))

        st.divider()
        st.markdown(hdr("package", "Cache", "h3", 16), unsafe_allow_html=True)
        cache_stats = cache.get_cache_stats()
        st.metric("Cached Items", cache_stats['topic_cache_files'] + cache_stats['paper_cache_files'])
        if st.button("Clear Cache", use_container_width=True):
            cache.clear_all_cache(); st.success("Cache cleared!")

    st.divider()
    c1, c2 = st.columns([5, 1])
    with c1:
        query = st.text_input("Search", placeholder="e.g., 'machine learning for drug discovery'",
                              label_visibility="collapsed")
    with c2:
        search_button = st.button("Search", type="primary", use_container_width=True)

    with st.expander("Example Queries"):
        st.markdown(f'{ic("lightbulb",15,"#f59e0b")} <b>Click any example to search</b>', unsafe_allow_html=True)
        examples = ["transformer models in NLP","CRISPR gene editing","quantum computing algorithms",
                    "climate change machine learning","deep learning protein structure"]
        cols = st.columns(3)
        for i, ex in enumerate(examples):
            with cols[i % 3]:
                if st.button(ex, key=f"ex_{i}"):
                    st.session_state.search_query = ex; st.rerun()

    if search_button or st.session_state.get('search_query'):
        if st.session_state.get('search_query'):
            query = st.session_state.search_query; st.session_state.search_query = None
        if not query: st.warning("Please enter a search topic"); return
        if not databases: st.warning("Please select at least one database"); return

        with st.spinner(f"Searching for papers on '{query}'..."):
            try:
                start = datetime.now()
                papers = research_agent.search_and_analyze(
                    query=query, limit=limit, summary_level=summary_level,
                    process_pdfs=process_pdfs, year_from=year_from,
                    year_to=year_to, open_access_only=open_access_only)
                duration = (datetime.now() - start).total_seconds()
                if papers:
                    st.session_state.search_results = papers
                    db.save_search({'query': query, 'limit': limit, 'summary_level': summary_level,
                        'year_from': year_from, 'year_to': year_to, 'open_access_only': open_access_only,
                        'databases': databases, 'results_count': len(papers),
                        'papers_found': [p.get('paper_id') for p in papers],
                        'search_duration_seconds': duration})
                    if st.session_state.current_project:
                        for paper in papers:
                            db_paper = db.create_or_update_paper(paper)
                            if db_paper:
                                db.add_paper_to_project(st.session_state.current_project, db_paper.id)
                    st.success(f"Found {len(papers)} papers in {duration:.1f}s")
                else:
                    st.error("No papers found. Try different keywords."); return
            except Exception as e:
                st.error(f"Search failed: {str(e)}"); logger.error(f"Search error: {str(e)}"); return

    if st.session_state.search_results:
        papers = st.session_state.search_results
        st.divider()
        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        with c1:
            st.markdown(hdr("book-open", f"Results ({len(papers)} papers)", "h2", 22), unsafe_allow_html=True)
        with c2:
            sort_by = st.selectbox("Sort", ["Relevance","Year (Newest)","Year (Oldest)","Citations"],
                                   label_visibility="collapsed")
        with c3:
            export_format = st.selectbox("Format", ["Word","PDF","CSV","BibTeX","Markdown","LaTeX","JSON"],
                                         label_visibility="collapsed")
        with c4:
            if st.button("Export All", use_container_width=True): export_results(papers, export_format)

        if sort_by == "Year (Newest)":
            papers = sorted(papers, key=lambda x: x.get('year',0) if isinstance(x.get('year'),int) else 0, reverse=True)
        elif sort_by == "Year (Oldest)":
            papers = sorted(papers, key=lambda x: x.get('year',0) if isinstance(x.get('year'),int) else 0)
        elif sort_by == "Citations":
            papers = sorted(papers, key=lambda x: x.get('citation_count',0), reverse=True)

        for i, paper in enumerate(papers, 1):
            display_paper(paper, i)


def display_paper(paper, index):
    with st.container():
        c1, c2 = st.columns([5, 1])
        with c1:
            source = paper.get('source','unknown')
            st.markdown(f'<span class="source-badge source-{source}">{source.upper()}</span>', unsafe_allow_html=True)
            st.markdown(f"### {index}. {paper.get('title','Untitled')}")
            authors = ", ".join(paper.get('authors',[])[:3])
            if len(paper.get('authors',[])) > 3: authors += " et al."
            st.markdown(
                f'{ic("file-text",14)} **{authors}** &bull; {paper.get("year","?")} &bull; '
                f'{paper.get("venue","?")} &bull; {paper.get("citation_count",0)} citations',
                unsafe_allow_html=True)
        with c2:
            url = paper.get('url','#')
            st.markdown(f'<a href="{url}" target="_blank">{ic("link",14)}View</a>', unsafe_allow_html=True)

        tabs = st.tabs(["Summary", "Analysis", "Export", "Actions"])

        with tabs[0]:
            if paper.get('abstract_summary'):
                st.write("**AI Summary:**"); st.write(paper['abstract_summary'])
            if paper.get('abstract'):
                with st.expander("View full abstract"): st.write(paper['abstract'])

        with tabs[1]:
            if paper.get('key_findings'):
                st.write("**Key Findings:**"); st.write(paper['key_findings'])
            if paper.get('research_gaps'):
                gaps = paper['research_gaps']
                c1, c2 = st.columns(2)
                with c1: st.write("**Methodology Gaps:**");  st.write(gaps.get('methodology_gaps','N/A'))
                with c2: st.write("**Knowledge Gaps:**");    st.write(gaps.get('knowledge_gaps','N/A'))
                st.write("**Future Directions:**"); st.write(gaps.get('future_directions','N/A'))

        with tabs[2]:
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("Word",   key=f"word_{index}", use_container_width=True): export_single_paper(paper,"Word")
            with c2:
                if st.button("PDF",    key=f"pdf_{index}",  use_container_width=True): export_single_paper(paper,"PDF")
            with c3:
                if st.button("BibTeX", key=f"bib_{index}",  use_container_width=True): export_single_paper(paper,"BibTeX")

        with tabs[3]:
            c1, c2 = st.columns(2)
            with c1:
                projects = db.get_all_projects()
                if projects:
                    proj = st.selectbox("Add to project",
                        ["Select project..."] + [p.name for p in projects], key=f"project_{index}")
                    if proj != "Select project..." and st.button("Add", key=f"add_{index}"):
                        sel = next(p for p in projects if p.name == proj)
                        db_paper = db.create_or_update_paper(paper)
                        if db_paper:
                            db.add_paper_to_project(sel.id, db_paper.id); st.success(f"Added to {proj}!")
            with c2:
                citation = research_agent.generate_citation(paper, "APA")
                st.text_area("Citation (APA)", citation, height=100, key=f"cite_{index}")
        st.divider()


def export_single_paper(paper, fmt):
    try:
        title = paper.get('title','paper')[:50]
        if fmt == "Word":
            doc = export_agent.export_to_word([paper])
            st.download_button("Download Word", doc, file_name=f"{title}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        elif fmt == "PDF":
            pdf = export_agent.export_to_pdf([paper])
            st.download_button("Download PDF", pdf, file_name=f"{title}.pdf", mime="application/pdf")
        elif fmt == "BibTeX":
            bib = export_agent.export_to_bibtex([paper])
            st.download_button("Download BibTeX", bib, file_name=f"{title}.bib", mime="text/plain")
    except Exception as e:
        st.error(f"Export failed: {str(e)}")


def export_results(papers, fmt):
    try:
        if fmt == "Word":
            st.download_button("Download (Word)", export_agent.export_to_word(papers),
                file_name="search_results.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        elif fmt == "PDF":
            st.download_button("Download (PDF)", export_agent.export_to_pdf(papers),
                file_name="search_results.pdf", mime="application/pdf")
        elif fmt == "CSV":
            st.download_button("Download (CSV)", export_agent.export_to_csv(papers).getvalue(),
                file_name="search_results.csv", mime="text/csv")
        elif fmt == "BibTeX":
            st.download_button("Download (BibTeX)", export_agent.export_to_bibtex(papers),
                file_name="search_results.bib", mime="text/plain")
        elif fmt == "Markdown":
            st.download_button("Download (Markdown)", export_agent.export_to_markdown(papers),
                file_name="search_results.md", mime="text/markdown")
        elif fmt == "LaTeX":
            st.download_button("Download (LaTeX)", export_agent.export_to_latex(papers),
                file_name="search_results.tex", mime="text/plain")
        elif fmt == "JSON":
            st.download_button("Download (JSON)", export_agent.export_to_json(papers),
                file_name="search_results.json", mime="application/json")
        st.success(f"Exported {len(papers)} papers!")
    except Exception as e:
        st.error(f"Export failed: {str(e)}")


if __name__ == "__main__":
    main()