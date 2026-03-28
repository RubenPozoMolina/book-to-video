import os
from typing import List, Dict, Any
from moviepy import (
    TextClip, AudioFileClip, ColorClip, CompositeVideoClip, 
    concatenate_videoclips
)
from src.interfaces.base_interfaces import IVideoGenerator

class SimpleVideoGenerator(IVideoGenerator):
    """
    Implementation of IVideoGenerator that creates a simple video 
    with a background color and the chapter title.
    """
    
    def __init__(self, size: tuple = (1920, 1080), bg_color: str = 'black', font_size: int = 70):
        self.size = size
        self.bg_color = bg_color
        self.font_size = font_size

    def create_video(self, audio_path: str, visual_data: Dict[str, Any], output_path: str) -> str:
        """
        Creates a video chapter with the title displayed while audio plays.
        visual_data: should contain 'title'.
        """
        title_text = visual_data.get('title', 'Chapter')
        
        # Load audio to get duration
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        # Create background
        bg_clip = ColorClip(size=self.size, color=(0,0,0), duration=duration)
        
        # Create text clip
        # Note: MoviePy v2+ uses slightly different parameters for TextClip
        # We assume common font availability like 'Arial' or 'DejaVuSans'
        try:
            text_clip = TextClip(
                text=title_text, 
                font="Arial", 
                font_size=self.font_size, 
                color="white",
                size=self.size,
                method='caption'
            ).with_duration(duration).with_position('center')
        except Exception:
            # Fallback if font or method fails
            text_clip = TextClip(
                text=title_text, 
                font_size=self.font_size, 
                color="white",
                size=self.size,
                method='label'
            ).with_duration(duration).with_position('center')

        # Combine background and text
        video = CompositeVideoClip([bg_clip, text_clip])
        video = video.with_audio(audio)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write file
        video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
        
        return output_path
