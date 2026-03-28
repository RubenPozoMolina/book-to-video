# Book to Video Converter

Este proyecto permite convertir un libro (formato EPUB) en una serie de vídeos (uno por capítulo) adecuados para YouTube. Utiliza modelos de IA locales para la generación de audio y librerías de Python para la creación de vídeo.

## Requisitos

- Python 3.12+
- `ffmpeg` instalado en el sistema (requerido por `moviepy`)
- Dependencias de Python listadas en `requirements.txt` o instaladas vía `pip`

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/RubenPozoMolina/book-to-video.git
cd book-to-video
```

### 2. Instalar dependencias
Puedes instalar las dependencias directamente:
```bash
pip install -r requirements.txt
```
O instalar el proyecto en modo editable:
```bash
pip install -e .
```

### 3. Asegurar que `ffmpeg` esté instalado
- **Ubuntu/Debian**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Descarga el binario desde [ffmpeg.org](https://ffmpeg.org/) y añádelo al PATH.

## Uso

Si has instalado el proyecto con `pip install -e .`, puedes usar el comando directamente:
```bash
book-to-video path/to/your/book.epub --output my_videos
```

De lo contrario, ejecuta el script principal:
```bash
python -m src.book_to_video path/to/your/book.epub --output my_videos
```

## Arquitectura

- **Diseño OOP**: El proyecto sigue los principios de Orientación a Objetos y Clean Code.
- **Interfaces**: Definen el contrato para cada componente (`IBookParser`, `IAudioGenerator`, `IVideoGenerator`).
- **Procesadores**: Implementaciones para parsear libros (ej. `EpubParser`).
- **Generadores**: Implementaciones para crear audio (`Pyttsx3AudioGenerator`) y vídeo (`SimpleVideoGenerator`).
- **IA Local**: Actualmente utiliza `pyttsx3` para texto a voz local. Se puede extender para usar Coqui TTS u otros modelos locales implementando la interfaz `IAudioGenerator`.

## Contribución

¡Las contribuciones son bienvenidas!
1. Haz un Fork del proyecto.
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`).
3. Haz commit de tus cambios (`git commit -m 'Añadir nueva característica'`).
4. Haz Push a la rama (`git push origin feature/nueva-caracteristica`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
