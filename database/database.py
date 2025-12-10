
import os
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, or_, and_, pool
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import config
from database.models import Base, Project, Paper, ProjectPaper, SearchHistory, ProjectNote, LiteratureReview
from utils.error_handler import logger, handle_errors


class DatabaseManager:
    """Manages all database operations"""
    
    def __init__(self, database_url: str = None):
        """
        Initialize database connection
        
        Args:
            database_url: PostgreSQL connection string
                         Format: postgresql://user:password@host:port/dbname
        """
        if database_url is None:
            # Get from environment or use SQLite for local development
            database_url = os.getenv(
                'DATABASE_URL',
                'sqlite:///./research_agent.db'  # Local fallback
            )
        
        # Fix for Render's postgres:// URL (should be postgresql://)
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        # Create engine
        # Create engine
        if database_url.startswith('sqlite'):
            # SQLite specific settings
            self.engine = create_engine(
                database_url,
                connect_args={"check_same_thread": False},
                poolclass=pool.StaticPool
            )
            # PostgreSQL settings
            self.engine = create_engine(
                database_url,
                pool_pre_ping=True,  # Verify connections before using
                pool_size=10,
                max_overflow=20
            )
        
        # Create session factory
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False)
        
        logger.info(f"Database initialized: {database_url.split('@')[0]}...")  # Don't log password
    
    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)
        logger.info("Database tables created")
        
 
    
    @contextmanager
    def get_session(self) -> Session:
        """Context manager for database sessions"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            session.close()
    
    # ==================== PROJECT OPERATIONS ====================
    
    @handle_errors#(default_return=None)
    def create_project(self, name: str, description: str = "", tags: List[str] = None) -> Optional[Project]:
        """Create a new project"""
        with self.get_session() as session:
            project = Project(
                name=name,
                description=description,
                tags=tags or []
            )
            session.add(project)
            session.flush()
            session.refresh(project)
            logger.info(f"Created project: {name}")
            return project
    
    # @handle_errors#(default_return=[])
    # def get_all_projects(self) -> List[Project]:
    #     """Get all projects"""
    #     with self.get_session() as session:
    #         # projects = session.query(Project).order_by(Project.updated_at.desc()).all()
    #         return projects
        
    @handle_errors   
    def get_all_projects(self):
        with self.get_session() as session:
            projects = session.query(Project).order_by(Project.updated_at.desc()).all()
            # projects = session.query(Project).all()
            # Eagerly load the attributes we need
            result = [
                type('Project', (), {
                    'id': p.id,
                    'name': p.name,
                    'tags': getattr(p, 'tags', []), 
                    'description': getattr(p, 'description', ''),
                    'created_at': getattr(p, 'created_at', None),
                    'updated_at': getattr(p, 'updated_at', None)
                
                })()
                for p in projects
            ]
            return result  
    # @handle_errors#(default_return=[])
    # def get_all_projects(self) -> List[Project]:
    #     """Get all projects"""
    #     with self.get_session() as session:
    #         projects = session.query(Project).order_by(Project.updated_at.desc()).all()
    #         # Force SQLAlchemy to load all attributes before closing session
    #         for p in projects:
    #             # Access attributes to ensure they're loaded
    #             _ = (p.id, p.name, p.description, p.tags, 
    #                 p.created_at, p.updated_at)
    #         return projects
    
    
    
    @handle_errors#(default_return=None)
    def get_project(self, project_id: int) -> Optional[Project]:
        """Get a specific project"""
        with self.get_session() as session:
            project = session.query(Project).filter(Project.id == project_id).first()
            return project
    
    @handle_errors#(default_return=False)
    def update_project(self, project_id: int, **kwargs) -> bool:
        """Update project fields"""
        with self.get_session() as session:
            project = session.query(Project).filter(Project.id == project_id).first()
            if not project:
                return False
            
            for key, value in kwargs.items():
                if hasattr(project, key):
                    setattr(project, key, value)
            
            logger.info(f"Updated project {project_id}")
            return True
    
    @handle_errors#(default_return=False)
    def delete_project(self, project_id: int) -> bool:
        """Delete a project and all associated data"""
        with self.get_session() as session:
            project = session.query(Project).filter(Project.id == project_id).first()
            if not project:
                return False
            
            session.delete(project)
            logger.info(f"Deleted project {project_id}")
            return True
    
    # ==================== PAPER OPERATIONS ====================
    
    @handle_errors#(default_return=None)
    def create_or_update_paper(self, paper_data: Dict[str, Any]) -> Optional[Paper]:
        """Create a new paper or update if exists"""
        with self.get_session() as session:
            # Check if paper exists (by DOI, arXiv ID, or title)
            existing = None
            
            if paper_data.get('doi'):
                existing = session.query(Paper).filter(Paper.doi == paper_data['doi']).first()
            
            if not existing and paper_data.get('arxiv_id'):
                existing = session.query(Paper).filter(Paper.arxiv_id == paper_data['arxiv_id']).first()
            
            if not existing and paper_data.get('title'):
                existing = session.query(Paper).filter(Paper.title == paper_data['title']).first()
            
            if existing:
                # Update existing paper
                for key, value in paper_data.items():
                    if hasattr(existing, key) and value is not None:
                        setattr(existing, key, value)
                session.commit()
                session.refresh(existing)
                logger.info(f"Updated paper: {existing.title[:50]}")
                return existing
            else:
                # Create new paper - filter to only valid columns
                valid_fields = {
                    key: value 
                    for key, value in paper_data.items() 
                    if hasattr(Paper, key) and key != 'id'  # Exclude 'id' as it's auto-generated
                }
                
                paper = Paper(**valid_fields)
                session.add(paper)
                session.flush()
                session.refresh(paper)
                session.commit()
                logger.info(f"Created paper: {paper.title[:50]}")
                return paper      
                
            
    
    @handle_errors#(default_return=None)
    def get_paper(self, paper_id: int) -> Optional[Paper]:
        """Get a specific paper"""
        with self.get_session() as session:
            paper = session.query(Paper).filter(Paper.id == paper_id).first()
            return paper
    
    @handle_errors#(default_return=None)
    def find_paper_by_identifier(self, doi: str = None, arxiv_id: str = None, title: str = None) -> Optional[Paper]:
        """Find paper by DOI, arXiv ID, or title"""
        with self.get_session() as session:
            if doi:
                paper = session.query(Paper).filter(Paper.doi == doi).first()
                if paper:
                    return paper
            
            if arxiv_id:
                paper = session.query(Paper).filter(Paper.arxiv_id == arxiv_id).first()
                if paper:
                    return paper
            
            if title:
                paper = session.query(Paper).filter(Paper.title == title).first()
                if paper:
                    return paper
            
            return None
    
    # ==================== PROJECT-PAPER OPERATIONS ====================
    
    @handle_errors#(default_return=False)
    def add_paper_to_project(self, project_id: int, paper_id: int, notes: str = "", importance: int = 3) -> bool:
        """Add a paper to a project"""
        with self.get_session() as session:
            # Check if already exists
            existing = session.query(ProjectPaper).filter(
                and_(ProjectPaper.project_id == project_id, ProjectPaper.paper_id == paper_id)
            ).first()
            
            if existing:
                logger.info(f"Paper {paper_id} already in project {project_id}")
                return True
            
            project_paper = ProjectPaper(
                project_id=project_id,
                paper_id=paper_id,
                notes=notes,
                importance=importance
            )
            session.add(project_paper)
            logger.info(f"Added paper {paper_id} to project {project_id}")
            return True
    
    @handle_errors#(default_return=[])
    def get_project_papers(self, project_id: int) -> List[Paper]:
        """Get all papers in a project"""
        with self.get_session() as session:
            project_papers = session.query(ProjectPaper).filter(
                ProjectPaper.project_id == project_id
            ).all()
            
            papers = [pp.paper for pp in project_papers if pp.paper]
            return papers
    
    @handle_errors#(default_return=False)
    def remove_paper_from_project(self, project_id: int, paper_id: int) -> bool:
        """Remove a paper from a project"""
        with self.get_session() as session:
            project_paper = session.query(ProjectPaper).filter(
                and_(ProjectPaper.project_id == project_id, ProjectPaper.paper_id == paper_id)
            ).first()
            
            if project_paper:
                session.delete(project_paper)
                logger.info(f"Removed paper {paper_id} from project {project_id}")
                return True
            return False
    
    # ==================== SEARCH HISTORY OPERATIONS ====================
    
    @handle_errors#(default_return=None)
    def save_search(self, search_data: Dict[str, Any]) -> Optional[SearchHistory]:
        """Save a search to history"""
        with self.get_session() as session:
            search = SearchHistory(**search_data)
            session.add(search)
            session.flush()
            session.refresh(search)
            logger.info(f"Saved search: {search.query}")
            return search
    
    @handle_errors#(default_return=[])
    def get_recent_searches(self, limit: int = 10) -> List[SearchHistory]:
        """Get recent search history"""
        with self.get_session() as session:
            searches = session.query(SearchHistory).order_by(
                SearchHistory.created_at.desc()
            ).limit(limit).all()
            return searches
    
    # ==================== NOTES OPERATIONS ====================
    
    @handle_errors#(default_return=None)
    def add_project_note(self, project_id: int, title: str, content: str, note_type: str = "general") -> Optional[ProjectNote]:
        """Add a note to a project"""
        with self.get_session() as session:
            note = ProjectNote(
                project_id=project_id,
                title=title,
                content=content,
                note_type=note_type
            )
            session.add(note)
            session.flush()
            session.refresh(note)
            logger.info(f"Added note to project {project_id}")
            return note
    
    @handle_errors#(default_return=[])
    def get_project_notes(self, project_id: int) -> List[ProjectNote]:
        """Get all notes for a project"""
        with self.get_session() as session:
            notes = session.query(ProjectNote).filter(
                ProjectNote.project_id == project_id
            ).order_by(ProjectNote.created_at.desc()).all()
            return notes
    
    # ==================== STATISTICS ====================
    
    @handle_errors#(default_return={})
    def get_statistics(self) -> Dict[str, int]:
        """Get database statistics"""
        with self.get_session() as session:
            stats = {
                'total_projects': session.query(Project).count(),
                'total_papers': session.query(Paper).count(),
                'total_searches': session.query(SearchHistory).count(),
                'papers_with_pdf': session.query(Paper).filter(Paper.has_pdf == True).count()
            }
            return stats


# Global database instance
db = DatabaseManager()