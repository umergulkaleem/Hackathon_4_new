from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MarkdownContent(BaseModel):
    """
    Represents the source Docusaurus-generated Markdown files with chapters, sections, headings, and paragraphs.
    """
    id: str
    file_path: str
    content: str
    title: Optional[str] = None
    headers: List[str] = []
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def get_word_count(self) -> int:
        """Calculate the word count of the content."""
        return len(self.content.split())

    def get_char_count(self) -> int:
        """Calculate the character count of the content."""
        return len(self.content)