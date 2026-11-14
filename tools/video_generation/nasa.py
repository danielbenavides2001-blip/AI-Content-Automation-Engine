import requests
from pathlib import Path
from pydantic import Field
from tools.common.messenger import Messenger
from tools.common.base_model import BaseModelTool
from typing import Optional

class NASATool(BaseModelTool):
    """
    Herramienta para buscar y descargar metraje de video y fotos de alta resolución
    de la NASA Image and Video Library (100% de dominio público y gratuito).
    """
    base_url: str = "https://images-api.nasa.gov/search"

    def fetch_video(self, query: str, out_path: Path) -> bool:
        """
        Busca un video en NASA API y descarga la versión MP4 óptima.
        Retorna True si fue exitoso, False en caso contrario.
        """
        if not query or not query.strip():
            return False

        clean_query = query.strip()
        Messenger.info(f"🚀 [NASA API] Buscando metraje de video para: '{clean_query}'...")

        try:
            params = {
                "q": clean_query,
                "media_type": "video"
            }
            resp = requests.get(self.base_url, params=params, timeout=12)
            if resp.status_code != 200:
                Messenger.warning(f"⚠️ NASA API respondió con status {resp.status_code}")
                return False

            items = resp.json().get("collection", {}).get("items", [])
            if not items:
                Messenger.info(f"ℹ️ No se encontraron videos en NASA para '{clean_query}'.")
                return False

            # Intentar con los primeros 3 resultados
            for item in items[:3]:
                collection_href = item.get("href")
                if not collection_href:
                    continue

                asset_resp = requests.get(collection_href, timeout=10)
                if asset_resp.status_code != 200:
                    continue

                asset_urls = asset_resp.json()
                # Priorizar mp4 en resolución adecuada (medium o preview o orig)
                mp4s = [u for u in asset_urls if isinstance(u, str) and u.endswith(".mp4")]
                if not mp4s:
                    continue

                best_url = None
                for candidate in ["~medium.mp4", "~orig.mp4", "~small.mp4", ".mp4"]:
                    match = next((u for u in mp4s if candidate in u), None)
                    if match:
                        best_url = match
                        break

                if not best_url:
                    best_url = mp4s[0]

                # Reemplazar http por https si aplica
                if best_url.startswith("http://"):
                    best_url = "https://" + best_url[7:]

                Messenger.info(f"⬇️ Descargando video de NASA: {best_url}")
                vid_data = requests.get(best_url, timeout=30, stream=True)
                if vid_data.status_code == 200:
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(out_path, "wb") as f:
                        for chunk in vid_data.iter_content(chunk_size=65536):
                            if chunk:
                                f.write(chunk)
                    if out_path.exists() and out_path.stat().st_size > 50000:
                        Messenger.success(f"✅ Video NASA descargado ({out_path.stat().st_size / 1024:.1f} KB)")
                        return True

            return False
        except Exception as e:
            Messenger.warning(f"⚠️ Error al consultar NASA API: {e}")
            return False
