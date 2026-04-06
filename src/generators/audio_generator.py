import pyttsx3
import os
import asyncio
import edge_tts
from src.interfaces.base_interfaces import IAudioGenerator

class EdgeTTSAudioGenerator(IAudioGenerator):
    """Implementation of IAudioGenerator using edge-tts (Microsoft Edge Online TTS)."""
    
    def __init__(self, voice: str = "en-US-AndrewNeural"):
        self.voice = voice

    def generate_audio(self, text: str, output_path: str) -> str:
        """Generates an MP3 file using edge-tts (asynchronous wrapper)."""
        asyncio.run(self._generate(text, output_path))
        return output_path

    async def _generate(self, text: str, output_path: str):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)

class Pyttsx3AudioGenerator(IAudioGenerator):
    """Implementation of IAudioGenerator using pyttsx3 (local TTS)."""
    
    def __init__(self, rate: int = 150, volume: float = 1.0, language: str = 'en'):
        self.rate = rate
        self.volume = volume
        self.language = language
        self._engine = None

    def _get_engine(self):
        """Lazy initialization of the pyttsx3 engine to keep it alive."""
        if self._engine is None:
            self._engine = pyttsx3.init()
            self._engine.setProperty('rate', self.rate)
            self._engine.setProperty('volume', self.volume)
            self._set_voice()
        return self._engine

    def _set_voice(self):
        """Sets the voice based on the requested language."""
        voices = self._engine.getProperty('voices')
        # Try to find a voice that matches the language code
        for voice in voices:
            if any(self.language.lower() in lang.lower() for lang in voice.languages):
                self._engine.setProperty('voice', voice.id)
                return
        
        # Fallback to a partial match if no exact match (e.g. 'es' in 'es-419')
        for voice in voices:
            for lang in voice.languages:
                if self.language.lower() in lang.lower() or lang.lower() in self.language.lower():
                    self._engine.setProperty('voice', voice.id)
                    return

    def generate_audio(self, text: str, output_path: str) -> str:
        """Generates an MP3 file from the given text."""
        engine = self._get_engine()
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Remove output file if it exists to avoid conflicts
        if os.path.exists(output_path):
            os.remove(output_path)
            
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        
        # Give some time for the OS to finalize the file
        import time
        for _ in range(10):
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                break
            time.sleep(1.0)

        # Verify file creation
        if not os.path.exists(output_path):
            # Some pyttsx3 drivers might change the extension (e.g., .mp3 -> .wav)
            # or fail silently. Let's check for common ones.
            base_path = os.path.splitext(output_path)[0]
            for ext in ['.wav', '.mp3', '.aiff']:
                if os.path.exists(base_path + ext):
                    return base_path + ext
            raise FileNotFoundError(f"pyttsx3 failed to generate audio file at {output_path}")
            
        return output_path

    def stop(self):
        """Properly stops the engine if it exists."""
        if self._engine is not None:
            self._engine.stop()
            self._engine = None
