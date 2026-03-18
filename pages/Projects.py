import streamlit as st
from datetime import datetime
from database.database import db
from agents.export_agent import export_agent
from utils.error_handler import logger

st.set_page_config(page_title="Projects", page_icon="", layout="wide")

# ── Lucide SVG icon helper ────────────────────────────────────────────────────
def svg(name, size=16, color="currentColor"):
    paths = {
        "folder":      '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
        "bar-chart":   '<line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/>',
        "zap":         '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
        "plus":        '<path d="M5 12h14"/><path d="M12 5v14"/>',
        "search":      '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>',
        "file-text":   '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
        "trash-2":     '<path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/>',
        "book-open":   '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
        "pen-line":    '<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
        "settings":    '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
        "alert-triangle": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
        "download":    '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>',
        "save":        '<path d="M15.2 3a2 2 0 0 1 1.4.6l3.8 3.8a2 2 0 0 1 .6 1.4V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M17 21v-7a1 1 0 0 0-1-1H8a1 1 0 0 0-1 1v7"/><path d="M7 3v4a1 1 0 0 0 1 1h7"/>',
        "calendar":    '<rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/>',
    }
    inner = paths.get(name, paths["folder"])
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
    .project-card{background-color:var(--background-color);padding:1.5rem;border-radius:10px;
        border-left:4px solid #28a745;margin-bottom:1rem;box-shadow:0 2px 4px rgba(0,0,0,.1);}
    .tag-badge{display:inline-block;padding:.25rem .75rem;border-radius:12px;
        background:#e3f2fd;color:#1976d2;font-size:.85rem;margin:.25rem;}
    .paper-mini-card{background-color:var(--secondary-background-color);padding:.75rem;
        border-radius:6px;margin:.5rem 0;border-left:3px solid #1f77b4;}
    </style>""", unsafe_allow_html=True)

if 'selected_project' not in st.session_state:  st.session_state.selected_project  = None
if 'show_create_form' not in st.session_state:  st.session_state.show_create_form  = False


def main():
    st.markdown(hdr("folder", "Research Projects", "h1", 28), unsafe_allow_html=True)
    st.markdown("Organise and manage your research papers")

    with st.sidebar:
        st.markdown(hdr("bar-chart", "Projects Overview", "h3", 18), unsafe_allow_html=True)
        try:
            stats = db.get_statistics()
            st.metric("Total Projects", stats.get('total_projects', 0))
            st.metric("Total Papers",   stats.get('total_papers',   0))
            st.metric("Papers with PDFs", stats.get('papers_with_pdf', 0))
        except:
            st.info("No statistics available")
        st.divider()

        st.markdown(hdr("zap", "Quick Actions", "h3", 16), unsafe_allow_html=True)
        if st.button("New Project",       use_container_width=True):
            st.session_state.show_create_form = True
            st.session_state.selected_project = None; st.rerun()
        if st.button("Search Papers",     use_container_width=True): st.switch_page("pages/Search.py")
        if st.button("Generate Review",   use_container_width=True): st.switch_page("pages/Literature_Review.py")

    if st.session_state.show_create_form:
        show_create_project_form()
    elif st.session_state.selected_project:
        show_project_details()
    else:
        show_projects_list()


def show_create_project_form():
    st.markdown(hdr("plus", "Create New Project", "h2", 22), unsafe_allow_html=True)
    with st.form("create_project_form"):
        name        = st.text_input("Project Name*", placeholder="e.g., PhD Literature Review")
        description = st.text_area("Description",    placeholder="Brief description of your research project…")
        tags_input  = st.text_input("Tags (comma-separated)", placeholder="machine learning, healthcare")
        tags = [t.strip() for t in tags_input.split(",") if t.strip()]
        c1, c2 = st.columns(2)
        with c1: submit = st.form_submit_button("Create Project", type="primary", use_container_width=True)
        with c2: cancel = st.form_submit_button("Cancel", use_container_width=True)
        if submit:
            if not name:
                st.error("Project name is required")
            else:
                try:
                    project = db.create_project(name=name, description=description, tags=tags)
                    if project:
                        st.success(f"Project '{name}' created!")
                        st.session_state.show_create_form = False
                        st.session_state.selected_project = project.id; st.rerun()
                    else: st.error("Failed to create project")
                except Exception as e: st.error(f"Error: {str(e)}")
        if cancel:
            st.session_state.show_create_form = False; st.rerun()


def show_projects_list():
    st.markdown(hdr("folder", "Your Projects", "h2", 22), unsafe_allow_html=True)
    try:
        projects = db.get_all_projects()
        if not projects:
            st.info("No projects yet. Create your first project to get started!")
            if st.button("Create First Project"):
                st.session_state.show_create_form = True; st.rerun()
            return

        c1, c2 = st.columns([3, 1])
        with c1:
            search_term = st.text_input("Search projects", placeholder="Search by name or tags…",
                                        label_visibility="collapsed")
        with c2:
            sort_by = st.selectbox("Sort by", ["Recent","Name","Papers Count"], label_visibility="collapsed")

        filtered = [p for p in projects if
            not search_term or search_term.lower() in p.name.lower()
            or any(search_term.lower() in t.lower() for t in (p.tags or []))]

        if sort_by == "Recent":
            filtered = sorted(filtered, key=lambda x: x.updated_at, reverse=True)
        elif sort_by == "Name":
            filtered = sorted(filtered, key=lambda x: x.name)
        elif sort_by == "Papers Count":
            filtered = sorted(filtered, key=lambda x: len(db.get_project_papers(x.id)), reverse=True)

        st.markdown(f"**{len(filtered)} project(s)**")
        for project in filtered:
            display_project_card(project)
    except Exception as e:
        st.error(f"Error loading projects: {str(e)}")
        logger.error(f"Projects list error: {str(e)}")


def display_project_card(project):
    papers     = db.get_project_papers(project.id)
    paper_count = len(papers)
    with st.container():
        st.markdown('<div class="project-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            st.markdown(f'### {ic("folder",18)}{project.name}', unsafe_allow_html=True)
            if project.description: st.markdown(project.description)
            if project.tags:
                st.markdown("".join(f'<span class="tag-badge">{t}</span>' for t in project.tags),
                            unsafe_allow_html=True)
        with c2:
            st.metric("Papers", paper_count)
            st.caption(f"Updated: {project.updated_at.strftime('%m/%d/%Y')}")
        with c3:
            if st.button("Open", key=f"open_{project.id}", use_container_width=True):
                st.session_state.selected_project = project.id; st.rerun()
            if st.button("Delete", key=f"del_{project.id}", use_container_width=True):
                if st.session_state.get(f'confirm_delete_{project.id}'):
                    db.delete_project(project.id); st.success("Deleted!"); st.rerun()
                else:
                    st.session_state[f'confirm_delete_{project.id}'] = True
                    st.warning("Click again to confirm")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("")


def show_project_details():
    project_id = st.session_state.selected_project
    try:
        project = db.get_project(project_id)
        if not project:
            st.error("Project not found"); st.session_state.selected_project = None; return

        c1, c2 = st.columns([5, 1])
        with c1: st.markdown(hdr("folder", project.name, "h1", 26), unsafe_allow_html=True)
        with c2:
            if st.button("Back", use_container_width=True):
                st.session_state.selected_project = None; st.rerun()

        if project.description: st.markdown(project.description)
        if project.tags:
            st.markdown("".join(f'<span class="tag-badge">{t}</span>' for t in project.tags),
                        unsafe_allow_html=True)
        st.markdown(f"*Created: {project.created_at.strftime('%B %d, %Y')} | "
                    f"Updated: {project.updated_at.strftime('%B %d, %Y')}*")
        st.divider()

        tabs = st.tabs(["Papers","Notes","Statistics","Settings"])
        with tabs[0]: show_project_papers(project)
        with tabs[1]: show_project_notes(project)
        with tabs[2]: show_project_statistics(project)
        with tabs[3]: show_project_settings(project)
    except Exception as e:
        st.error(f"Error loading project: {str(e)}")
        logger.error(f"Project details error: {str(e)}")


def show_project_papers(project):
    papers = db.get_project_papers(project.id)
    if not papers:
        st.info("No papers yet. Add papers from the Search page!")
        if st.button("Go to Search"): st.switch_page("pages/Search.py")
        return
    c1, c2, c3 = st.columns(3)
    with c1: export_format = st.selectbox("Export as", ["Word","PDF","CSV","BibTeX","Markdown"])
    with c3:
        if st.button("Export All Papers", use_container_width=True):
            export_project_papers(papers, export_format)
    st.markdown(f"**{len(papers)} paper(s) in this project**")
    for i, paper in enumerate(papers, 1):
        with st.container():
            st.markdown('<div class="paper-mini-card">', unsafe_allow_html=True)
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"**{i}. {paper.title}**")
                authors = ", ".join((paper.authors or [])[:3])
                if len(paper.authors or []) > 3: authors += " et al."
                st.caption(f"{authors} • {paper.year} • {paper.citation_count} citations")
            with c2:
                if st.button("Remove", key=f"remove_{paper.id}"):
                    db.remove_paper_from_project(project.id, paper.id); st.success("Removed!"); st.rerun()
            if paper.abstract_summary_medium or paper.abstract:
                with st.expander("View summary"):
                    st.write(paper.abstract_summary_medium or paper.abstract[:300])
            st.markdown('</div>', unsafe_allow_html=True)


def show_project_notes(project):
    st.markdown(hdr("pen-line", "Project Notes", "h3", 18), unsafe_allow_html=True)
    with st.expander("Add New Note"):
        with st.form("add_note_form"):
            note_title   = st.text_input("Note Title")
            note_content = st.text_area("Note Content", height=150)
            note_type    = st.selectbox("Note Type",
                ["general","literature_review","methodology","findings","ideas"])
            if st.form_submit_button("Save Note"):
                if note_content:
                    db.add_project_note(project.id, note_title, note_content, note_type)
                    st.success("Note added!"); st.rerun()
    notes = db.get_project_notes(project.id)
    if notes:
        for note in notes:
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"**{note.title or 'Untitled Note'}**")
                st.caption(f"{note.note_type} • {note.created_at.strftime('%m/%d/%Y')}")
            st.write(note.content); st.divider()
    else:
        st.info("No notes yet. Add your first note above!")


def show_project_statistics(project):
    papers = db.get_project_papers(project.id)
    if not papers:
        st.info("No statistics yet. Add papers to see analytics."); return
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Papers",    len(papers))
    c2.metric("With PDFs",       sum(1 for p in papers if p.has_pdf))
    c3.metric("Total Citations",  sum(p.citation_count or 0 for p in papers))
    years = [p.year for p in papers if p.year and isinstance(p.year, int)]
    c4.metric("Avg Year", sum(years)//len(years) if years else 0)
    st.divider()
    st.markdown(hdr("calendar", "Year Distribution", "h3", 16), unsafe_allow_html=True)
    if years:
        import plotly.express as px
        year_counts = {}
        for y in years: year_counts[y] = year_counts.get(y, 0) + 1
        fig = px.bar(x=list(year_counts.keys()), y=list(year_counts.values()),
                     labels={'x':'Year','y':'Number of Papers'}, title="Papers by Publication Year")
        st.plotly_chart(fig, use_container_width=True)
    st.markdown(hdr("bar-chart", "Top Venues", "h3", 16), unsafe_allow_html=True)
    venues = {}
    for p in papers:
        if p.venue: venues[p.venue] = venues.get(p.venue, 0) + 1
    if venues:
        for venue, count in sorted(venues.items(), key=lambda x: x[1], reverse=True)[:10]:
            st.write(f"• **{venue}**: {count} paper(s)")


def show_project_settings(project):
    st.markdown(hdr("settings", "Project Settings", "h3", 18), unsafe_allow_html=True)
    with st.form("edit_project_form"):
        new_name        = st.text_input("Project Name", value=project.name)
        new_description = st.text_area("Description",   value=project.description or "")
        tags_input      = st.text_input("Tags (comma-separated)",
                                        value=", ".join(project.tags) if project.tags else "")
        new_tags = [t.strip() for t in tags_input.split(",") if t.strip()]
        if st.form_submit_button("Save Changes", type="primary"):
            db.update_project(project.id, name=new_name, description=new_description, tags=new_tags)
            st.success("Project updated!"); st.rerun()
    st.divider()
    st.markdown(hdr("alert-triangle", "Danger Zone", "h3", 16, "#dc2626"), unsafe_allow_html=True)
    st.warning("These actions cannot be undone!")
    if st.button("Delete Project", type="secondary", use_container_width=True):
        if st.session_state.get('confirm_delete_project'):
            db.delete_project(project.id); st.success("Deleted!")
            st.session_state.selected_project = None; st.rerun()
        else:
            st.session_state.confirm_delete_project = True
            st.error("Click again to confirm deletion")


def export_project_papers(papers, format_type):
    papers_dict = [{'title': p.title, 'authors': p.authors or [], 'year': p.year,
        'venue': p.venue, 'citation_count': p.citation_count, 'abstract': p.abstract,
        'abstract_summary': p.abstract_summary_medium, 'url': p.url,
        'doi': p.doi, 'has_pdf': p.has_pdf} for p in papers]
    try:
        if format_type == "Word":
            st.download_button("Download", export_agent.export_to_word(papers_dict),
                file_name="project_papers.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        elif format_type == "PDF":
            st.download_button("Download", export_agent.export_to_pdf(papers_dict),
                file_name="project_papers.pdf", mime="application/pdf")
        elif format_type == "CSV":
            st.download_button("Download", export_agent.export_to_csv(papers_dict).getvalue(),
                file_name="project_papers.csv", mime="text/csv")
        elif format_type == "BibTeX":
            st.download_button("Download", export_agent.export_to_bibtex(papers_dict),
                file_name="project_papers.bib", mime="text/plain")
        elif format_type == "Markdown":
            st.download_button("Download", export_agent.export_to_markdown(papers_dict),
                file_name="project_papers.md", mime="text/markdown")
        st.success("Exported successfully!")
    except Exception as e:
        st.error(f"Export failed: {str(e)}")


if __name__ == "__main__":
    main()