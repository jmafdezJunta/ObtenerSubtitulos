#!/usr/bin/env python3
"""
Script para descargar y procesar subtítulos de videos de YouTube.
Soporta múltiples formatos: vtt, srt, json
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Optional, List
import yt_dlp


class YouTubeSubtitleDownloader:
    def __init__(self, output_dir: str = "downloads"):
        """
        Inicializa el descargador de subtítulos.
        
        Args:
            output_dir: Directorio donde guardar los subtítulos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def download_subtitles(
        self,
        url: str,
        language: str = "es",
        formats: List[str] = None
    ) -> bool:
        """
        Descarga los subtítulos de un video de YouTube.
        
        Args:
            url: URL del video de YouTube
            language: Código de idioma (ej: es, en, fr)
            formats: Lista de formatos a descargar (vtt, srt, json)
        
        Returns:
            True si la descarga fue exitosa, False en caso contrario
        """
        if formats is None:
            formats = ["vtt", "srt", "json"]
        
        # Validar URL
        if not self._validate_url(url):
            print("❌ URL de YouTube inválida")
            return False
        
        try:
            print(f"📥 Descargando subtítulos en idioma: {language}")
            print(f"📁 Guardando en: {self.output_dir.absolute()}")
            
            # Configurar opciones de yt-dlp
            ydl_opts = {
                'skip_download': True,
                'writesubtitles': True,
                'subtitleslangs': [language],
                'subtitlesformat': ','.join(formats),
                'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
            }
            
            # Descargar usando yt-dlp como módulo
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
            print("✅ Subtítulos descargados exitosamente")
            return True
                
        except Exception as e:
            error_msg = str(e)
            if "yt-dlp" in error_msg or "YoutubeDL" in error_msg:
                print("❌ yt-dlp no está instalado correctamente")
                print("   Ejecuta: pip install yt-dlp")
            else:
                print(f"❌ Error: {e}")
            return False
    
    def list_downloads(self) -> None:
        """Lista todos los subtítulos descargados."""
        subtitle_files = list(self.output_dir.glob("*"))
        
        if not subtitle_files:
            print("📭 No hay subtítulos descargados")
            return
        
        print(f"\n📋 Archivos en {self.output_dir}:")
        for idx, file in enumerate(subtitle_files, 1):
            size = file.stat().st_size / 1024  # Tamaño en KB
            print(f"   {idx}. {file.name} ({size:.1f} KB)")
    
    def search_in_subtitles(
        self,
        search_term: str,
        filename: Optional[str] = None
    ) -> None:
        """
        Busca un término en los subtítulos descargados.
        
        Args:
            search_term: Término a buscar
            filename: Nombre del archivo específico (opcional)
        """
        if filename:
            files = [self.output_dir / filename]
        else:
            files = list(self.output_dir.glob("*.vtt")) + list(self.output_dir.glob("*.srt"))
        
        if not files:
            print("⚠️  No hay archivos de subtítulos")
            return
        
        found_count = 0
        print(f"\n🔍 Buscando: '{search_term}'")
        
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                matches = [(i+1, line.strip()) 
                          for i, line in enumerate(lines)
                          if search_term.lower() in line.lower()]
                
                if matches:
                    print(f"\n📄 {file.name}: {len(matches)} coincidencia(s)")
                    for line_num, line in matches[:5]:  # Mostrar los primeros 5
                        print(f"   Línea {line_num}: {line[:80]}")
                    if len(matches) > 5:
                        print(f"   ... y {len(matches) - 5} más")
                    found_count += len(matches)
                    
            except Exception as e:
                print(f"⚠️  Error leyendo {file.name}: {e}")
        
        if found_count == 0:
            print("❌ No se encontraron coincidencias")
    
    def convert_to_json(self, input_file: str, output_file: Optional[str] = None) -> bool:
        """
        Convierte un archivo de subtítulos (vtt/srt) a JSON.
        
        Args:
            input_file: Archivo de entrada
            output_file: Archivo de salida (opcional)
        
        Returns:
            True si la conversión fue exitosa
        """
        input_path = self.output_dir / input_file
        
        if not input_path.exists():
            print(f"❌ Archivo no encontrado: {input_file}")
            return False
        
        if output_file is None:
            output_file = input_path.stem + ".json"
        
        output_path = self.output_dir / output_file
        
        try:
            subtitles = self._parse_subtitles(input_path)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(subtitles, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Convertido a: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    @staticmethod
    def _parse_subtitles(file_path: Path) -> List[dict]:
        """Parsea un archivo de subtítulos (vtt o srt)."""
        subtitles = []
        current_subtitle = {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            
            # Saltar líneas vacías y cabecera
            if not line or line.startswith("WEBVTT"):
                continue
            
            # Detectar timestamps
            if " --> " in line:
                current_subtitle["timestamp"] = line
            elif line and current_subtitle.get("timestamp"):
                if "text" not in current_subtitle:
                    current_subtitle["text"] = line
                else:
                    current_subtitle["text"] += " " + line
            elif line and "timestamp" in current_subtitle:
                subtitles.append(current_subtitle)
                current_subtitle = {}
        
        # Agregar el último subtítulo
        if "timestamp" in current_subtitle:
            subtitles.append(current_subtitle)
        
        return subtitles
    
    @staticmethod
    def _validate_url(url: str) -> bool:
        """Valida que la URL sea de YouTube."""
        return any(domain in url for domain in [
            "youtube.com",
            "youtu.be",
            "m.youtube.com"
        ])


def main():
    parser = argparse.ArgumentParser(
        description="Descargador de subtítulos de YouTube",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python youtube_subtitles.py -u https://youtu.be/tYqehyG2K38
  python youtube_subtitles.py -u https://youtu.be/tYqehyG2K38 -l en -f vtt srt
  python youtube_subtitles.py --list
  python youtube_subtitles.py --search "palabra clave"
  python youtube_subtitles.py --convert subtitles.vtt
        """
    )
    
    parser.add_argument(
        "-u", "--url",
        help="URL del video de YouTube"
    )
    parser.add_argument(
        "-l", "--language",
        default="es",
        help="Código de idioma (default: es)"
    )
    parser.add_argument(
        "-f", "--formats",
        nargs="+",
        default=["vtt", "srt", "json"],
        help="Formatos de salida: vtt, srt, json (default: vtt srt json)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Listar subtítulos descargados"
    )
    parser.add_argument(
        "--search",
        help="Buscar un término en los subtítulos"
    )
    parser.add_argument(
        "--convert",
        help="Convertir archivo de subtítulos a JSON"
    )
    parser.add_argument(
        "-d", "--directory",
        default="downloads",
        help="Directorio de salida (default: downloads)"
    )
    
    args = parser.parse_args()
    
    downloader = YouTubeSubtitleDownloader(args.directory)
    
    # Si no hay argumentos, mostrar ayuda
    if not any([args.url, args.list, args.search, args.convert]):
        parser.print_help()
        return
    
    if args.url:
        downloader.download_subtitles(args.url, args.language, args.formats)
    
    if args.list:
        downloader.list_downloads()
    
    if args.search:
        downloader.search_in_subtitles(args.search)
    
    if args.convert:
        downloader.convert_to_json(args.convert)


if __name__ == "__main__":
    main()
