import os
import requests
import random
from pathlib import Path
from pydantic import Field
from tools.common.messenger import Messenger
from tools.common.base_model import BaseModelTool
from typing import Optional

class PexelsTool(BaseModelTool):
    """
    Herramienta para interactuar con la API de Pexels y descargar videos de stock gratuitos.
    """
    api_key: Optional[str] = Field(default_factory=lambda: os.getenv("PEXELS_API_KEY"))

    def fetch_video(self, query: str, out_path: Path) -> bool:
        """
        Busca un video vertical basado en el query y lo descarga.
        Retorna True si fue exitoso, False en caso contrario.
        """
        if not self.api_key:
            Messenger.warning("⚠️ No se encontró PEXELS_API_KEY en el entorno. Saltando Pexels.")
            return False

        if not query or not query.strip():
            Messenger.warning("⚠️ Query de Pexels vacío. Saltando búsqueda.")
            return False

        clean_query = query.strip()
        Messenger.info(f"🔎 Buscando video en Pexels para: '{clean_query}'...")
        url = "https://api.pexels.com/videos/search"
        headers = {"Authorization": self.api_key}
        
        # Intentos progresivos: 1) Portrait específico, 2) Sin restricción estricta de size, 3) Orientación general
        search_attempts = [
            {"query": clean_query, "orientation": "portrait", "per_page": 15, "page": random.randint(1, 2), "size": "large"},
            {"query": clean_query, "orientation": "portrait", "per_page": 15, "page": 1},
            {"query": clean_query, "per_page": 15, "page": 1},
        ]
        
        # Si la consulta tiene varias palabras, agregar fallback con las 2 primeras palabras
        words = clean_query.split()
        if len(words) > 2:
            search_attempts.append({"query": " ".join(words[:2]), "orientation": "portrait", "per_page": 15, "page": 1})
            search_attempts.append({"query": words[0], "per_page": 15, "page": 1})

        videos = []
        for attempt_params in search_attempts:
            try:
                response = requests.get(url, headers=headers, params=attempt_params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    vids = data.get("videos", [])
                    if vids:
                        videos = vids
                        break
            except Exception:
                continue

        if not videos:
            Messenger.warning(f"⚠️ No se encontraron videos para '{clean_query}' en Pexels.")
            return False

        try:
            # Elegir uno al azar de la lista
            selected_video = random.choice(videos)
            video_files = selected_video.get("video_files", [])
            if not video_files:
                return False
                
            # Buscar el archivo de video de mejor calidad (vertical o HD)
            best_file = None
            for f in video_files:
                if f.get("quality") == "hd" and f.get("width") and f.get("height") and f.get("height") > f.get("width"):
                    best_file = f
                    break
            
            # Si no hay hd vertical, buscar cualquier archivo vertical
            if not best_file:
                for f in video_files:
                    if f.get("width") and f.get("height") and f.get("height") > f.get("width"):
                        best_file = f
                        break
            
            # Fallback a cualquiera de buena resolucion
            if not best_file:
                best_file = video_files[0]
                
            download_link = best_file.get("link")
            if not download_link:
                return False

            Messenger.info(f"⬇️ Descargando video de Pexels ({selected_video.get('duration', 0)}s)...")
            vid_res = requests.get(download_link, stream=True, timeout=20)
            vid_res.raise_for_status()
            
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "wb") as f:
                for chunk in vid_res.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            if out_path.exists() and out_path.stat().st_size > 10240:
                Messenger.success(f"✅ Video descargado con éxito: {out_path.name}")
                return True
            return False

        except Exception as e:
            Messenger.error(f"❌ Error al descargar video de Pexels: {e}")
            return False

    def fetch_photo(self, query: str, out_path: Path) -> bool:
        """
        Descarga una foto vertical de alta resolución desde Pexels Photo API.
        Sirve como respaldo inmediato y de alta calidad cuando no hay clips de video disponibles.
        """
        if not self.api_key or not query or not query.strip():
            return False

        clean_query = query.strip()
        Messenger.info(f"🔎 Buscando foto de respaldo en Pexels para: '{clean_query}'...")
        url = "https://api.pexels.com/v1/search"
        headers = {"Authorization": self.api_key}

        attempts = [
            {"query": clean_query, "orientation": "portrait", "per_page": 15, "page": 1},
            {"query": clean_query, "per_page": 15, "page": 1},
        ]
        words = clean_query.split()
        if len(words) > 2:
            attempts.append({"query": " ".join(words[:2]), "per_page": 15, "page": 1})

        photos = []
        for params in attempts:
            try:
                res = requests.get(url, headers=headers, params=params, timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    p_list = data.get("photos", [])
                    if p_list:
                        photos = p_list
                        break
            except Exception:
                continue

        if not photos:
            return False

        try:
            chosen = random.choice(photos)
            src = chosen.get("src", {})
            img_url = src.get("large2x") or src.get("large") or src.get("original")
            if not img_url:
                return False

            img_res = requests.get(img_url, timeout=15)
            img_res.raise_for_status()

            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "wb") as f:
                f.write(img_res.content)

            if out_path.exists() and out_path.stat().st_size > 5120:
                Messenger.success(f"✅ Foto de respaldo Pexels guardada: {out_path.name}")
                return True
            return False
        except Exception as e:
            Messenger.warning(f"⚠️ Error al descargar foto de Pexels: {e}")
            return False
