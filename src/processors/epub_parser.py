import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from typing import List
from src.interfaces.base_interfaces import IBookParser
from src.models.chapter import Chapter

class EpubParser(IBookParser):
    """Implementation of IBookParser for EPUB files."""
    
    def parse(self, source_path: str) -> List[Chapter]:
        """Parses an EPUB file and extracts chapters."""
        book = epub.read_epub(source_path)
        chapters = []
        index = 1
        
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                content = item.get_content().decode('utf-8')
                soup = BeautifulSoup(content, 'html.parser')
                
                # Extract title from h1, h2 or first few words
                title_tag = soup.find(['h1', 'h2', 'h3'])
                title = title_tag.get_text() if title_tag else f"Chapter {index}"
                
                # Extract text content
                text = soup.get_text(separator=' ').strip()
                
                if text:
                    chapters.append(Chapter(
                        title=title,
                        content=text,
                        index=index
                    ))
                    index += 1
                    
        return chapters
