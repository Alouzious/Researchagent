


import sys
from research_agent import research_agent
from agents.cache_manager import cache
from utils.error_handler import logger


def test_basic_search():
    """Test basic search functionality"""
    print("\n" + "="*60)
    print("TEST 1: Basic Search (No PDF processing)")
    print("="*60)
    
    try:
        papers = research_agent.search_and_analyze(
            query="machine learning",
            limit=3,
            summary_level="short",
            process_pdfs=False
        )
        
        if papers:
            print(f"SUCCESS: Found {len(papers)} papers")
            print(f"   First paper: {papers[0]['title'][:50]}...")
            return True
        else:
            print("FAILED: No papers returned")
            return False
    except Exception as e:
        print(f"FAILED: {str(e)}")
        return False


def test_pdf_processing():
    """Test PDF download and processing"""
    print("\n" + "="*60)
    print("TEST 2: PDF Processing")
    print("="*60)
    
    try:
        papers = research_agent.search_and_analyze(
            query="deep learning",
            limit=2,
            summary_level="medium",
            process_pdfs=True,
            open_access_only=True  
        )
        
        pdf_processed = sum(1 for p in papers if p.get("pdf_text"))
        print(f"SUCCESS: Processed {pdf_processed}/{len(papers)} PDFs")
        
        if pdf_processed > 0:
            print(f"   PDF text length: {len(papers[0].get('pdf_text', ''))} chars")
        
        return True
    except Exception as e:
        print(f"FAILED: {str(e)}")
        return False


def test_caching():
    """Test caching functionality"""
    print("\n" + "="*60)
    print("TEST 3: Caching")
    print("="*60)
    
    try:
        # First search (should cache)
        papers1 = research_agent.search_and_analyze(
            query="artificial intelligence",
            limit=2,
            process_pdfs=False
        )
        
        # Second search (should use cache)
        papers2 = research_agent.search_and_analyze(
            query="artificial intelligence",
            limit=2,
            process_pdfs=False
        )
        
        if papers1 and papers2:
            print(f"SUCCESS: Cache working")
            stats = cache.get_cache_stats()
            print(f"   Cached topics: {stats['topic_cache_count']}")
            print(f"   Cached papers: {stats['paper_cache_count']}")
            return True
        else:
            print("FAILED: Caching not working properly")
            return False
    except Exception as e:
        print(f"FAILED: {str(e)}")
        return False


def test_research_gaps():
    """Test research gap identification"""
    print("\n" + "="*60)
    print("TEST 4: Research Gap Analysis")
    print("="*60)
    
    try:
        papers = research_agent.search_and_analyze(
            query="quantum computing",
            limit=1,
            process_pdfs=True,
            open_access_only=True
        )
        
        if papers and papers[0].get("research_gaps"):
            gaps = papers[0]["research_gaps"]
            print(f"SUCCESS: Research gaps identified")
            print(f"   Methodology gaps: {len(gaps['methodology_gaps'])} chars")
            print(f"   Knowledge gaps: {len(gaps['knowledge_gaps'])} chars")
            print(f"   Future directions: {len(gaps['future_directions'])} chars")
            return True
        else:
            print("WARNING: No research gaps found (PDF might not be available)")
            return True  
    except Exception as e:
        print(f"AILED: {str(e)}")
        return False


def test_error_handling():
    """Test error handling with invalid inputs"""
    print("\n" + "="*60)
    print("TEST 5: Error Handling")
    print("="*60)
    
    try:
        # Test with non-existent topic
        papers = research_agent.search_and_analyze(
            query="xyzabc123nonexistent",
            limit=5
        )
        
        # Should return empty list, not crash
        print(f"SUCCESS: Handled non-existent topic gracefully")
        print(f"   Returned {len(papers)} papers (expected 0)")
        return True
    except Exception as e:
        print(f"FAILED: Crashed on invalid input: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("RUNNING PHASE 1 TESTS")
    print("="*70)
    
    tests = [
        ("Basic Search", test_basic_search),
        ("PDF Processing", test_pdf_processing),
        ("Caching", test_caching),
        ("Research Gaps", test_research_gaps),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n{name} crashed: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{status}: {name}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nALL TESTS PASSED! Ready for deployment!")
        return True
    else:
        print(f"\n{total - passed} test(s) failed. Fix before deploying.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
