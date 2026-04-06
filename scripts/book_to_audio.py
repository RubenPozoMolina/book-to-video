import os
import argparse
from tqdm import tqdm
from src.processors.epub_parser import EpubParser
from src.processors.markdown_parser import MarkdownParser
from src.processors.html_parser import HtmlParser
from src.processors.pdf_parser import PdfParser
from src.generators.audio_generator import EdgeTTSAudioGenerator, Pyttsx3AudioGenerator

class BookToAudioOrchestrator:
    """Orchestrates the process of converting a book into audio files (one per chapter)."""
    
    def __init__(self, parser, audio_gen, output_dir="output"):
        self.parser = parser
        self.audio_gen = audio_gen
        self.output_dir = output_dir

    def run(self, book_path: str):
        """Converts the whole book into a set of audio files."""
        print(f"[*] Parsing book: {book_path}")
        chapters = self.parser.parse(book_path)
        print(f"[*] Found {len(chapters)} chapters.")

        # Ensure output directory exists
        audio_output_dir = os.path.join(self.output_dir, "audio")
        os.makedirs(audio_output_dir, exist_ok=True)

        for chapter in tqdm(chapters, desc="Generating Audio"):
            # Generate Audio
            audio_filename = f"chapter_{chapter.index}_{chapter.title.replace(' ', '_')}.mp3"
            # Sanitize filename
            audio_filename = "".join([c for c in audio_filename if c.isalnum() or c in (' ', '.', '_')]).strip()
            audio_path = os.path.join(audio_output_dir, audio_filename)
            
            print(f"\n[+] Generating audio for: {chapter.title}")
            chapter.audio_path = self.audio_gen.generate_audio(chapter.content, audio_path)

        print(f"[*] Done! Audio files are in {audio_output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Convert PDF, Markdown, EPUB or HTML books to audio files.")
    parser.add_argument("input", help="Path to the book file (pdf, md, epub, html)")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--voice", default="es-ES-AlvaroNeural", help="Edge TTS Voice (e.g. 'es-ES-AlvaroNeural', 'en-US-AndrewNeural')")
    parser.add_argument("--local", action="store_true", help="Use local pyttsx3 instead of Edge TTS")
    parser.add_argument("--language", default="es", help="Language code for pyttsx3 (only if --local is used)")
    
    args = parser.parse_args()

    # Select parser based on file extension
    ext = os.path.splitext(args.input)[1].lower()
    if ext in ('.md', '.markdown'):
        book_parser = MarkdownParser()
    elif ext in ('.epub',):
        book_parser = EpubParser()
    elif ext in ('.html', '.htm'):
        book_parser = HtmlParser()
    elif ext in ('.pdf',):
        book_parser = PdfParser()
    else:
        print(f"[-] Unsupported file extension: {ext}")
        return

    # Select audio generator
    if args.local:
        audio_generator = Pyttsx3AudioGenerator(rate=150, language=args.language)
    else:
        audio_generator = EdgeTTSAudioGenerator(voice=args.voice)

    # Run orchestrator
    orchestrator = BookToAudioOrchestrator(
        book_parser, 
        audio_generator, 
        output_dir=args.output
    )
    
    try:
        orchestrator.run(args.input)
    finally:
        if hasattr(audio_generator, 'stop'):
            audio_generator.stop()

if __name__ == "__main__":
    main()
