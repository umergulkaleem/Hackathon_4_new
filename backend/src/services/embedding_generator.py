import cohere
from typing import List, Dict, Any
from ..models.embedding_vector import EmbeddingVector
from ..models.text_chunk import TextChunk
from ..lib.config import Config
from ..lib.logging import logger
from uuid import uuid4

class EmbeddingGeneratorService:
    """
    Service for generating embeddings using the Cohere API.
    """

    def __init__(self):
        """
        Initialize the embedding generator service with Cohere client.
        """
        if not Config.COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.client = cohere.Client(Config.COHERE_API_KEY)
        self.model = Config.DEFAULT_EMBEDDING_MODEL

    def generate_embeddings(self, chunks: List[TextChunk]) -> List[EmbeddingVector]:
        """
        Generate embeddings for a list of text chunks.

        Args:
            chunks: List of TextChunk objects to generate embeddings for

        Returns:
            List[EmbeddingVector]: List of generated embedding vectors
        """
        if not chunks:
            return []

        # Extract text content from chunks
        texts = [chunk.content for chunk in chunks]

        try:
            # Generate embeddings using Cohere
            response = self.client.embed(
                texts=texts,
                model=self.model,
                input_type="search_document"  # Optimize for search use case
            )

            embeddings = response.embeddings
            embedding_vectors = []

            # Create EmbeddingVector objects from the response
            for i, embedding in enumerate(embeddings):
                chunk = chunks[i]
                embedding_vector = EmbeddingVector(
                    id=str(uuid4()),
                    vector=embedding,
                    chunk_id=chunk.id,
                    model=self.model,
                    dimension=len(embedding)
                )

                # Validate the embedding vector
                if not embedding_vector.validate_vector():
                    logger.warning(f"Generated embedding with invalid dimension for chunk {chunk.id}")

                embedding_vectors.append(embedding_vector)

            logger.info(f"Generated {len(embedding_vectors)} embeddings for {len(chunks)} chunks")
            return embedding_vectors

        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    def generate_embedding_for_single_chunk(self, chunk: TextChunk) -> EmbeddingVector:
        """
        Generate embedding for a single text chunk.

        Args:
            chunk: TextChunk object to generate embedding for

        Returns:
            EmbeddingVector: Generated embedding vector
        """
        try:
            response = self.client.embed(
                texts=[chunk.content],
                model=self.model,
                input_type="search_document"
            )

            embedding = response.embeddings[0]
            embedding_vector = EmbeddingVector(
                id=str(uuid4()),
                vector=embedding,
                chunk_id=chunk.id,
                model=self.model,
                dimension=len(embedding)
            )

            if not embedding_vector.validate_vector():
                logger.warning(f"Generated embedding with invalid dimension for chunk {chunk.id}")

            logger.info(f"Generated embedding for chunk {chunk.id}")
            return embedding_vector

        except Exception as e:
            logger.error(f"Error generating embedding for chunk {chunk.id}: {str(e)}")
            raise

    def batch_generate_embeddings(self, chunks: List[TextChunk], batch_size: int = 96) -> List[EmbeddingVector]:
        """
        Generate embeddings in batches to handle large numbers of chunks efficiently.

        Args:
            chunks: List of TextChunk objects to generate embeddings for
            batch_size: Number of chunks to process in each batch

        Returns:
            List[EmbeddingVector]: List of generated embedding vectors
        """
        all_embeddings = []

        # Process chunks in batches
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            batch_embeddings = self.generate_embeddings(batch)
            all_embeddings.extend(batch_embeddings)

        logger.info(f"Batch generated {len(all_embeddings)} embeddings for {len(chunks)} chunks")
        return all_embeddings

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the embedding model being used.

        Returns:
            Dict[str, Any]: Model information
        """
        # Note: Cohere doesn't have a direct API to get model info
        # This is just a placeholder for model information
        return {
            "model": self.model,
            "dimensions": 768,  # Default for Cohere multilingual model
            "input_type": "search_document"
        }