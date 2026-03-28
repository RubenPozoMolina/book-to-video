import pyttsx3
import os
from src.interfaces.base_interfaces import IAudioGenerator

class Pyttsx3AudioGenerator(IAudioGenerator):
    """Implementation of IAudioGenerator using pyttsx3 (local TTS)."""
    
    def __init__(self, rate: int = 150, volume: float = 1.0):
        self.rate = rate
        self.volume = volume

    def generate_audio(self, text: str, output_path: str) -> str:
        """Generates an MP3 file from the given text."""
        engine = pyttsx3.init()
        engine.setProperty('rate', self.rate)
        engine.setProperty('volume', self.volume)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        
        return output_path
