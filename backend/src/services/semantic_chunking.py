from typing import List, Optional
from ..models.text_chunk import TextChunk
from ..models.markdown_content import MarkdownContent
from ..lib.logging import logger
import re
from uuid import uuid4

class SemanticChunkingService:
    """
    Service for semantically chunking text content while preserving document structure.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the semantic chunking service.

        Args:
            chunk_size: Maximum size of each chunk
            chunk_overlap: Overlap between chunks to maintain context
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, content: str, source_document_id: str, headers_context: List[str] = None) -> List[TextChunk]:
        """
        Chunk the text while preserving semantic boundaries and document structure.

        Args:
            content: Text content to chunk
            source_document_id: ID of the source document
            headers_context: Contextual headers for the content

        Returns:
            List[TextChunk]: List of semantically coherent text chunks
        """
        if headers_context is None:
            headers_context = []

        # Split content by paragraphs and major sections to maintain semantic boundaries
        paragraphs = self._split_by_paragraphs(content)

        chunks = []
        chunk_index = 0

        for paragraph in paragraphs:
            # If paragraph is larger than chunk size, further split it
            if len(paragraph) > self.chunk_size:
                sub_chunks = self._split_large_paragraph(paragraph)
                for sub_chunk in sub_chunks:
                    chunk = self._create_text_chunk(sub_chunk, source_document_id, chunk_index, headers_context)
                    chunks.append(chunk)
                    chunk_index += 1
            else:
                chunk = self._create_text_chunk(paragraph, source_document_id, chunk_index, headers_context)
                chunks.append(chunk)
                chunk_index += 1

        logger.info(f"Created {len(chunks)} chunks from content")
        return chunks

    def chunk_markdown_content(self, markdown_content: MarkdownContent) -> List[TextChunk]:
        """
        Chunk Markdown content while preserving document structure and headers.

        Args:
            markdown_content: MarkdownContent object to chunk

        Returns:
            List[TextChunk]: List of semantically coherent text chunks
        """
        # Extract content and preserve headers
        content = markdown_content.content
        headers = markdown_content.headers

        # Process content with document structure awareness
        chunks = self.chunk_text(content, markdown_content.id, headers)

        # Add document structure information to each chunk
        for i, chunk in enumerate(chunks):
            # Add relevant headers to the chunk based on position in document
            relevant_headers = self._get_relevant_headers(headers, i, len(chunks))
            chunk.headers_context = relevant_headers

        logger.info(f"Chunked markdown content from {markdown_content.file_path} into {len(chunks)} chunks")
        return chunks

    def _split_by_paragraphs(self, content: str) -> List[str]:
        """
        Split content by paragraphs and major sections.

        Args:
            content: Content to split

        Returns:
            List[str]: List of content sections
        """
        # Split by double newlines (paragraphs) and major section breaks
        sections = re.split(r'\n\s*\n', content)
        # Filter out empty sections
        sections = [section.strip() for section in sections if section.strip()]
        return sections

    def _split_large_paragraph(self, paragraph: str) -> List[str]:
        """
        Split a large paragraph into smaller chunks while maintaining sentence boundaries.

        Args:
            paragraph: Large paragraph to split

        Returns:
            List[str]: List of smaller text chunks
        """
        # Use a more efficient approach for large paragraphs
        if len(paragraph) <= self.chunk_size:
            return [paragraph]

        chunks = []
        sentences = re.split(r'(?<=[.!?])\s+', paragraph)

        current_chunk = ""
        for sentence in sentences:
            # Check if adding the sentence would exceed chunk size
            test_chunk = current_chunk + " " + sentence if current_chunk else sentence

            if len(test_chunk) <= self.chunk_size:
                current_chunk = test_chunk
            else:
                # If current chunk is not empty, save it and start a new one with the sentence
                if current_chunk:
                    chunks.append(current_chunk.strip())
                # If the sentence itself is too long, we need to split it
                if len(sentence) > self.chunk_size:
                    # Split the long sentence into smaller parts
                    sentence_chunks = self._split_long_sentence(sentence)
                    chunks.extend(sentence_chunks[:-1])  # Add all but the last part
                    current_chunk = sentence_chunks[-1]  # Keep the last part as the start of the next chunk
                else:
                    current_chunk = sentence

        # Add the final chunk if it exists
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def _split_long_sentence(self, sentence: str) -> List[str]:
        """
        Split a sentence that is longer than the chunk size into smaller parts.

        Args:
            sentence: Long sentence to split

        Returns:
            List[str]: List of sentence chunks
        """
        if len(sentence) <= self.chunk_size:
            return [sentence]

        chunks = []
        words = sentence.split()

        current_chunk = ""
        for word in words:
            test_chunk = current_chunk + " " + word if current_chunk else word

            if len(test_chunk) <= self.chunk_size:
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = word

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def _create_text_chunk(self, content: str, source_document_id: str, chunk_index: int, headers_context: List[str]) -> TextChunk:
        """
        Create a TextChunk object from content.

        Args:
            content: Content for the chunk
            source_document_id: ID of the source document
            chunk_index: Index of this chunk in the document
            headers_context: Contextual headers

        Returns:
            TextChunk: Created TextChunk object
        """
        chunk_id = str(uuid4())
        text_chunk = TextChunk(
            id=chunk_id,
            content=content,
            chunk_index=chunk_index,
            source_document_id=source_document_id,
            headers_context=headers_context.copy()
        )
        text_chunk.calculate_counts()
        return text_chunk

    def _get_relevant_headers(self, all_headers: List[str], chunk_index: int, total_chunks: int) -> List[str]:
        """
        Get relevant headers for a specific chunk based on document position.

        Args:
            all_headers: All headers in the document
            chunk_index: Index of the current chunk
            total_chunks: Total number of chunks

        Returns:
            List[str]: Relevant headers for this content section
        """
        if not all_headers:
            return []

        # Analyze the headers hierarchy to find relevant ones
        # This is a simplified approach - in a more advanced implementation,
        # we'd analyze the actual position of the chunk in the document
        relevant_headers = []
        for header in all_headers:
            # Add logic to determine which headers are relevant to this chunk
            # For now, we'll return all headers, but in a real implementation
            # we'd use document position to determine relevant headers
            relevant_headers.append(header)

        return relevant_headers

    def enhance_chunking_with_document_hierarchy(self, content: str, headers: List[str], source_document_id: str) -> List[TextChunk]:
        """
        Enhanced chunking that respects document hierarchy and structure.

        Args:
            content: Content to chunk
            headers: Headers from the document
            source_document_id: ID of the source document

        Returns:
            List[TextChunk]: List of text chunks with document hierarchy context
        """
        # Split content by major sections (based on headers)
        sections = self._split_by_headers(content, headers)

        chunks = []
        chunk_index = 0

        for section_content, section_headers in sections:
            # Chunk each section individually while preserving header context
            section_chunks = self.chunk_text(section_content, source_document_id, section_headers)
            for chunk in section_chunks:
                chunk.chunk_index = chunk_index
                chunks.append(chunk)
                chunk_index += 1

        return chunks

    def _split_by_headers(self, content: str, headers: List[str]) -> List[tuple]:
        """
        Split content by headers to maintain document structure.

        Args:
            content: Content to split
            headers: Headers in the document

        Returns:
            List[tuple]: List of (content_section, headers_context) tuples
        """
        if not headers:
            return [(content, [])]

        # This is a simplified implementation
        # In a real implementation, we'd use the headers to split the content properly
        sections = [(content, headers)]
        return sections

    def update_chunk_size(self, new_chunk_size: int):
        """
        Update the chunk size parameter.

        Args:
            new_chunk_size: New chunk size value
        """
        self.chunk_size = new_chunk_size
        logger.info(f"Updated chunk size to {new_chunk_size}")

    def update_chunk_overlap(self, new_chunk_overlap: int):
        """
        Update the chunk overlap parameter.

        Args:
            new_chunk_overlap: New chunk overlap value
        """
        self.chunk_overlap = new_chunk_overlap
        logger.info(f"Updated chunk overlap to {new_chunk_overlap}")