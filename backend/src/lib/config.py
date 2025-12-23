import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration management for the markdown embeddings service."""

    # Cohere configuration
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")

    # Qdrant configuration
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")

    # Processing configuration
    DEFAULT_CHUNK_SIZE: int = int(os.getenv("DEFAULT_CHUNK_SIZE", "1000"))
    DEFAULT_CHUNK_OVERLAP: int = int(os.getenv("DEFAULT_CHUNK_OVERLAP", "200"))
    DEFAULT_EMBEDDING_MODEL: str = os.getenv("DEFAULT_EMBEDDING_MODEL", "embed-multilingual-v2.0")

    # Validation
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY environment variable is required")
        return True