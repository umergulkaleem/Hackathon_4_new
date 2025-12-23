from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TextChunk(BaseModel):
    """
    Represents semantically coherent segments of text extracted from Markdown content, with metadata linking to source.
    """
    id: str
    content: str
    chunk_index: int
    source_document_id: str
    headers_context: List[str] = []
    word_count: int = 0
    char_count: int = 0
    created_at: datetime = datetime.now()

    def calculate_counts(self):
        """Calculate word and character counts for the chunk."""
        self.word_count = len(self.content.split())
        self.char_count = len(self.content)