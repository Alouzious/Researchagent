
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Project(Base):
    """Research project containing multiple papers and searches"""
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    tags = Column(JSON)  # List of tags
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    papers = relationship("ProjectPaper", back_populates="project", cascade="all, delete-orphan")
    searches = relationship("SearchHistory", back_populates="project", cascade="all, delete-orphan")
    notes = relationship("ProjectNote", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"


class Paper(Base):
    """Academic paper with metadata and analysis"""
    __tablename__ = 'papers'
    
    id = Column(Integer, primary_key=True)
    
    # Identifiers
    title = Column(String(500), nullable=False)
    doi = Column(String(255), unique=True, index=True)
    arxiv_id = Column(String(50), index=True)
    semantic_scholar_id = Column(String(100), index=True)
    url = Column(String(500))
    
    # Metadata
    abstract = Column(Text)
    authors = Column(JSON)  # List of author names
    year = Column(Integer, index=True)
    venue = Column(String(255))
    publication_date = Column(String(50))
    citation_count = Column(Integer, default=0)
    
    # PDF info
    has_pdf = Column(Boolean, default=False)
    pdf_url = Column(String(500))
    pdf_text = Column(Text)  # Full extracted text
    
    # AI Analysis
    abstract_summary_short = Column(Text)
    abstract_summary_medium = Column(Text)
    abstract_summary_long = Column(Text)
    pdf_summary_short = Column(Text)
    pdf_summary_medium = Column(Text)
    pdf_summary_long = Column(Text)
    
    key_findings = Column(Text)
    methodology_gaps = Column(Text)
    knowledge_gaps = Column(Text)
    future_directions = Column(Text)
    
    # Source database
    source = Column(String(50))  # 'semantic_scholar', 'arxiv', 'pubmed'
    
    # Processing status
    processing_status = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project_papers = relationship("ProjectPaper", back_populates="paper")
    
    def __repr__(self):
        return f"<Paper(id={self.id}, title='{self.title[:50]}...')>"


class ProjectPaper(Base):
    """Association between projects and papers"""
    __tablename__ = 'project_papers'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    paper_id = Column(Integer, ForeignKey('papers.id'), nullable=False)
    
    # Paper-specific notes in this project
    notes = Column(Text)
    tags = Column(JSON)  # Project-specific tags for this paper
    importance = Column(Integer, default=3)  # 1-5 scale
    
    added_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="papers")
    paper = relationship("Paper", back_populates="project_papers")
    
    def __repr__(self):
        return f"<ProjectPaper(project_id={self.project_id}, paper_id={self.paper_id})>"


class SearchHistory(Base):
    """History of searches performed"""
    __tablename__ = 'search_history'
    
    id = Column(Integer, primary_key=True)
    query = Column(String(500), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    
    # Search parameters
    limit = Column(Integer)
    summary_level = Column(String(20))
    year_from = Column(Integer)
    year_to = Column(Integer)
    open_access_only = Column(Boolean)
    databases = Column(JSON)  # List of databases searched
    
    # Results
    results_count = Column(Integer)
    papers_found = Column(JSON)  # List of paper IDs
    
    # Timing
    search_duration_seconds = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    project = relationship("Project", back_populates="searches")
    
    def __repr__(self):
        return f"<SearchHistory(query='{self.query}', results={self.results_count})>"


class ProjectNote(Base):
    """General notes for a project"""
    __tablename__ = 'project_notes'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    
    title = Column(String(255))
    content = Column(Text, nullable=False)
    note_type = Column(String(50))  # 'general', 'literature_review', 'methodology', etc.
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    project = relationship("Project", back_populates="notes")
    
    def __repr__(self):
        return f"<ProjectNote(id={self.id}, title='{self.title}')>"


class LiteratureReview(Base):
    """Generated literature reviews"""
    __tablename__ = 'literature_reviews'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    
    title = Column(String(500))
    content = Column(Text, nullable=False)  # Full generated review
    papers_included = Column(JSON)  # List of paper IDs used
    
    # Generation parameters
    review_type = Column(String(50))  # 'thematic', 'chronological', 'methodological'
    detail_level = Column(String(20))  # 'short', 'medium', 'long'
    
    # Export formats (cached)
    markdown_content = Column(Text)
    latex_content = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<LiteratureReview(id={self.id}, title='{self.title}')>"


# ============================================
# MONETIZATION MODELS 
# ============================================

# class User(Base):
#     """User accounts for monetization"""
#     __tablename__ = 'users'
#     
#     id = Column(Integer, primary_key=True)
#     email = Column(String(255), unique=True, nullable=False, index=True)
#     hashed_password = Column(String(255), nullable=False)
#     
#     # Profile
#     full_name = Column(String(255))
#     institution = Column(String(255))
#     
#     # Subscription
#     tier = Column(String(20), default='free')  # 'free', 'pro', 'team'
#     stripe_customer_id = Column(String(100))
#     subscription_status = Column(String(20))  # 'active', 'cancelled', 'past_due'
#     subscription_end_date = Column(DateTime)
#     
#     # Usage tracking
#     searches_this_month = Column(Integer, default=0)
#     exports_this_month = Column(Integer, default=0)
#     lit_reviews_this_month = Column(Integer, default=0)
#     
#     created_at = Column(DateTime, default=datetime.utcnow)
#     last_login = Column(DateTime)
#     
#     def __repr__(self):
#         return f"<User(email='{self.email}', tier='{self.tier}')>"


# class UsageLog(Base):
#     """Track usage for billing and analytics"""
#     __tablename__ = 'usage_logs'
#     
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     
#     action = Column(String(50))  # 'search', 'export', 'lit_review'
#     details = Column(JSON)
#     
#     created_at = Column(DateTime, default=datetime.utcnow)