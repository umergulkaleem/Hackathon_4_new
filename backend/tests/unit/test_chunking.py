import unittest
from src.services.semantic_chunking import SemanticChunkingService
from src.models.text_chunk import TextChunk

class TestSemanticChunkingService(unittest.TestCase):
    """
    Unit tests for SemanticChunkingService
    """

    def setUp(self):
        """Set up test fixtures"""
        self.service = SemanticChunkingService(chunk_size=100, chunk_overlap=20)

    def test_chunk_text(self):
        """Test basic text chunking functionality"""
        content = "This is a test paragraph. " * 10  # Create content longer than chunk size
        source_id = "test_source"

        chunks = self.service.chunk_text(content, source_id)

        # Verify we got chunks
        self.assertGreater(len(chunks), 0)

        # Verify each chunk is a TextChunk instance
        for chunk in chunks:
            self.assertIsInstance(chunk, TextChunk)
            self.assertLessEqual(len(chunk.content), self.service.chunk_size + 10)  # Allow some buffer

    def test_chunk_with_headers(self):
        """Test chunking with headers context"""
        content = "This is content with headers context."
        source_id = "test_source"
        headers = ["# Main Header", "## Sub Header"]

        chunks = self.service.chunk_text(content, source_id, headers)

        # Verify headers are preserved in chunks
        for chunk in chunks:
            self.assertEqual(chunk.headers_context, headers)

    def test_create_text_chunk(self):
        """Test creating a single text chunk"""
        content = "Test content for chunking."
        source_id = "test_source"
        headers = ["# Test Header"]
        chunk_index = 0

        chunk = self.service._create_text_chunk(content, source_id, chunk_index, headers)

        # Verify chunk properties
        self.assertIsInstance(chunk, TextChunk)
        self.assertEqual(chunk.content, content)
        self.assertEqual(chunk.source_document_id, source_id)
        self.assertEqual(chunk.chunk_index, chunk_index)
        self.assertEqual(chunk.headers_context, headers)
        self.assertGreater(chunk.word_count, 0)
        self.assertGreater(chunk.char_count, 0)


if __name__ == '__main__':
    unittest.main()