import os
import requests
import random
from pathlib import Path
from pydantic import Field
from tools.common.messenger import Messenger
from tools.common.base_model import BaseModelTool
from typing import Optional

class PixabayTool(BaseModelTool):
    """
    Herramienta para interactuar con la API de Pixabay y descargar videos de stock gratuitos.
    """
    api_key: Optional[str] = Field(default_factory=lambda: os.getenv("PIXABAY_API_KEY"))

    def fetch_video(self, query: str, out_path: Path) -> bool:
        """
        Busca un video basado en el query y lo descarga.
        Retorna True si fue exitoso, False en caso contrario.
        """
        if not self.api_key:
            Messenger.warning("⚠️ No se encontró PIXABAY_API_KEY en el entorno. Saltando Pixabay.")
            return False

        if not query or not query.strip():
            Messenger.warning("⚠️ Query de Pixabay vacío. Saltando búsqueda.")
            return False

        clean_query = query.strip()
        Messenger.info(f"🔎 Buscando video en Pixabay para: '{clean_query}'...")
        
        url = "https://pixabay.com/api/videos/"
        
        # Intentos progresivos: 1) Consulta original, 2) Primeras 2 palabras, 3) Primera palabra clave
        words = clean_query.split()
        attempts = [clean_query]
        if len(words) > 2:
            attempts.append(" ".join(words[:2]))
            attempts.append(words[0])
        elif len(words) == 2:
            attempts.append(words[0])

        hits = []
        for q in attempts:
            formatted_q = q.replace(" ", "+")
            params = {
                "key": self.api_key,
                "q": formatted_q,
                "video_type": "film",
                "per_page": 15,
                "page": 1,
                "safesearch": "true"
            }
            try:
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    h = data.get("hits", [])
                    if h:
                        hits = h
                        break
            except Exception:
                continue

        if not hits:
            Messenger.warning(f"⚠️ No se encontraron videos para '{clean_query}' en Pixabay.")
            return False

        try:
            # Elegir uno al azar de la lista completa (hasta 15 opciones diferentes)
            selected_video = random.choice(hits)
            videos_data = selected_video.get("videos", {})
            if not videos_data:
                return False
                
            # Preferimos la versión 'large' (HD) y luego 'medium'
            best_video_obj = videos_data.get("large")
            if not best_video_obj or not best_video_obj.get("url"):
                best_video_obj = videos_data.get("medium")
                
            if not best_video_obj or not best_video_obj.get("url"):
                best_video_obj = list(videos_data.values())[0]

            download_link = best_video_obj.get("url")
            if not download_link:
                return False

            Messenger.info(f"⬇️ Descargando video de Pixabay ({selected_video.get('duration', 0)}s)...")
            vid_res = requests.get(download_link, stream=True, timeout=20)
            vid_res.raise_for_status()
            
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "wb") as f:
                for chunk in vid_res.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            if out_path.exists() and out_path.stat().st_size > 10240:
                Messenger.success(f"✅ Video descargado con éxito de Pixabay: {out_path.name}")
                return True
            return False

        except Exception as e:
            Messenger.error(f"❌ Error al consultar/descargar de Pixabay API: {e}")
            return False

    def fetch_photo(self, query: str, out_path: Path) -> bool:
        """
        Descarga una foto en HD desde Pixabay Image API como respaldo infalible.
        """
        if not self.api_key or not query or not query.strip():
            return False

        clean_query = query.strip()
        Messenger.info(f"🔎 Buscando foto de respaldo en Pixabay para: '{clean_query}'...")
        url = "https://pixabay.com/api/"

        words = clean_query.split()
        attempts = [clean_query]
        if len(words) > 2:
            attempts.append(" ".join(words[:2]))
            attempts.append(words[0])

        hits = []
        for q in attempts:
            params = {
                "key": self.api_key,
                "q": q.replace(" ", "+"),
                "image_type": "photo",
                "orientation": "vertical",
                "per_page": 15,
                "page": 1,
                "safesearch": "true"
            }
            try:
                res = requests.get(url, params=params, timeout=10)
                if res.status_code == 200:
                    h = res.json().get("hits", [])
                    if h:
                        hits = h
                        break
            except Exception:
                continue

        if not hits:
            return False

        try:
            chosen = random.choice(hits)
            img_url = chosen.get("largeImageURL") or chosen.get("webformatURL")
            if not img_url:
                return False

            img_res = requests.get(img_url, timeout=15)
            img_res.raise_for_status()

            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "wb") as f:
                f.write(img_res.content)

            if out_path.exists() and out_path.stat().st_size > 5120:
                Messenger.success(f"✅ Foto de respaldo Pixabay guardada: {out_path.name}")
                return True
            return False
        except Exception as e:
            Messenger.warning(f"⚠️ Error al descargar foto de Pixabay: {e}")
            return False
