#!/usr/bin/env python3
"""
Docusaurus to Qdrant Ingestor

This script ingests content from a Docusaurus site into Qdrant for RAG applications.
It fetches URLs from the sitemap, extracts content, generates embeddings, and stores
them with metadata in Qdrant.
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse, urlunparse
from qdrant_client import QdrantClient
from qdrant_client.http import models
import openai
import logging
import time
from typing import List, Dict, Optional
import hashlib
import os
from uuid import uuid4


class DocusaurusQdrantIngestor:
    def __init__(self, qdrant_url: str = "http://localhost:6333", openai_api_key: str = None):
        """
        Initialize the Docusaurus to Qdrant ingester.

        Args:
            qdrant_url: URL to the Qdrant instance
            openai_api_key: OpenAI API key for embeddings (if using OpenAI)
        """
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(url=qdrant_url)

        # Initialize OpenAI client if API key provided
        if openai_api_key:
            openai.api_key = openai_api_key

        # Collection name for storing embeddings
        self.collection_name = "docusaurus_embeddings"

        # Create collection if it doesn't exist
        self._create_collection()

    def _create_collection(self):
        """Create Qdrant collection if it doesn't exist."""
        try:
            # Check if collection exists
            collections = self.qdrant_client.get_collections()
            collection_names = [collection.name for collection in collections.collections]

            if self.collection_name not in collection_names:
                # Create collection with 1536 dimensions for OpenAI embeddings
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)
                )
                self.logger.info(f"Created collection '{self.collection_name}'")
            else:
                self.logger.info(f"Collection '{self.collection_name}' already exists")
        except Exception as e:
            self.logger.error(f"Error creating collection: {e}")
            raise

    def fetch_sitemap_urls(self, sitemap_url: str) -> List[str]:
        """
        Fetch all URLs from the sitemap.xml file.

        Args:
            sitemap_url: URL to the sitemap.xml file

        Returns:
            List of URLs extracted from the sitemap
        """
        self.logger.info(f"Fetching sitemap from {sitemap_url}")

        try:
            response = requests.get(sitemap_url, timeout=30)
            response.raise_for_status()

            # Parse the sitemap XML content
            soup = BeautifulSoup(response.content, 'xml')

            # Find all <loc> tags which contain the URLs
            loc_tags = soup.find_all('loc')
            urls = []

            for loc in loc_tags:
                url = loc.get_text().strip()
                if url:
                    # Normalize URL: ensure trailing slash, remove query params/fragments
                    normalized_url = self._normalize_url(url)
                    urls.append(normalized_url)

            self.logger.info(f"Found {len(urls)} URLs in sitemap")
            return urls

        except requests.RequestException as e:
            self.logger.error(f"Error fetching sitemap: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error parsing sitemap: {e}")
            return []

    def _normalize_url(self, url: str) -> str:
        """
        Normalize URL by ensuring leading slash, trailing slash, and removing query parameters/fragments.

        Args:
            url: Original URL to normalize

        Returns:
            Normalized URL
        """
        parsed = urlparse(url)

        # Remove query parameters and fragments
        normalized = parsed._replace(query='', fragment='')

        # Ensure leading slash
        path = normalized.path
        if not path.startswith('/'):
            path = '/' + path

        # Ensure trailing slash
        if not path.endswith('/'):
            path = path + '/'

        normalized = normalized._replace(path=path)

        return urlunparse(normalized)

    def is_url_accessible(self, url: str) -> bool:
        """
        Check if a URL is accessible (returns 200 status).

        Args:
            url: URL to check

        Returns:
            True if URL is accessible, False otherwise
        """
        try:
            response = requests.head(url, timeout=10)
            return response.status_code == 200
        except:
            return False

    def extract_content_from_url(self, url: str) -> Optional[Dict[str, str]]:
        """
        Extract main content from a Docusaurus page.

        Args:
            url: URL of the page to extract content from

        Returns:
            Dictionary with content, title, and module/section info, or None if failed
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else "No Title"

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Try to find main content area (Docusaurus specific selectors)
            main_content = None

            # Common Docusaurus content selectors
            selectors = [
                'main div[class*="docItemContainer"]',  # Docusaurus docs container
                'article',  # General article tag
                'main',  # Main content area
                'div.main-wrapper',  # Docusaurus main wrapper
                'div.container',  # Container div
                'div[class*="docItem"]',  # Docusaurus doc item
                'div[class*="theme"]',  # Theme-related content
            ]

            for selector in selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    break

            # If no specific content area found, use body
            if not main_content:
                main_content = soup.find('body')

            if main_content:
                # Extract text content
                content = main_content.get_text(separator=' ', strip=True)

                # Clean up content (remove extra whitespace)
                content = re.sub(r'\s+', ' ', content)

                # Extract module/section from URL path
                parsed_url = urlparse(url)
                path_parts = [part for part in parsed_url.path.strip('/').split('/') if part]

                # Determine module/section based on URL structure
                module_section = "General"
                if len(path_parts) >= 2:
                    if path_parts[0] == 'docs':
                        if len(path_parts) > 1:
                            module_section = path_parts[1]  # First part after docs/

                return {
                    'url': url,
                    'title': title,
                    'content': content,
                    'module_section': module_section
                }
            else:
                self.logger.warning(f"No content found for {url}")
                return None

        except requests.RequestException as e:
            self.logger.error(f"Error fetching content from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error extracting content from {url}: {e}")
            return None

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI API.

        Args:
            text: Text to generate embedding for

        Returns:
            List of floats representing the embedding
        """
        try:
            # Use OpenAI API to generate embedding
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"  # Using the recommended embedding model
            )

            embedding = response['data'][0]['embedding']
            return embedding

        except Exception as e:
            self.logger.error(f"Error generating embedding for text: {e}")
            # Return a zero vector if embedding fails
            return [0.0] * 1536

    def store_in_qdrant(self, content_data: Dict[str, str], embedding: List[float]):
        """
        Store content with embedding in Qdrant.

        Args:
            content_data: Dictionary with content, title, URL, module/section
            embedding: Embedding vector to store
        """
        try:
            # Create a unique ID for this record
            content_id = str(uuid4())

            # Create payload with metadata
            payload = {
                'url': content_data['url'],
                'title': content_data['title'],
                'module_section': content_data['module_section'],
                'content': content_data['content'][:1000],  # Store first 1000 chars as preview
                'timestamp': time.time()
            }

            # Store in Qdrant
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=content_id,
                        vector=embedding,
                        payload=payload
                    )
                ]
            )

            self.logger.info(f"Stored content from {content_data['url']} in Qdrant")

        except Exception as e:
            self.logger.error(f"Error storing content in Qdrant: {e}")

    def process_docusaurus_site(self, base_url: str):
        """
        Main method to process the entire Docusaurus site.

        Args:
            base_url: Base URL of the Docusaurus site
        """
        # Construct sitemap URL
        sitemap_url = f"{base_url.rstrip('/')}/sitemap.xml"

        # Fetch URLs from sitemap
        all_urls = self.fetch_sitemap_urls(sitemap_url)

        if not all_urls:
            self.logger.error("No URLs found in sitemap, exiting.")
            return

        # Process each URL
        processed_count = 0
        for i, url in enumerate(all_urls):
            self.logger.info(f"Processing {i+1}/{len(all_urls)}: {url}")

            # Check if URL is accessible
            if not self.is_url_accessible(url):
                self.logger.warning(f"URL not accessible, skipping: {url}")
                continue

            # Extract content from URL
            content_data = self.extract_content_from_url(url)

            if not content_data:
                self.logger.warning(f"Could not extract content, skipping: {url}")
                continue

            # Generate embedding for the content
            embedding = self.generate_embedding(content_data['content'])

            if not embedding:
                self.logger.warning(f"Could not generate embedding, skipping: {url}")
                continue

            # Store in Qdrant
            self.store_in_qdrant(content_data, embedding)

            processed_count += 1

            # Add a small delay to avoid overwhelming the server
            time.sleep(0.1)

        self.logger.info(f"Successfully processed {processed_count} out of {len(all_urls)} URLs")


def main():
    """
    Main function to run the Docusaurus to Qdrant ingestion process.
    """
    # Configuration
    BASE_URL = "https://hackathon-4-new.vercel.app/"
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Set this in your environment

    if not OPENAI_API_KEY:
        print("Please set the OPENAI_API_KEY environment variable")
        return

    # Create the ingester
    ingester = DocusaurusQdrantIngestor(
        qdrant_url=QDRANT_URL,
        openai_api_key=OPENAI_API_KEY
    )

    # Process the Docusaurus site
    ingester.process_docusaurus_site(BASE_URL)


if __name__ == "__main__":
    main()