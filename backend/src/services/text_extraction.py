from bs4 import BeautifulSoup
import markdown
from typing import List, Dict, Any, Optional
from ..models.markdown_content import MarkdownContent
from ..lib.logging import logger
import os
import requests
from urllib.parse import urljoin, urlparse

class TextExtractionService:
    """
    Service for extracting clean text from Markdown files, preserving document structure.
    """

    @staticmethod
    def extract_from_file(file_path: str) -> MarkdownContent:
        """
        Extract content from a Markdown file.

        Args:
            file_path: Path to the Markdown file

        Returns:
            MarkdownContent: Extracted content with metadata
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Extract title from first heading if available
            title = TextExtractionService._extract_title(content)

            # Extract headers to preserve document structure
            headers = TextExtractionService._extract_headers(content)

            # Create MarkdownContent object
            markdown_content = MarkdownContent(
                id=file_path,
                file_path=file_path,
                content=content,
                title=title,
                headers=headers
            )

            logger.info(f"Successfully extracted content from {file_path}")
            return markdown_content

        except Exception as e:
            logger.error(f"Error extracting content from {file_path}: {str(e)}")
            raise

    @staticmethod
    def extract_from_url(url: str) -> MarkdownContent:
        """
        Extract content from a URL.

        Args:
            url: URL to fetch content from

        Returns:
            MarkdownContent: Extracted content with metadata
        """
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Convert Markdown to HTML then extract text
            html = markdown.markdown(response.text)
            soup = BeautifulSoup(html, 'html.parser')

            # Extract clean text
            clean_text = soup.get_text(separator=' ', strip=True)

            # Extract title
            title_tag = soup.find('title')
            title = title_tag.get_text() if title_tag else urlparse(url).path.split('/')[-1]

            # Create a temporary ID based on URL
            content_id = url

            # Create MarkdownContent object
            markdown_content = MarkdownContent(
                id=content_id,
                file_path=url,
                content=clean_text,
                title=title,
                headers=[]
            )

            logger.info(f"Successfully extracted content from {url}")
            return markdown_content

        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")
            raise

    @staticmethod
    def extract_from_string(content: str, source_id: str = "string_input") -> MarkdownContent:
        """
        Extract content from a string.

        Args:
            content: Markdown content as string
            source_id: Identifier for the content source

        Returns:
            MarkdownContent: Extracted content with metadata
        """
        try:
            # Extract title from first heading if available
            title = TextExtractionService._extract_title(content)

            # Extract headers to preserve document structure
            headers = TextExtractionService._extract_headers(content)

            # Create MarkdownContent object
            markdown_content = MarkdownContent(
                id=source_id,
                file_path=source_id,
                content=content,
                title=title,
                headers=headers
            )

            logger.info(f"Successfully extracted content from string input")
            return markdown_content

        except Exception as e:
            logger.error(f"Error extracting content from string: {str(e)}")
            raise

    @staticmethod
    def _extract_title(content: str) -> Optional[str]:
        """
        Extract title from Markdown content (first H1 heading).

        Args:
            content: Markdown content

        Returns:
            Optional[str]: Extracted title or None
        """
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()  # Remove '# ' prefix
            elif line.startswith('##'):
                # If no H1 found, take H2 as title
                return line.lstrip('# ').strip()
        return None

    @staticmethod
    def _extract_headers(content: str) -> List[str]:
        """
        Extract headers from Markdown content.

        Args:
            content: Markdown content

        Returns:
            List[str]: List of headers found in the content
        """
        headers = []
        lines = content.split('\n')

        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                # Count number of # to determine header level
                level = 0
                for char in line:
                    if char == '#':
                        level += 1
                    else:
                        break
                header_text = line[level:].strip()
                headers.append(f"{'#' * level} {header_text}")

        return headers

    @staticmethod
    def extract_headers_with_hierarchy(content: str) -> List[Dict[str, Any]]:
        """
        Extract headers with their hierarchy information.

        Args:
            content: Markdown content

        Returns:
            List[Dict[str, Any]]: List of headers with hierarchy information
        """
        headers = []
        lines = content.split('\n')
        current_path = []

        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('#'):
                # Count number of # to determine header level
                level = 0
                for char in line:
                    if char == '#':
                        level += 1
                    else:
                        break
                header_text = line[level:].strip()

                # Update current path based on header level
                current_path = current_path[:level-1]  # Remove deeper levels
                current_path.append(header_text)

                header_info = {
                    "level": level,
                    "text": header_text,
                    "path": " > ".join(current_path),
                    "line_number": i
                }
                headers.append(header_info)

        return headers

    @staticmethod
    def get_all_urls_from_directory(directory_path: str, base_url: str) -> List[str]:
        """
        Get all Markdown file URLs from a directory structure.

        Args:
            directory_path: Path to the directory containing Markdown files
            base_url: Base URL to construct full URLs

        Returns:
            List[str]: List of URLs for Markdown files
        """
        urls = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.md') or file.endswith('.mdx'):
                    file_path = os.path.join(root, file)
                    # Convert file path to relative path for URL construction
                    rel_path = os.path.relpath(file_path, directory_path)
                    url = urljoin(base_url, rel_path.replace('\\', '/'))
                    urls.append(url)

        logger.info(f"Found {len(urls)} Markdown files in directory")
        return urls