# YouTube Subtitles Downloader 🎬

Script Python para descargar y procesar subtítulos de videos de YouTube fácilmente.

## Características ✨

- 📥 Descarga subtítulos en múltiples idiomas
- 📁 Soporta varios formatos: VTT, SRT, JSON
- 🔍 Búsqueda de términos dentro de los subtítulos
- 🔄 Conversión entre formatos
- 📋 Listado de archivos descargados
- 🌍 Compatible con cualquier idioma disponible en YouTube

## Instalación 🚀

### Requisitos
- Python 3.7+
- pip

### Pasos

1. Clonar o descargar este repositorio
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Uso 📖

### Descargar subtítulos básico

```bash
python youtube_subtitles.py -u https://youtu.be/tYqehyG2K38
```

Esto descargará los subtítulos en castellano (idioma por defecto) en formatos VTT, SRT y JSON.

### Descargar en otro idioma

```bash
python youtube_subtitles.py -u https://youtu.be/tYqehyG2K38 -l en
```

Códigos de idioma comunes:
- `es` - Español
- `en` - Inglés
- `fr` - Francés
- `de` - Alemán
- `it` - Italiano
- `pt` - Portugués
- `ja` - Japonés
- `zh` - Chino

### Especificar formatos

```bash
python youtube_subtitles.py -u https://youtu.be/tYqehyG2K38 -f vtt srt
```

### Listar subtítulos descargados

```bash
python youtube_subtitles.py --list
```

### Buscar un término en los subtítulos

```bash
python youtube_subtitles.py --search "palabra clave"
```

### Convertir a JSON

```bash
python youtube_subtitles.py --convert nombre_archivo.vtt
```

## Ejemplos completos

```bash
# Descargar en inglés solo en formato VTT
python youtube_subtitles.py -u https://youtu.be/tYqehyG2K38 -l en -f vtt

# Buscar "tutorial" en todos los subtítulos descargados
python youtube_subtitles.py --search "tutorial"

# Convertir SRT a JSON
python youtube_subtitles.py --convert subtitles.srt

# Usar directorio personalizado
python youtube_subtitles.py -u https://youtu.be/tYqehyG2K38 -d mi_carpeta
```

## Estructura de carpetas

```
.
├── youtube_subtitles.py      # Script principal
├── requirements.txt           # Dependencias
├── README.md                 # Este archivo
├── .gitignore               # Archivos ignorados por git
└── downloads/               # Carpeta con subtítulos descargados
```

## Formatos de salida

### VTT (WebVTT)
Formato estándar para subtítulos en web. Incluye timestamps y formato legible.

### SRT (SubRip)
Formato compatible con la mayoría de reproductores de video.

### JSON
Formato estructurado para procesamiento programático.

## Solución de problemas 🔧

### Error: "yt-dlp no está instalado"

```bash
pip install yt-dlp
```

### Error: "URL de YouTube inválida"

Asegúrate de usar una URL válida de YouTube:
- ✅ `https://youtu.be/VIDEO_ID`
- ✅ `https://www.youtube.com/watch?v=VIDEO_ID`
- ❌ `youtube.com/watch?v=VIDEO_ID` (sin https)

### No encuentra subtítulos

El video podría no tener subtítulos en el idioma solicitado. Prueba con otro idioma.

## Licencia 📄

MIT License

## Autor

Script creado para extraer y procesar subtítulos de YouTube de manera fácil y eficiente.
