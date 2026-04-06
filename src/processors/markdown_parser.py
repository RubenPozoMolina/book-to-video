import os
from typing import List
from src.interfaces.base_interfaces import IBookParser
from src.models.chapter import Chapter

class MarkdownParser(IBookParser):
    """
    Implementation of IBookParser for Markdown files.
    Treats the first H1/H2 as the book title and subsequent H2/H3 as chapters.
    If no headings are found, treats the entire file as a single chapter.
    """
    
    def parse(self, source_path: str) -> List[Chapter]:
        """Parses a Markdown file and extracts chapters."""
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Markdown file not found: {source_path}")

        with open(source_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        chapters = []
        current_title = "Book Title"
        current_content = []
        index = 1
        book_title_found = False

        for line in lines:
            stripped_line = line.strip()
            # Check for H1 as book title or H2 as chapter headers
            if stripped_line.startswith('# ') and not book_title_found:
                current_title = stripped_line.replace('# ', '').strip()
                book_title_found = True
                continue
            
            if stripped_line.startswith('## '):
                # Save previous chapter if it has content
                if current_content:
                    chapters.append(Chapter(
                        title=current_title,
                        content="\n".join(current_content).strip(),
                        index=index
                    ))
                    index += 1
                
                current_title = stripped_line.replace('## ', '').strip()
                current_content = []
            elif stripped_line.startswith('# '):
                # Another H1, treat as new chapter if we already have content
                if current_content:
                    chapters.append(Chapter(
                        title=current_title,
                        content="\n".join(current_content).strip(),
                        index=index
                    ))
                    index += 1
                
                current_title = stripped_line.replace('# ', '').strip()
                current_content = []
            else:
                current_content.append(line.rstrip())

        # Add the last chapter
        if current_content or current_title:
            chapters.append(Chapter(
                title=current_title,
                content="\n".join(current_content).strip(),
                index=index
            ))

        # Filter out empty chapters
        return [c for c in chapters if c.content]
