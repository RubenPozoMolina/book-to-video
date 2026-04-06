# Book to Video Converter

This project allows you to convert a book (EPUB or Markdown format) into a series of videos (one per chapter) suitable for YouTube. It uses local AI models for audio generation and Python libraries for video creation.

## Requirements

- Python 3.12+
- `ffmpeg` installed on your system (required for `moviepy`)
- Python dependencies listed in `requirements.txt`

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure `ffmpeg` is installed:
   - **Ubuntu/Debian**: `sudo apt install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download the binary from [ffmpeg.org](https://ffmpeg.org/) and add it to your PATH.

## Usage

Run the main script providing the path to your EPUB or Markdown book and the desired language (default is 'en'):

```bash
PYTHONPATH=. python scripts/book_to_video.py path/to/your/book.epub --output my_videos --language es
```

Or for a Markdown file:

```bash
PYTHONPATH=. python scripts/book_to_video examples/caracol_aventurero/caracol_aventurero.md --output output/caracol_aventurero --language es
```

### Book to Audio

Si solo deseas generar los archivos de audio (MP3) por capítulos sin generar el video, puedes usar el script especializado:

```bash
PYTHONPATH=. python scripts/book_to_audio.py examples/caracol_aventurero/caracol_aventurero.md --output output --voice es-ES-AlvaroNeural
```

Soporta los siguientes formatos: `.pdf`, `.md`, `.epub`, `.html`.

Opciones principales:
- `--voice`: Voz de Edge TTS (ej. `es-ES-AlvaroNeural`, `en-US-AndrewNeural`). Por defecto usa una voz en español.
- `--local`: Usa `pyttsx3` en lugar de Edge TTS para generación local (offline).
- `--language`: Código de lenguaje si se usa `--local`.

## Architecture

- **OOP Design**: The project follows Object-Oriented principles and Clean Code.
- **Interfaces**: Define the contract for each component (`IBookParser`, `IAudioGenerator`, `IVideoGenerator`).
- **Processors**: Implementations for parsing books (e.g., `EpubParser`, `MarkdownParser`, `PdfParser`, `HtmlParser`).
- **Generators**: Implementations for creating audio (`Pyttsx3AudioGenerator`, `EdgeTTSAudioGenerator`) and video (`SimpleVideoGenerator`).
- **Local/Cloud TTS**: Soporta generación local con `pyttsx3` y voces naturales de Microsoft Edge via `edge-tts`.

## Project Structure

- `src/interfaces/`: Abstract base classes.
- `src/models/`: Data models (Chapter, Book).
- `src/processors/`: Book parsing logic (EPUB, Markdown, PDF, HTML).
- `src/generators/`: Audio and Video generation logic.
- `scripts/book_to_video.py`: Main orchestrator.
- `scripts/book_to_audio.py`: Audio generation script.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
