import unittest
from unittest.mock import Mock, patch
from src.services.embedding_generator import EmbeddingGeneratorService
from src.models.text_chunk import TextChunk
from src.models.embedding_vector import EmbeddingVector

class TestEmbeddingGeneratorService(unittest.TestCase):
    """
    Unit tests for EmbeddingGeneratorService
    """

    def setUp(self):
        """Set up test fixtures"""
        # Mock the Cohere client to avoid actual API calls
        with patch('src.services.embedding_generator.cohere.Client') as mock_client:
            self.mock_cohere_client = Mock()
            mock_client.return_value = self.mock_cohere_client
            self.service = EmbeddingGeneratorService()

    def test_generate_embedding_for_single_chunk(self):
        """Test generating embedding for a single chunk"""
        # Create a mock text chunk
        chunk = TextChunk(
            id="test_chunk_id",
            content="This is test content for embedding.",
            chunk_index=0,
            source_document_id="test_source"
        )

        # Mock the embed response
        mock_response = Mock()
        mock_response.embeddings = [[0.1, 0.2, 0.3, 0.4]]
        self.mock_cohere_client.embed.return_value = mock_response

        # Generate embedding
        embedding = self.service.generate_embedding_for_single_chunk(chunk)

        # Verify the embedding was created
        self.assertIsInstance(embedding, EmbeddingVector)
        self.assertEqual(embedding.chunk_id, chunk.id)
        self.assertEqual(len(embedding.vector), 4)  # 4 dimensions in mock
        self.assertEqual(embedding.dimension, 4)

    def test_batch_generate_embeddings(self):
        """Test generating embeddings for multiple chunks"""
        # Create mock text chunks
        chunks = [
            TextChunk(
                id="chunk_1",
                content="First chunk content.",
                chunk_index=0,
                source_document_id="test_source"
            ),
            TextChunk(
                id="chunk_2",
                content="Second chunk content.",
                chunk_index=1,
                source_document_id="test_source"
            )
        ]

        # Mock the embed response
        mock_response = Mock()
        mock_response.embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        self.mock_cohere_client.embed.return_value = mock_response

        # Generate embeddings
        embeddings = self.service.batch_generate_embeddings(chunks, batch_size=2)

        # Verify the embeddings were created
        self.assertEqual(len(embeddings), 2)
        for i, embedding in enumerate(embeddings):
            self.assertIsInstance(embedding, EmbeddingVector)
            self.assertEqual(embedding.chunk_id, chunks[i].id)
            self.assertEqual(len(embedding.vector), 3)  # 3 dimensions in mock


if __name__ == '__main__':
    unittest.main()