#!/usr/bin/env python3
"""
Test script for RAG retrieval validation pipeline
"""
from retrieve import RAGValidator

def test_validation_pipeline():
    """Test the complete validation pipeline"""
    print("🧪 Testing RAG retrieval validation pipeline...")

    # Initialize validator
    validator = RAGValidator()

    # Test with a sample query
    sample_query = "What are vector embeddings?"
    print(f"\n🔍 Testing with query: '{sample_query}'")

    # Run validation
    result = validator.run_validation(
        query=sample_query,
        top_k=3,
        min_score=0.0,
        verbose=True
    )

    print(f"\n✅ Pipeline test {'PASSED' if result else 'FAILED'}")

    # Test with multiple queries from file
    print(f"\n🔍 Testing batch validation with query file...")
    try:
        with open('test_queries.txt', 'r', encoding='utf-8') as f:
            queries = [line.strip() for line in f if line.strip()]

        all_passed = True
        for query in queries:
            print(f"\nProcessing query: {query}")
            result = validator.run_validation(query, top_k=2, verbose=False)
            all_passed = all_passed and result

        print(f"\n✅ Batch validation test {'PASSED' if all_passed else 'FAILED'}")

    except Exception as e:
        print(f"❌ Batch validation test failed: {str(e)}")
        all_passed = False

    return result and all_passed

if __name__ == "__main__":
    success = test_validation_pipeline()
    print(f"\n🏁 Overall test result: {'✅ PASSED' if success else '❌ FAILED'}")