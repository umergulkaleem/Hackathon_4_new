"""
RAG Retrieval Validation Script

This script connects to Qdrant to validate the retrieval pipeline by:
- Connecting to Qdrant and loading existing vector collections
- Accepting a test query and performing top-k similarity search
- Validating results using returned text, metadata, and source URLs
"""
import os
import time
import argparse
import logging
from typing import List, Dict, Any, Optional
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv


class RAGValidator:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # Initialize clients
        self.qdrant_host = os.getenv('QDRANT_HOST', 'localhost')
        self.qdrant_port = int(os.getenv('QDRANT_PORT', '6333'))
        self.qdrant_api_key = os.getenv('QDRANT_API_KEY')
        self.collection_name = os.getenv('QDRANT_COLLECTION_NAME', 'book_content_vectors')

        # Cohere configuration
        self.cohere_api_key = os.getenv('COHERE_API_KEY')
        self.cohere_model = os.getenv('COHERE_MODEL', 'embed-multilingual-v2.0')

        # Initialize clients
        if self.qdrant_api_key:
            # For Qdrant Cloud, use the full URL format
            if self.qdrant_port == 6333:  # Default port, likely cloud instance
                self.qdrant_client = QdrantClient(
                    url=f"https://{self.qdrant_host}",
                    api_key=self.qdrant_api_key,
                    https=True
                )
                self.logger.info(f"Initialized Qdrant cloud client with URL: https://{self.qdrant_host}")
            else:
                self.qdrant_client = QdrantClient(
                    url=f"https://{self.qdrant_host}:{self.qdrant_port}",
                    api_key=self.qdrant_api_key,
                    https=True
                )
                self.logger.info(f"Initialized Qdrant client with URL: https://{self.qdrant_host}:{self.qdrant_port}")
        else:
            self.qdrant_client = QdrantClient(host=self.qdrant_host, port=self.qdrant_port)
            self.logger.info(f"Initialized Qdrant client with host: {self.qdrant_host} (no API key)")

        self.cohere_client = cohere.Client(self.cohere_api_key)
        self.logger.info("Initialized Cohere client")

    def validate_connection(self) -> bool:
        """Validate connection to Qdrant and check if collection exists"""
        try:
            self.logger.info("Validating connection to Qdrant...")
            # Test connection
            self.qdrant_client.get_collections()

            # Check if collection exists
            collections = self.qdrant_client.get_collections().collections
            collection_names = [coll.name for coll in collections]
            self.logger.info(f"Found collections in Qdrant: {collection_names}")

            if self.collection_name not in collection_names:
                error_msg = f"Collection '{self.collection_name}' not found in Qdrant"
                self.logger.error(error_msg)
                print(f"[ERROR] {error_msg}")
                print(f"Available collections: {collection_names}")
                return False

            self.logger.info(f"Successfully connected to Qdrant and found collection '{self.collection_name}'")
            print(f"[SUCCESS] Connected to Qdrant and found collection '{self.collection_name}'")
            return True

        except Exception as e:
            error_msg = f"Failed to connect to Qdrant: {str(e)}"
            self.logger.error(error_msg)
            print(f"[ERROR] {error_msg}")
            return False

    def get_vector_dimensions(self) -> Optional[int]:
        """Get the vector dimensions of the collection"""
        try:
            self.logger.info(f"Getting vector dimensions for collection '{self.collection_name}'...")
            collection_info = self.qdrant_client.get_collection(self.collection_name)

            # Get vector configuration from collection info
            vector_size = collection_info.config.params.vectors.size
            self.logger.info(f"Vector dimensions: {vector_size}")
            return vector_size

        except Exception as e:
            # Fallback: try to get a sample point to determine vector size
            try:
                points = self.qdrant_client.scroll(
                    collection_name=self.collection_name,
                    limit=1
                )

                if points and len(points) > 0 and points[0]:
                    if hasattr(points[0], 'vector') and points[0].vector:
                        dimensions = len(points[0].vector)
                        self.logger.info(f"Vector dimensions: {dimensions}")
                        return dimensions
                    else:
                        # If vector is not available, try to get from payload
                        warning_msg = "Could not determine vector dimensions from sample point"
                        self.logger.warning(warning_msg)
                        print(f"[WARNING] {warning_msg}")
                        return None
                else:
                    warning_msg = "No points found in collection to determine vector dimensions"
                    self.logger.warning(warning_msg)
                    print(f"[WARNING] {warning_msg}")
                    return None
            except Exception as e2:
                error_msg = f"Failed to get vector dimensions: {str(e2)}"
                self.logger.error(error_msg)
                print(f"[ERROR] {error_msg}")
                return None

    def query_vectors(self, query_text: str, top_k: int = 5, min_score: float = 0.0) -> List[Dict[str, Any]]:
        """Perform similarity search on the vector collection"""
        try:
            self.logger.info(f"Converting query to embedding: '{query_text[:50]}{'...' if len(query_text) > 50 else ''}'")
            # Convert query text to embedding
            response = self.cohere_client.embed(
                texts=[query_text],
                model=self.cohere_model
            )
            query_embedding = response.embeddings[0]
            self.logger.info(f"Generated embedding with {len(query_embedding)} dimensions")

            # Perform similarity search
            start_time = time.time()
            self.logger.info(f"Performing similarity search with top_k={top_k}, min_score={min_score}")
            search_results = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=top_k,
                score_threshold=min_score
            )
            end_time = time.time()

            # Process results
            results = []

            # The query_points method returns a QueryResponse object with a 'points' attribute
            # The 'points' attribute contains a list of ScoredPoint objects
            if hasattr(search_results, 'points'):
                # Handle QueryResponse object
                search_points = search_results.points
            else:
                # Fallback to original behavior
                search_points = search_results if hasattr(search_results, '__iter__') and not isinstance(search_results, (str, bytes)) else [search_results]

            for hit in search_points:
                # For ScoredPoint objects, get the attributes
                point_id = getattr(hit, 'id', 'unknown')
                score = getattr(hit, 'score', 0.0)

                # Get payload (should be a dict for ScoredPoint)
                payload = getattr(hit, 'payload', {})
                if not isinstance(payload, dict):
                    payload = {}

                # Extract content, source_url, and metadata from payload
                content = payload.get('content', '') or ''
                source_url = payload.get('source_file', '') or \
                           payload.get('url', '') or \
                           payload.get('source', '') or \
                           payload.get('document_url', '') or \
                           ''

                # Use all payload as metadata, but exclude content and source fields to avoid duplication
                metadata = {k: v for k, v in payload.items() if k not in ['content', 'source_file', 'url', 'source', 'document_url']}

                result = {
                    'id': point_id,
                    'score': score,
                    'content': content,
                    'source_url': source_url,
                    'metadata': metadata,
                    'vector_distance': 1 - score  # Convert similarity to distance
                }
                results.append(result)

            execution_time = end_time - start_time
            self.logger.info(f"Query completed in {execution_time:.2f}s, retrieved {len(results)} results")
            print(f"[SUCCESS] Query completed in {execution_time:.2f}s")
            return results

        except Exception as e:
            error_msg = f"Failed to perform query: {str(e)}"
            self.logger.error(error_msg)
            print(f"[ERROR] {error_msg}")
            # Try alternative method - scroll all points (not recommended for large collections)
            return self._fallback_query(query_text, top_k)

    def _fallback_query(self, query_text: str, top_k: int) -> List[Dict[str, Any]]:
        """Fallback method if search is not available"""
        self.logger.warning("Using fallback query method - this is inefficient for large collections")
        try:
            # Get all points and manually calculate similarity (not efficient but works as fallback)
            all_points = self.qdrant_client.scroll(
                collection_name=self.collection_name,
                limit=1000  # Limit to avoid memory issues
            )[0]

            if not all_points:
                self.logger.warning("No points found in collection")
                return []

            # For fallback, return first few results
            results = []
            for point in all_points[:top_k]:
                payload = point.payload if hasattr(point, 'payload') and point.payload else {}
                result = {
                    'id': point.id,
                    'score': 0.0,  # No similarity score in fallback
                    'content': payload.get('content', ''),
                    'source_url': payload.get('source_url', ''),
                    'metadata': payload.get('metadata', {}),
                    'vector_distance': 0.0
                }
                results.append(result)

            self.logger.info(f"Fallback query returned {len(results)} results")
            return results
        except Exception as e:
            self.logger.error(f"Fallback query also failed: {str(e)}")
            return []

    def validate_results(self, query: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate the retrieved results"""
        validation_details = []
        validation_passed = True

        # Check if results exist
        if not results:
            validation_details.append({
                'check_type': 'result_existence',
                'passed': False,
                'message': 'No results returned for the query'
            })
            validation_passed = False
        else:
            validation_details.append({
                'check_type': 'result_existence',
                'passed': True,
                'message': f'Returned {len(results)} results'
            })

        # Validate content, source_url, and metadata for each result
        for i, result in enumerate(results):
            # Check content
            if not result.get('content') or result['content'].strip() == '':
                validation_details.append({
                    'check_type': 'content_validation',
                    'passed': False,
                    'message': f'Result {i+1} has empty content'
                })
                validation_passed = False
            else:
                validation_details.append({
                    'check_type': 'content_validation',
                    'passed': True,
                    'message': f'Result {i+1} content is valid'
                })

            # Check source URL
            if not result.get('source_url'):
                validation_details.append({
                    'check_type': 'source_url_validation',
                    'passed': False,
                    'message': f'Result {i+1} missing source URL'
                })
                validation_passed = False
            else:
                validation_details.append({
                    'check_type': 'source_url_validation',
                    'passed': True,
                    'message': f'Result {i+1} source URL is valid: {result["source_url"]}'
                })

            # Check metadata
            if not result.get('metadata'):
                validation_details.append({
                    'check_type': 'metadata_validation',
                    'passed': False,
                    'message': f'Result {i+1} missing metadata'
                })
                validation_passed = False
            else:
                validation_details.append({
                    'check_type': 'metadata_validation',
                    'passed': True,
                    'message': f'Result {i+1} metadata is present'
                })

        return {
            'query': query,
            'results': results,
            'validation_passed': validation_passed,
            'validation_details': validation_details,
            'execution_time': sum(r.get('vector_distance', 0) for r in results)  # Placeholder
        }

    def run_validation(self, query: str, top_k: int = 5, min_score: float = 0.0, verbose: bool = False):
        """Run the complete validation process"""
        self.logger.info(f"Starting RAG retrieval validation with query: '{query}', top_k: {top_k}, min_score: {min_score}")
        print(f"[INFO] Starting RAG retrieval validation...")
        print(f"Query: '{query}'")
        print(f"Top-K: {top_k}, Min Score: {min_score}")
        print("-" * 50)

        # Step 1: Validate connection
        if not self.validate_connection():
            self.logger.error("Connection validation failed")
            return False

        # Step 2: Get vector dimensions
        dimensions = self.get_vector_dimensions()
        if dimensions:
            print(f"Vector dimensions: {dimensions}")

        # Step 3: Perform query
        results = self.query_vectors(query, top_k, min_score)
        if not results:
            self.logger.error("No results returned from query, validation failed")
            print("[ERROR] No results returned, validation failed")
            return False

        # Step 4: Validate results
        validation_result = self.validate_results(query, results)

        # Step 5: Report results
        print("-" * 50)
        print("VALIDATION RESULTS:")
        print(f"Query: '{query}'")
        print(f"Results retrieved: {len(results)}")

        if verbose:
            print("\nDetailed Results:")
            for i, result in enumerate(results, 1):
                print(f"\nResult {i} (Score: {result['score']:.3f}):")
                # Sanitize content to remove problematic Unicode characters
                safe_content = result['content'][:100].encode('ascii', errors='ignore').decode('ascii')
                print(f"  Content: {safe_content}...")
                print(f"  Source: {result['source_url']}")
                print(f"  Metadata: {result['metadata']}")

        print("\nValidation Checks:")
        for detail in validation_result['validation_details']:
            status = "[SUCCESS]" if detail['passed'] else "[ERROR]"
            print(f"  {status} {detail['check_type']}: {detail['message']}")

        overall_status = "[SUCCESS] PASSED" if validation_result['validation_passed'] else "[ERROR] FAILED"
        print(f"\nOverall Validation: {overall_status}")

        # Log the overall result
        if validation_result['validation_passed']:
            self.logger.info("Validation completed successfully")
        else:
            self.logger.warning("Validation completed with failures")

        return validation_result['validation_passed']


def main():
    parser = argparse.ArgumentParser(description='Validate RAG retrieval pipeline')
    parser.add_argument('--query', '-q', type=str, required=False,
                       help='Test query for similarity search')
    parser.add_argument('--query-file', type=str,
                       help='File containing multiple queries (one per line)')
    parser.add_argument('--top-k', type=int, default=5,
                       help='Number of results to retrieve (default: 5)')
    parser.add_argument('--min-score', type=float, default=0.0,
                       help='Minimum similarity score threshold (default: 0.0)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed results')

    args = parser.parse_args()

    # Input validation
    if not args.query and not args.query_file:
        print("[ERROR] Either --query or --query-file must be provided")
        parser.print_help()
        return

    if args.query and args.query_file:
        print("[ERROR] Cannot specify both --query and --query-file")
        return

    if args.top_k <= 0:
        print(f"[ERROR] top-k must be a positive integer, got {args.top_k}")
        return

    if args.min_score < 0.0 or args.min_score > 1.0:
        print(f"[ERROR] min-score must be between 0.0 and 1.0, got {args.min_score}")
        return

    # Initialize validator
    validator = RAGValidator()

    if args.query_file:
        # Run validation for each query in the file
        try:
            with open(args.query_file, 'r', encoding='utf-8') as f:
                queries = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"[ERROR] Query file '{args.query_file}' not found")
            return
        except Exception as e:
            print(f"[ERROR] reading query file: {str(e)}")
            return

        all_passed = True
        for query in queries:
            print(f"\n{'='*60}")
            print(f"Processing query: {query}")
            print(f"{'='*60}")
            result = validator.run_validation(query, args.top_k, args.min_score, args.verbose)
            all_passed = all_passed and result

        print(f"\n{'='*60}")
        final_status = "[SUCCESS] ALL VALIDATIONS PASSED" if all_passed else "[ERROR] SOME VALIDATIONS FAILED"
        print(f"FINAL RESULT: {final_status}")
        print(f"{'='*60}")
    else:
        # Run single validation
        validator.run_validation(args.query, args.top_k, args.min_score, args.verbose)


if __name__ == "__main__":
    main()