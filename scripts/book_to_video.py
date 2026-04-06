import os
import argparse
from tqdm import tqdm
from src.processors.epub_parser import EpubParser
from src.processors.markdown_parser import MarkdownParser
from src.generators.audio_generator import Pyttsx3AudioGenerator
from src.generators.video_generator import SimpleVideoGenerator

class BookToVideoOrchestrator:
    """Orchestrates the process of converting a book into videos (one per chapter)."""
    
    def __init__(self, parser, audio_gen, video_gen, output_dir="output"):
        self.parser = parser
        self.audio_gen = audio_gen
        self.video_gen = video_gen
        self.output_dir = output_dir

    def run(self, book_path: str):
        """Converts the whole book into a set of videos."""
        print(f"[*] Parsing book: {book_path}")
        chapters = self.parser.parse(book_path)
        print(f"[*] Found {len(chapters)} chapters.")

        # Ensure output directories exist
        os.makedirs(os.path.join(self.output_dir, "audio"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "video"), exist_ok=True)

        for chapter in tqdm(chapters, desc="Processing Chapters"):
            # 1. Generate Audio
            audio_filename = f"chapter_{chapter.index}_audio.mp3"
            audio_path = os.path.join(self.output_dir, "audio", audio_filename)
            print(f"\n[+] Generating audio for: {chapter.title}")
            chapter.audio_path = self.audio_gen.generate_audio(chapter.content, audio_path)

            # 2. Generate Video
            video_filename = f"chapter_{chapter.index}_video.mp4"
            video_path = os.path.join(self.output_dir, "video", video_filename)
            visual_data = {"title": chapter.title}
            print(f"[+] Generating video for: {chapter.title}")
            chapter.video_path = self.video_gen.create_video(
                chapter.audio_path, 
                visual_data, 
                video_path
            )

        print(f"[*] Done! Videos are in {os.path.join(self.output_dir, 'video')}")

def main():
    parser = argparse.ArgumentParser(description="Convert an EPUB or Markdown book to chapter-wise YouTube videos.")
    parser.add_argument("input", help="Path to the EPUB or Markdown file")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--language", "-l", default="en", help="Language code for TTS (e.g., 'en', 'es')")
    args = parser.parse_args()

    # Initialize components
    if args.input.lower().endswith(('.md', '.markdown')):
        book_parser = MarkdownParser()
    else:
        book_parser = EpubParser()
    
    audio_generator = Pyttsx3AudioGenerator(rate=150, language=args.language)
    video_generator = SimpleVideoGenerator()

    # Run orchestrator
    orchestrator = BookToVideoOrchestrator(
        book_parser, 
        audio_generator, 
        video_generator, 
        output_dir=args.output
    )
    try:
        orchestrator.run(args.input)
    finally:
        if hasattr(audio_generator, 'stop'):
            audio_generator.stop()

if __name__ == "__main__":
    main()
