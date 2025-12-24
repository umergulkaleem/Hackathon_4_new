import os
import sys
from typing import List, Dict, Any
from urllib.parse import urljoin
import requests

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ..models.markdown_content import MarkdownContent
from ..models.text_chunk import TextChunk
from ..models.embedding_vector import EmbeddingVector
from ..models.metadata import Metadata
from ..services.text_extraction import TextExtractionService
from ..services.semantic_chunking import SemanticChunkingService
from ..services.embedding_generator import EmbeddingGeneratorService
from ..services.qdrant_storage import QdrantStorageService
from ..lib.config import Config
from ..lib.logging import logger
from ..lib.utils import validate_environment


def normalize_url_for_docusaurus(url: str, trailing_slash: bool = False) -> str:
    """
    Normalize URL to match Docusaurus routing requirements.

    Args:
        url: URL to normalize
        trailing_slash: Whether to ensure trailing slash (set to False for Docusaurus without trailing slash)

    Returns:
        Normalized URL
    """
    from urllib.parse import urlparse, urlunparse

    parsed = urlparse(url)

    # Ensure proper path format for Docusaurus (without trailing slash)
    path = parsed.path
    if trailing_slash and not path.endswith('/'):
        path += '/'
    elif not trailing_slash and path.endswith('/'):
        path = path.rstrip('/')

    # Ensure no double slashes
    path = path.replace('//', '/')

    # Special handling for Docusaurus: remove trailing slash for documentation pages
    if '/docs/' in path and path.endswith('/'):
        path = path.rstrip('/')

    normalized = parsed._replace(path=path)
    return urlunparse(normalized)


