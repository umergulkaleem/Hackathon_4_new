import unittest
import tempfile
import os
from unittest.mock import Mock, patch

from src.services.text_extraction import TextExtractionService
from src.services.semantic_chunking import SemanticChunkingService
from src.services.embedding_generator import EmbeddingGeneratorService
from src.services.qdrant_storage import QdrantStorageService
from src.models.markdown_content import MarkdownContent


class TestFullPipelineIntegration(unittest.TestCase):
    """
    Integration tests for the full markdown to embeddings pipeline
    """

    def setUp(self):
        """Set up test fixtures"""
        self.text_extraction_service = TextExtractionService()
        self.chunking_service = SemanticChunkingService(chunk_size=200, chunk_overlap=50)

        # Mock external services to avoid actual API calls
        with patch('src.services.embedding_generator.cohere.Client'):
            self.embedding_service = EmbeddingGeneratorService()

    def test_full_pipeline_from_text(self):
        """Test the full pipeline from text input to embedding generation"""
        # Create sample markdown content
        markdown_text = """
# Introduction
This is an introduction to our documentation.

## Getting Started
To get started, follow these steps:

1. Install the package
2. Configure your settings
3. Run the application

## Advanced Usage
For advanced users, additional options are available.

### Configuration Options
- Option 1: Description
- Option 2: Description

### Performance Tips
- Tip 1: Improve performance
- Tip 2: Optimize resources
"""

        # Step 1: Extract content
        content = self.text_extraction_service.extract_from_string(
            markdown_text,
            source_id="test_doc"
        )

        # Verify extraction
        self.assertIsInstance(content, MarkdownContent)
        self.assertIsNotNone(content.title)
        self.assertGreater(len(content.content), 0)
        self.assertGreater(len(content.headers), 0)

        # Step 2: Chunk the content
        chunks = self.chunking_service.chunk_markdown_content(content)

        # Verify chunking
        self.assertGreater(len(chunks), 0)
        for chunk in chunks:
            self.assertLessEqual(len(chunk.content), 200)  # chunk_size
            self.assertGreater(len(chunk.content), 0)

        # Step 3: Generate embeddings (mocked)
        with patch.object(self.embedding_service.client, 'embed') as mock_embed:
            # Mock the embedding response
            mock_response = Mock()
            mock_response.embeddings = [[0.1] * 768 for _ in range(len(chunks))]  # Cohere default dimension
            mock_embed.return_value = mock_response

            embeddings = self.embedding_service.batch_generate_embeddings(chunks)

        # Verify embeddings
        self.assertEqual(len(embeddings), len(chunks))
        for embedding in embeddings:
            self.assertEqual(len(embedding.vector), 768)  # Expected dimension

    def test_pipeline_with_different_chunk_sizes(self):
        """Test the pipeline with different chunk sizes"""
        markdown_text = "# Title\n\n" + "This is a test paragraph. " * 50  # Long content

        # Test with different chunk sizes
        for chunk_size in [100, 200, 500]:
            with self.subTest(chunk_size=chunk_size):
                chunking_service = SemanticChunkingService(chunk_size=chunk_size, chunk_overlap=chunk_size//4)

                # Extract content
                content = self.text_extraction_service.extract_from_string(
                    markdown_text,
                    source_id=f"test_doc_{chunk_size}"
                )

                # Chunk content
                chunks = chunking_service.chunk_markdown_content(content)

                # Verify chunk sizes
                for chunk in chunks:
                    self.assertLessEqual(len(chunk.content), chunk_size + 10)  # Allow some buffer


if __name__ == '__main__':
    unittest.main()