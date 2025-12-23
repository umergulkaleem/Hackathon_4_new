from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from .config import Config
import logging

logger = logging.getLogger(__name__)

def get_qdrant_client() -> QdrantClient:
    """
    Create and return a Qdrant client instance based on configuration.

    Returns:
        QdrantClient: Configured Qdrant client instance
    """
    if Config.QDRANT_API_KEY:
        client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY,
        )
    else:
        client = QdrantClient(
            url=Config.QDRANT_URL,
        )

    logger.info(f"Qdrant client initialized with URL: {Config.QDRANT_URL}")
    return client

def create_embeddings_collection(
    client: QdrantClient,
    collection_name: str,
    vector_size: int = 768  # Default size for Cohere embeddings
) -> bool:
    """
    Create a collection in Qdrant for storing embeddings.

    Args:
        client: Qdrant client instance
        collection_name: Name of the collection to create
        vector_size: Size of the embedding vectors

    Returns:
        bool: True if collection was created or already exists
    """
    try:
        # Check if collection already exists
        collections = client.get_collections()
        existing_collection_names = [c.name for c in collections.collections]

        if collection_name in existing_collection_names:
            logger.info(f"Collection '{collection_name}' already exists")
            return True

        # Create new collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE
            )
        )

        logger.info(f"Created collection '{collection_name}' with vector size {vector_size}")
        return True

    except Exception as e:
        logger.error(f"Failed to create collection '{collection_name}': {str(e)}")
        raise

def validate_environment() -> bool:
    """
    Validate that all required environment variables are set.

    Returns:
        bool: True if all required environment variables are set
    """
    required_vars = ["COHERE_API_KEY"]

    for var in required_vars:
        if not getattr(Config, var):
            raise ValueError(f"Required environment variable {var} is not set")

    return True