def get_all_urls(base_url: str) -> List[str]:
    """
    Get all URLs from the deployed site by crawling and discovering links.

    Args:
        base_url: Base URL of the deployed site

    Returns:
        List[str]: List of URLs to process
    """
    from urllib.parse import urljoin, urlparse
    import requests
    from bs4 import BeautifulSoup
    from collections import deque

    # Set to store discovered URLs to avoid duplicates
    urls = set()

    # Queue for BFS crawling
    to_crawl = deque([base_url])

    # Set to track visited URLs
    visited = set()

    # Parse the base domain to only crawl internal links
    base_domain = urlparse(base_url).netloc

    # Maximum number of pages to crawl to prevent infinite crawling
    max_pages = 100
    pages_crawled = 0

    # Additional patterns to look for in links (for documentation sites like Docusaurus)
    content_patterns = [
        '/docs/', '/blog/', '/api/', '/guide/', '/tutorial/',
        '/reference/', '/examples/', '/changelog/', '/about/'
    ]

    # Enhanced approach: First try to get the sitemap and map all URLs to the production domain
    sitemap_url = urljoin(base_url, 'sitemap.xml')
    try:
        sitemap_response = requests.get(sitemap_url, timeout=30)  # Increased timeout
        if sitemap_response.status_code == 200:
            logger.info("Found sitemap, extracting URLs and mapping to production domain...")
            import re

            # Extract URLs from sitemap using regex to avoid xml parser issues
            urls_from_text = re.findall(r'<loc>(.*?)</loc>', sitemap_response.text)

            production_urls_found = 0
            for url in urls_from_text:
                url = url.strip()

                # Map preview URLs to the new production domain
                if 'hackathon-4-git-' in url and '.vercel.app' in url:
                    # Extract the path from the preview URL and map to new production domain
                    parsed_preview = urlparse(url)
                    production_url = f"https://hackathon-4-new.vercel.app{parsed_preview.path}"
                    if any(pattern in production_url for pattern in content_patterns):
                        # Normalize the URL for Docusaurus routing with trailing slash
                        normalized_url = normalize_url_for_docusaurus(production_url, trailing_slash=True)
                        urls.add(normalized_url)
                        production_urls_found += 1

                elif url.startswith('https://hackathon-4-new.vercel.app') and any(pattern in url for pattern in content_patterns):
                    # Already a new production URL from sitemap
                    normalized_url = normalize_url_for_docusaurus(url, trailing_slash=True)
                    urls.add(normalized_url)
                    production_urls_found += 1

            logger.info(f"Found {production_urls_found} production URLs from sitemap mapped to production domain")
    except Exception as e:
        logger.warning(f"Could not fetch sitemap: {str(e)}")

    # First, directly fetch the base URL to extract all links from the homepage
    try:
        base_response = requests.get(base_url, timeout=30)  # Increased timeout
        base_response.raise_for_status()
        base_soup = BeautifulSoup(base_response.content, 'html.parser')

        # Find all links on the homepage, especially documentation links
        homepage_links = base_soup.find_all('a', href=True)

        for link in homepage_links:
            href = link['href']
            absolute_url = urljoin(base_url, href)
            parsed_url = urlparse(absolute_url)

            # Add documentation links found on the homepage
            if (parsed_url.netloc == base_domain and
                absolute_url.startswith(base_url) and
                any(pattern in absolute_url for pattern in content_patterns)):
                # Normalize the URL for Docusaurus routing with trailing slash
                normalized_url = normalize_url_for_docusaurus(absolute_url, trailing_slash=True)
                urls.add(normalized_url)

        logger.info(f"Found {len(urls)} URLs directly from homepage")
    except Exception as e:
        logger.warning(f"Could not fetch homepage to extract links: {str(e)}")

    # If we found some URLs from homepage, we can skip extensive crawling in some cases
    # But still proceed with crawling to find more links
    while to_crawl and pages_crawled < max_pages:
            current_url = to_crawl.popleft()

            # Skip if already visited
            if current_url in visited:
                continue

            visited.add(current_url)
            pages_crawled += 1

            try:
                # Fetch the page content
                response = requests.get(current_url, timeout=15)  # Increased timeout
                response.raise_for_status()

                # Add current URL to the set of URLs to process if it's likely to have content
                has_content = any(pattern in current_url for pattern in content_patterns) or current_url == base_url
                if has_content:
                    normalized_url = normalize_url_for_docusaurus(current_url, trailing_slash=True)
                    urls.add(normalized_url)

                # Parse the HTML content
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all links on the page with different selectors for Docusaurus sites
                all_links = soup.find_all('a', href=True)

                # Also look for nav links and sidebar links which are common in Docusaurus
                nav_links = soup.find_all(['nav', 'div'], {'class': lambda x: x and ('nav' in x or 'menu' in x or 'sidebar' in x)})
                for nav in nav_links:
                    all_links.extend(nav.find_all('a', href=True))

                for link in all_links:
                    href = link['href']

                    # Convert relative URLs to absolute URLs
                    absolute_url = urljoin(current_url, href)

                    # Parse the URL to check if it's within the same domain
                    parsed_url = urlparse(absolute_url)

                    # Only add URLs from the same domain and with proper structure
                    if parsed_url.netloc == base_domain and absolute_url not in visited:
                        # Only include URLs that are likely to contain content (not external links)
                        if absolute_url.startswith(base_url) and not any(absolute_url.endswith(ext) for ext in ['.pdf', '.jpg', '.png', '.zip', '.exe', '.css', '.js', '.ico', '.svg']):
                            # Check if it matches content patterns or is a likely page
                            # Loosened the criteria to capture more documentation pages
                            if any(pattern in absolute_url for pattern in content_patterns) or absolute_url.count('/') <= 6:
                                # Normalize the URL for Docusaurus routing with trailing slash
                                normalized_url = normalize_url_for_docusaurus(absolute_url, trailing_slash=True)
                                if normalized_url not in to_crawl:
                                    to_crawl.append(normalized_url)

            except requests.exceptions.RequestException as e:
                logger.warning(f"Failed to crawl {current_url}: {str(e)}")
                continue
            except Exception as e:
                logger.warning(f"Unexpected error while crawling {current_url}: {str(e)}")
                continue

    # Convert set to list
    url_list = list(urls)

    logger.info(f"Found {len(url_list)} URLs to process after crawling")
    return url_list


