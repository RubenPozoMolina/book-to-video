from pydantic import BaseModel
from typing import List, Optional

class Chapter(BaseModel):
    """Represents a single chapter of a book."""
    title: str
    content: str
    index: int
    audio_path: Optional[str] = None
    video_path: Optional[str] = None

class Book(BaseModel):
    """Represents a book with multiple chapters."""
    title: str
    chapters: List[Chapter]
    author: Optional[str] = None
