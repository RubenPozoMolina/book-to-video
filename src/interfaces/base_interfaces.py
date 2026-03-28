from abc import ABC, abstractmethod
from typing import List, Any
from src.models.chapter import Chapter

class IBookParser(ABC):
    """Interface for parsing a book into chapters."""
    @abstractmethod
    def parse(self, source_path: str) -> List[Chapter]:
        """Parses the input book file into a list of Chapter objects."""
        pass

class ITextProcessor(ABC):
    """Interface for processing raw text into narration scripts or prompts."""
    @abstractmethod
    def process_text(self, text: str) -> str:
        """Processes the input text (e.g., cleaning, summarizing, or formatting)."""
        pass

class IAudioGenerator(ABC):
    """Interface for generating audio from text using local AI models."""
    @abstractmethod
    def generate_audio(self, text: str, output_path: str) -> str:
        """Generates audio file from text and returns the path to the file."""
        pass

class IVideoGenerator(ABC):
    """Interface for generating video from audio and visual elements."""
    @abstractmethod
    def create_video(self, audio_path: str, visual_data: Any, output_path: str) -> str:
        """Creates a video file using audio and visual components."""
        pass