def extract_text_from_urls(urls: List[str]) -> List[MarkdownContent]:
    """
    Extract text from the provided URLs.

    Args:
        urls: List of URLs to extract text from

    Returns:
        List[MarkdownContent]: List of extracted content
    """
    text_extraction_service = TextExtractionService()
    contents = []

    for url in urls:
        try:
            content = text_extraction_service.extract_from_url(url)
            contents.append(content)
            logger.info(f"Successfully extracted content from {url}")
        except Exception as e:
            logger.error(f"Failed to extract content from {url}: {str(e)}")
            continue

    return contents


def chunk_text(contents: List[MarkdownContent], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[TextChunk]:
    """
    Chunk the provided content.

    Args:
        contents: List of MarkdownContent to chunk
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks

    Returns:
        List[TextChunk]: List of text chunks
    """
    chunking_service = SemanticChunkingService(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_chunks = []

    for content in contents:
        chunks = chunking_service.chunk_markdown_content(content)
        all_chunks.extend(chunks)
        logger.info(f"Chunked content from {content.file_path} into {len(chunks)} chunks")

    return all_chunks


def embed(chunks: List[TextChunk]) -> List[EmbeddingVector]:
    """
    Generate embeddings for the provided text chunks.

    Args:
        chunks: List of TextChunk to generate embeddings for

    Returns:
        List[EmbeddingVector]: List of embedding vectors
    """
    embedding_service = EmbeddingGeneratorService()
    embeddings = embedding_service.batch_generate_embeddings(chunks)

    logger.info(f"Generated {len(embeddings)} embeddings for {len(chunks)} chunks")
    return embeddings


def create_collections(collection_name: str = "rag_embeddings", vector_size: int = 768) -> bool:
    """
    Create Qdrant collections for storing embeddings.

    Args:
        collection_name: Name of the collection to create
        vector_size: Size of the embedding vectors

    Returns:
        bool: True if collection was created successfully
    """
    storage_service = QdrantStorageService(collection_name)
    # The collection is automatically created when the service is initialized
    # But we can still call this method to ensure it exists
    try:
        storage_service.create_new_collection(collection_name, vector_size)
        logger.info(f"Collection '{collection_name}' is ready for use")
        return True
    except Exception as e:
        logger.error(f"Failed to create collection '{collection_name}': {str(e)}")
        return False


def save_chunk_to_qdrant(embeddings: List[EmbeddingVector], chunks: List[TextChunk], contents: List[MarkdownContent], collection_name: str = "rag_embeddings") -> bool:
    """
    Save embeddings and their metadata to Qdrant.

    Args:
        embeddings: List of EmbeddingVector to save
        chunks: List of TextChunk objects for metadata
        contents: List of original MarkdownContent for metadata
        collection_name: Name of the collection to save to

    Returns:
        bool: True if embeddings were saved successfully
    """
    from ..services.embedding_validator import EmbeddingValidatorService

    # First, validate the embeddings before saving
    validator = EmbeddingValidatorService()
    validation_result = validator.validate_embeddings_quality(embeddings)

    if not validation_result["valid"]:
        logger.error(f"Embeddings failed validation: {validation_result['message']}")
        return False

    logger.info(f"Embeddings passed quality validation with score: {validation_result['metrics']['quality_percentage']:.2f}%")

    storage_service = QdrantStorageService(collection_name)

    # Create metadata for each embedding
    metadata_list = []
    for i, embedding in enumerate(embeddings):
        # Find the corresponding chunk and content
        chunk = chunks[i] if i < len(chunks) else None
        content = None

        if chunk:
            # Find content that matches the chunk's source
            for c in contents:
                if c.id == chunk.source_document_id:
                    content = c
                    break
            if not content and len(contents) > 0:
                content = contents[0]  # Fallback to first content

        if content and chunk:
            metadata = Metadata(
                source_file=content.file_path,
                document_title=content.title,
                chunk_index=chunk.chunk_index,
                headers_hierarchy=" | ".join(chunk.headers_context),
                word_count=chunk.word_count,
                content_type="text"
            )
        elif content:
            metadata = Metadata(
                source_file=content.file_path,
                document_title=content.title,
                chunk_index=0,
                headers_hierarchy=" | ".join(content.headers),
                word_count=0,
                content_type="text"
            )
        else:
            metadata = Metadata(
                source_file="unknown",
                document_title="unknown",
                chunk_index=0,
                headers_hierarchy="",
                word_count=0,
                content_type="text"
            )

        metadata_list.append(metadata)

    # Validate metadata linkage before saving (using Qdrant storage service)
    storage_service_for_validation = QdrantStorageService(collection_name)
    embedding_ids = [embed.id for embed in embeddings]
    expected_source_files = [meta.source_file for meta in metadata_list]
    metadata_linkage_valid = storage_service_for_validation.validate_metadata_linkage(embedding_ids, expected_source_files)
    if not metadata_linkage_valid:
        logger.error("Metadata linkage validation failed")
        return False

    try:
        success = storage_service.save_embeddings(embeddings, metadata_list)
        logger.info(f"Successfully saved {len(embeddings)} embeddings to Qdrant")
        return success
    except Exception as e:
        logger.error(f"Failed to save embeddings to Qdrant: {str(e)}")
        return False


def main():
    """
    Main function to execute the complete pipeline:
    1. Get all URLs from the deployed site
    2. Extract text from URLs
    3. Chunk the text
    4. Generate embeddings
    5. Create Qdrant collection
    6. Save embeddings to Qdrant
    """
    try:
        # Validate environment
        validate_environment()
        logger.info("Environment validated successfully")

        # Use the deployed link provided by the user
        deployed_url = "https://hackathon-4-new.vercel.app/"

        # Step 1: Get all URLs
        logger.info("Step 1: Getting all URLs from deployed site...")
        urls = get_all_urls(deployed_url)
        logger.info(f"Discovered {len(urls)} URLs to process")
        if not urls:
            logger.warning("No URLs found, using the base URL")
            urls = [deployed_url]

        # Step 2: Extract text from URLs
        logger.info("Step 2: Extracting text from URLs...")
        contents = extract_text_from_urls(urls)

        if not contents:
            logger.error("No content extracted from any URLs")
            return False

        # Validate that we have unique content from different URLs
        logger.info("Validating content uniqueness...")
        unique_contents = set()
        duplicate_count = 0
        for i, content in enumerate(contents):
            content_hash = hash(content.content[:100] if len(content.content) > 100 else content.content)  # Use first 100 chars as hash
            if content_hash in unique_contents:
                logger.warning(f"Duplicate content detected for {content.file_path}")
                duplicate_count += 1
            else:
                unique_contents.add(content_hash)

        logger.info(f"Out of {len(contents)} URLs, found {len(unique_contents)} unique content items, {duplicate_count} duplicates")

        if len(unique_contents) < len(contents) * 0.5:  # If more than 50% are duplicates
            logger.warning("High percentage of duplicate content detected - this may indicate content extraction issues")
        else:
            logger.info("Content diversity looks good")

        # Step 3: Chunk the text
        logger.info("Step 3: Chunking text content...")
        chunks = []
        for content in contents:
            content_chunks = chunk_text([content], chunk_size=Config.DEFAULT_CHUNK_SIZE, chunk_overlap=Config.DEFAULT_CHUNK_OVERLAP)
            chunks.extend(content_chunks)

        if not chunks:
            logger.error("No chunks created from content")
            return False

        logger.info(f"Created {len(chunks)} total chunks from {len(contents)} documents")

        # Step 4: Generate embeddings
        logger.info("Step 4: Generating embeddings...")
        embeddings = embed(chunks)
        if not embeddings:
            logger.error("No embeddings generated")
            return False

        # Step 5: Create Qdrant collection with specific name for the deployed site
        collection_name = "docusaurus_hackathon_4_embeddings"
        logger.info(f"Step 5: Creating Qdrant collection '{collection_name}'...")
        collection_created = create_collections(collection_name=collection_name)
        if not collection_created:
            logger.error("Failed to create Qdrant collection")
            return False

        # Step 6: Save embeddings to Qdrant
        logger.info("Step 6: Saving embeddings to Qdrant...")
        save_success = save_chunk_to_qdrant(embeddings, chunks, contents, collection_name=collection_name)
        if not save_success:
            logger.error("Failed to save embeddings to Qdrant")
            return False

        logger.info("Pipeline completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("Pipeline completed successfully!")
        sys.exit(0)
    else:
        print("Pipeline failed!")
        sys.exit(1)
