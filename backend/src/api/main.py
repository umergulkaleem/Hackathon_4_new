import os
import sys
import time
from typing import List
from urllib.parse import urljoin, urlparse

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bs4 import BeautifulSoup
import requests

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
    Normalize URL for Docusaurus routing.
    Ensures proper trailing slashes and removes double slashes.
    """
    parsed = urlparse(url)
    path = parsed.path

    if trailing_slash and not path.endswith('/'):
        path += '/'
    elif not trailing_slash and path.endswith('/'):
        path = path.rstrip('/')

    path = path.replace('//', '/')

    if '/docs/' in path and path.endswith('/'):
        path = path.rstrip('/')

    return parsed._replace(path=path).geturl()


def get_all_urls(base_url: str, max_pages: int = 100) -> List[str]:
    """
    Crawl the deployed site to find all URLs for processing.
    Includes sitemap parsing, homepage links, and BFS crawling.
    """
    urls = set()
    to_crawl = [base_url]
    visited = set()
    base_domain = urlparse(base_url).netloc

    # Patterns likely to contain content
    content_patterns = [
        '/docs/', '/blog/', '/api/', '/guide/', '/tutorial/',
        '/reference/', '/examples/', '/changelog/', '/about/'
    ]

    # Try fetching sitemap first
    sitemap_url = urljoin(base_url, 'sitemap.xml')
    try:
        response = requests.get(sitemap_url, timeout=30)
        if response.status_code == 200:
            import re
            sitemap_urls = re.findall(r'<loc>(.*?)</loc>', response.text)
            for url in sitemap_urls:
                if any(pat in url for pat in content_patterns):
                    normalized = normalize_url_for_docusaurus(url, trailing_slash=True)
                    urls.add(normalized)
    except Exception as e:
        logger.warning(f"Could not fetch sitemap: {str(e)}")

    # Crawl starting from homepage
    pages_crawled = 0
    while to_crawl and pages_crawled < max_pages:
        current_url = to_crawl.pop(0)
        if current_url in visited:
            continue
        visited.add(current_url)
        pages_crawled += 1

        try:
            response = requests.get(current_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Add current page if it matches content patterns
            if any(pat in current_url for pat in content_patterns) or current_url == base_url:
                urls.add(normalize_url_for_docusaurus(current_url, trailing_slash=True))

            # Find all links on this page
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                absolute_url = urljoin(current_url, href)
                parsed_url = urlparse(absolute_url)
                if parsed_url.netloc == base_domain and absolute_url not in visited:
                    if absolute_url.startswith(base_url) and not any(absolute_url.endswith(ext) for ext in ['.pdf', '.jpg', '.png', '.zip', '.exe', '.css', '.js', '.ico', '.svg']):
                        if any(pat in absolute_url for pat in content_patterns) or absolute_url.count('/') <= 6:
                            to_crawl.append(absolute_url)

        except Exception as e:
            logger.warning(f"Failed to crawl {current_url}: {str(e)}")
            continue

    return list(urls)


def extract_text_from_urls(urls: List[str]) -> List[MarkdownContent]:
    """
    Extract text from the provided URLs.
    Skips URLs with no actual text content.
    """
    text_service = TextExtractionService()
    contents = []

    for url in urls:
        try:
            content = text_service.extract_from_url(url)
            if content and content.content.strip():
                contents.append(content)
                logger.info(f"Extracted content from {url}")
            else:
                logger.warning(f"No text found in {url}")
        except Exception as e:
            logger.error(f"Failed to extract from {url}: {str(e)}")
            continue

    return contents


def chunk_text(contents: List[MarkdownContent], chunk_size: int = Config.DEFAULT_CHUNK_SIZE, chunk_overlap: int = Config.DEFAULT_CHUNK_OVERLAP) -> List[TextChunk]:
    """
    Chunk the extracted text into smaller pieces.
    """
    chunk_service = SemanticChunkingService(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_chunks: List[TextChunk] = []

    for content in contents:
        chunks = chunk_service.chunk_markdown_content(content)
        all_chunks.extend(chunks)
        logger.info(f"Chunked {len(chunks)} chunks from {content.file_path}")

    return all_chunks


def embed_chunks(chunks: List[TextChunk], batch_size: int = 50) -> List[EmbeddingVector]:
    """
    Generate embeddings for all chunks in batches with retry/backoff.
    """
    embedding_service = EmbeddingGeneratorService()
    all_embeddings: List[EmbeddingVector] = []

    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i + batch_size]
        retries = 0
        success = False
        while not success and retries < 5:
            try:
                embeddings = embedding_service.batch_generate_embeddings(batch_chunks)
                all_embeddings.extend(embeddings)
                success = True
            except Exception as e:
                if "rate limit" in str(e).lower():
                    wait_time = 2 ** retries
                    logger.warning(f"Rate limited, retrying batch in {wait_time}s")
                    time.sleep(wait_time)
                    retries += 1
                else:
                    logger.error(f"Failed to generate embeddings for batch: {str(e)}")
                    success = True  # skip batch if not rate-limit

    return all_embeddings


def save_to_qdrant(embeddings: List[EmbeddingVector], chunks: List[TextChunk], contents: List[MarkdownContent], collection_name: str = "rag_embeddings") -> bool:
    """
    Save embeddings along with metadata to Qdrant collection.
    """
    if not embeddings:
        logger.error("No embeddings to save")
        return False

    qdrant_service = QdrantStorageService(collection_name)
    vector_size = len(embeddings[0].vector)
    qdrant_service.create_new_collection(collection_name, vector_size)

    metadata_list: List[Metadata] = []

    for i, embedding in enumerate(embeddings):
        chunk = chunks[i]
        content = next((c for c in contents if c.id == chunk.source_document_id), None)
        if not content:
            content = contents[0]  # fallback
        metadata = Metadata(
            source_file=content.file_path,
            document_title=content.title,
            chunk_index=chunk.chunk_index,
            headers_hierarchy=" | ".join(chunk.headers_context),
            word_count=chunk.word_count,
            content_type="text",
            content=chunk.content   # <- add actual text for RAG
        )
        metadata_list.append(metadata)

    try:
        success = qdrant_service.save_embeddings(embeddings, metadata_list)
        if success:
            logger.info(f"Saved {len(embeddings)} embeddings to Qdrant collection '{collection_name}'")
        else:
            logger.error("Failed to save embeddings to Qdrant")
        return success
    except Exception as e:
        logger.error(f"Error saving to Qdrant: {str(e)}")
        return False


def main():
    try:
        validate_environment()
        logger.info("Environment validated successfully")

        deployed_url = "https://hackathon-4-new.vercel.app/"

        # Step 1: Get all URLs
        urls = get_all_urls(deployed_url)
        if not urls:
            logger.warning("No URLs found, using base URL only")
            urls = [deployed_url]

        logger.info(f"Total URLs discovered: {len(urls)}")

        # Step 2: Extract text
        contents = extract_text_from_urls(urls)
        if not contents:
            logger.error("No content extracted, aborting pipeline")
            return False

        # Step 3: Chunk text
        chunks = chunk_text(contents)
        if not chunks:
            logger.error("No chunks created, aborting pipeline")
            return False

        # Step 4: Generate embeddings
        embeddings = embed_chunks(chunks)
        if not embeddings:
            logger.error("No embeddings generated, aborting pipeline")
            return False

        # Step 5: Save to Qdrant
        success = save_to_qdrant(embeddings, chunks, contents)
        if not success:
            logger.error("Failed to save embeddings to Qdrant")
            return False

        logger.info("Pipeline completed successfully")
        return True

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("Pipeline completed successfully!")
        sys.exit(0)
    else:
        print("Pipeline failed!")
        sys.exit(1)
