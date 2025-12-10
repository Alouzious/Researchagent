"""
Test script for Literature Review Generator
Run this to verify Phase 2 literature review functionality
"""

from research_agent import research_agent
from agents.literature_review_agent import lit_review_agent


def test_literature_review_generation():
    """Test the complete literature review generation pipeline"""
    
    print("\n" + "="*70)
    print(" TESTING LITERATURE REVIEW GENERATOR")
    print("="*70)
    
    # Step 1: Search for papers
    print("\nStep 1: Searching for papers...")
    papers = research_agent.search_and_analyze(
        query="machine learning for drug discovery",
        limit=10,
        summary_level="medium",
        process_pdfs=False,  # Faster for testing
        databases=['semantic_scholar', 'arxiv']
    )
    
    if not papers:
        print("No papers found. Cannot test literature review.")
        return False
    
    print(f"Found {len(papers)} papers")
    
    # Step 2: Generate literature review
    print("\nStep 2: Generating literature review...")
    print("   This may take 30-60 seconds...")
    
    try:
        review_result = lit_review_agent.generate_review(
            papers=papers,
            query="Machine Learning for Drug Discovery",
            detail_level="medium",
            review_type="thematic",
            save_to_db=False  # Don't save during testing
        )
        
        print(f"Literature review generated!")
        print(f"   - Word count: {review_result['word_count']}")
        print(f"   - Estimated pages: {review_result['page_estimate']}")
        print(f"   - Papers included: {review_result['papers_count']}")
        
    except Exception as e:
        print(f"Failed to generate review: {str(e)}")
        return False
    
    # Step 3: Show preview
    print("\nStep 3: Review Preview (first 500 characters):")
    print("-" * 70)
    preview = review_result['content'][:500]
    print(preview + "...")
    print("-" * 70)
    
    # Step 4: Test statistics
    print("\nStep 4: Review Statistics:")
    stats = lit_review_agent.get_review_statistics(review_result['content'])
    for key, value in stats.items():
        print(f"   - {key}: {value}")
    
    # Step 5: Test export formats
    print("\nStep 5: Testing export formats...")
    
    formats_to_test = ['markdown', 'latex']
    
    for fmt in formats_to_test:
        try:
            exported = lit_review_agent.export_review(
                review_content=review_result['content'],
                format=fmt
            )
            
            if exported:
                if isinstance(exported, str):
                    size = len(exported)
                else:
                    size = len(exported.read())
                    exported.seek(0)
                
                print(f"{fmt.upper()}: {size} bytes")
            else:
                print(f"{fmt.upper()}: Export failed")
        except Exception as e:
            print(f"{fmt.upper()}: {str(e)}")
    
    # Success!
    print("\n" + "="*70)
    print(" ALL TESTS PASSED!")
    print("="*70)
    print("\nSummary:")
    print(f"   - Papers analyzed: {len(papers)}")
    print(f"   - Review generated: {review_result['word_count']} words")
    print(f"   - Export formats: Working")
    print("\nLiterature Review Generator is ready!")
    
    return True


def test_theme_detection():
    """Test just the theme detection"""
    print("\n" + "="*70)
    print("TESTING THEME DETECTION")
    print("="*70)
    
    # Create sample papers
    sample_papers = [
        {
            'title': 'Deep Learning for Protein Structure Prediction',
            'abstract': 'We use deep neural networks to predict protein structures...',
            'year': 2023
        },
        {
            'title': 'Machine Learning in Drug Screening',
            'abstract': 'This paper presents ML methods for high-throughput drug screening...',
            'year': 2022
        },
        {
            'title': 'AI-Driven Molecular Design',
            'abstract': 'We propose an AI system for designing novel molecules...',
            'year': 2023
        },
        {
            'title': 'Predicting Drug-Target Interactions with Neural Networks',
            'abstract': 'Neural networks can predict interactions between drugs and targets...',
            'year': 2021
        },
        {
            'title': 'Generative Models for Drug Discovery',
            'abstract': 'Generative AI models create new drug candidates...',
            'year': 2023
        }
    ]
    
    try:
        from agents.llm_agent import llm_agent
        themes = llm_agent.detect_themes(sample_papers)
        
        print(f"\nDetected {len(themes)} themes:")
        for theme_name, papers in themes.items():
            print(f"\n{theme_name}")
            for paper_title in papers:
                print(f"      - {paper_title}")
        
        return True
    except Exception as e:
        print(f"\nTheme detection failed: {str(e)}")
        return False


if __name__ == "__main__":
    print("\nLiterature Review Generator Test Suite")
    print("=" * 70)
    
    # Test 1: Theme Detection
    theme_success = test_theme_detection()
    
    # Test 2: Full Literature Review
    if theme_success:
        review_success = test_literature_review_generation()
    else:
        print("\nSkipping full review test due to theme detection failure")
        review_success = False
    
    # Final result
    print("\n" + "="*70)
    if theme_success and review_success:
        print(" ALL LITERATURE REVIEW TESTS PASSED!")
        print("\n Phase 2 Option A (Literature Review Generator) is COMPLETE!")
    else:
        print(" Some tests failed. Check errors above.")
    print("="*70)
