from pydantic import BaseModel
from typing import List, Optional

class Metadata(BaseModel):
    """
    Contains information linking embeddings back to source files, including file paths, document structure, and content hierarchy.
    """
    source_file: str
    document_title: Optional[str] = None
    chunk_index: int = 0
    headers_hierarchy: str = ""
    word_count: int = 0
    content_type: str = "text"
    retrieval_score: Optional[float] = None

    def to_payload(self) -> dict:
        """Convert metadata to a payload suitable for Qdrant storage."""
        return {
            "source_file": self.source_file,
            "document_title": self.document_title,
            "chunk_index": self.chunk_index,
            "headers_hierarchy": self.headers_hierarchy,
            "word_count": self.word_count,
            "content_type": self.content_type,
            "retrieval_score": self.retrieval_score
        }

    @classmethod
    def from_payload(cls, payload: dict) -> 'Metadata':
        """Create a Metadata instance from a Qdrant payload."""
        return cls(
            source_file=payload.get("source_file", ""),
            document_title=payload.get("document_title"),
            chunk_index=payload.get("chunk_index", 0),
            headers_hierarchy=payload.get("headers_hierarchy", ""),
            word_count=payload.get("word_count", 0),
            content_type=payload.get("content_type", "text"),
            retrieval_score=payload.get("retrieval_score")
        )