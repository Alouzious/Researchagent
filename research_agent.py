from typing import List, Dict, Optional
import config
from utils.error_handler import logger, ErrorContext
from agents.search_agent import search_agent
from agents.pdf_agent import pdf_agent
from agents.llm_agent import llm_agent
from agents.cache_manager import cache


class ResearchAgent:
    """Main orchestrator for research operations"""
    
    def __init__(self):
        self.search_agent = search_agent 
        self.pdf_agent = pdf_agent
        self.llm_agent = llm_agent
        logger.info("Research Agent initialized")
    
    def search_and_analyze(
        self,
        query: str,
        limit: int = config.DEFAULT_PAPER_LIMIT,
        summary_level: str = config.DEFAULT_SUMMARY_LEVEL,
        process_pdfs: bool = True,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        open_access_only: bool = False
    ) -> List[Dict]:
        """
        Complete research workflow: search, download, analyze
        
        Args:
            query: Search query
            limit: Number of papers to retrieve
            summary_level: 'short', 'medium', or 'long'
            process_pdfs: Whether to download and process PDFs
            year_from: Filter papers from this year
            year_to: Filter papers until this year
            open_access_only: Only return open access papers
            
        Returns:
            List of analyzed paper dictionaries
        """
        with ErrorContext(f"Research workflow for: '{query}'"):
            # Step 1: Search for papers
            logger.info(f"Searching for papers: {query}")
            papers = self.search_agent.search_papers(
                query=query,
                limit=limit,
                year_from=year_from,
                year_to=year_to,
                open_access_only=open_access_only
            )
            
            if not papers:
                logger.warning("No papers found")
                return []
            
            # Step 2: Process each paper
            results = []
            for i, paper in enumerate(papers, 1):
                logger.info(f"Processing paper {i}/{len(papers)}: {paper['title'][:50]}...")
                
                processed_paper = self._process_single_paper(
                    paper=paper,
                    summary_level=summary_level,
                    process_pdf=process_pdfs
                )
                
                results.append(processed_paper)
            
            logger.info(f"Completed processing {len(results)} papers")
            return results
    
    def _process_single_paper(
        self,
        paper: Dict,
        summary_level: str,
        process_pdf: bool
    ) -> Dict:
        """
        Process a single paper: summarize, extract gaps, etc.
        
        Args:
            paper: Paper data from search
            summary_level: Summary detail level
            process_pdf: Whether to process PDF
            
        Returns:
            Enhanced paper dictionary
        """
        paper_id = paper["paper_id"]
        
        # Start with basic paper info
        result = {
            **paper,
            "processing_status": {
                "abstract_summary": "pending",
                "pdf_processed": "pending",
                "research_gaps": "pending",
                "key_findings": "pending"
            }
        }
        
        # Generate abstract summary
        try:
            abstract_summary = self.llm_agent.summarize_text(
                text=paper["abstract"],
                detail_level=summary_level,
                paper_id=paper_id
            )
            result["abstract_summary"] = abstract_summary
            result["processing_status"]["abstract_summary"] = "success"
        except Exception as e:
            logger.warning(f"Failed to summarize abstract: {str(e)}")
            result["abstract_summary"] = "Summary unavailable"
            result["processing_status"]["abstract_summary"] = "failed"
        
        # Process PDF if available
        if process_pdf and paper["has_pdf"]:
            try:
                pdf_text = self.pdf_agent.process_pdf(
                    pdf_url=paper["pdf_url"],
                    paper_id=paper_id
                )
                
                if pdf_text:
                    result["pdf_text"] = pdf_text
                    result["pdf_text_length"] = len(pdf_text)
                    result["processing_status"]["pdf_processed"] = "success"
                    
                    # Generate PDF-based summary
                    try:
                        pdf_summary = self.llm_agent.summarize_text(
                            text=pdf_text,
                            detail_level=summary_level,
                            paper_id=f"{paper_id}_pdf"
                        )
                        result["pdf_summary"] = pdf_summary
                    except Exception as e:
                        logger.warning(f"Failed to summarize PDF: {str(e)}")
                        result["pdf_summary"] = "PDF summary unavailable"
                    
                    # Extract research gaps
                    try:
                        research_gaps = self.llm_agent.identify_research_gaps(
                            text=pdf_text,
                            paper_id=paper_id
                        )
                        result["research_gaps"] = research_gaps
                        result["processing_status"]["research_gaps"] = "success"
                    except Exception as e:
                        logger.warning(f"Failed to identify research gaps: {str(e)}")
                        result["research_gaps"] = {
                            "methodology_gaps": "Analysis unavailable",
                            "knowledge_gaps": "Analysis unavailable",
                            "future_directions": "Analysis unavailable"
                        }
                        result["processing_status"]["research_gaps"] = "failed"
                    
                    # Extract key findings
                    try:
                        key_findings = self.llm_agent.extract_key_findings(
                            text=pdf_text,
                            paper_id=paper_id
                        )
                        result["key_findings"] = key_findings
                        result["processing_status"]["key_findings"] = "success"
                    except Exception as e:
                        logger.warning(f"Failed to extract key findings: {str(e)}")
                        result["key_findings"] = "Analysis unavailable"
                        result["processing_status"]["key_findings"] = "failed"
                else:
                    result["processing_status"]["pdf_processed"] = "failed"
                    result["pdf_error"] = "Could not extract text from PDF"
                    
            except Exception as e:
                logger.warning(f"PDF processing failed: {str(e)}")
                result["processing_status"]["pdf_processed"] = "failed"
                result["pdf_error"] = str(e)
        else:
            result["processing_status"]["pdf_processed"] = "skipped"
            if not paper["has_pdf"]:
                result["pdf_error"] = "No PDF available"
        
        return result
    
    def generate_citation(
        self,
        paper: Dict,
        style: str = "APA"
    ) -> str:
        """
        Generate citation in specified format
        
        Args:
            paper: Paper data
            style: Citation style (APA, MLA, IEEE)
            
        Returns:
            Formatted citation
        """
        authors = paper.get("authors", [])
        
        if style.upper() == "APA":
            # APA format
            if len(authors) == 0:
                author_str = "Unknown"
            elif len(authors) == 1:
                author_str = authors[0]
            elif len(authors) <= 3:
                author_str = ", ".join(authors[:-1]) + " & " + authors[-1]
            else:
                author_str = authors[0] + " et al."
            
            year = paper.get("year", "n.d.")
            title = paper.get("title", "Untitled")
            venue = paper.get("venue", "")
            url = paper.get("url", "")
            
            citation = f"{author_str} ({year}). {title}."
            if venue:
                citation += f" {venue}."
            if url:
                citation += f" Retrieved from {url}"
            
            return citation
        
        # Add other citation styles as needed
        return f"Citation style '{style}' not yet implemented"


# Global research agent instance
research_agent = ResearchAgent()
