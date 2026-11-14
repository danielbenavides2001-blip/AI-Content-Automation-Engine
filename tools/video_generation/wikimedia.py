import requests
import subprocess
from pathlib import Path
from pydantic import Field
from tools.common.messenger import Messenger
from tools.common.base_model import BaseModelTool
from typing import Optional

class WikimediaTool(BaseModelTool):
    """
    Herramienta para buscar y descargar metraje de video, fotos históricas, diagramas
    y material científico libre de Wikimedia Commons (100% gratuito y de uso libre).
    """
    base_url: str = "https://commons.wikimedia.org/w/api.php"
    user_agent: str = "EnigmaIQAutomationEngine/2.0 (contact@enigmaiq.org)"

    def fetch_video(self, query: str, out_path: Path) -> bool:
        """
        Busca un archivo de video en Wikimedia Commons y lo guarda en out_path como MP4.
        """
        if not query or not query.strip():
            return False

        clean_query = query.strip()
        Messenger.info(f"🏛️ [Wikimedia Commons] Buscando video para: '{clean_query}'...")

        try:
            # Buscar videos primero (webm, ogv, mp4)
            search_query = f"filetype:video {clean_query}"
            params = {
                "action": "query",
                "format": "json",
                "generator": "search",
                "gsrsearch": search_query,
                "gsrlimit": 5,
                "prop": "imageinfo",
                "iiprop": "url|mime|size"
            }
            headers = {"User-Agent": self.user_agent}
            resp = requests.get(self.base_url, params=params, headers=headers, timeout=12)
            if resp.status_code != 200:
                return False

            data = resp.json()
            pages = data.get("query", {}).get("pages", {})
            if not pages:
                Messenger.info(f"ℹ️ No se encontraron videos directos en Wikimedia para '{clean_query}'.")
                return False

            for pid, pdata in pages.items():
                imageinfo = pdata.get("imageinfo", [])
                if not imageinfo:
                    continue
                file_url = imageinfo[0].get("url")
                if not file_url:
                    continue

                Messenger.info(f"⬇️ Descargando archivo de Wikimedia: {pdata.get('title')}...")
                raw_ext = file_url.split(".")[-1].lower()
                temp_raw = out_path.with_suffix(f".raw.{raw_ext}")
                
                r = requests.get(file_url, headers=headers, timeout=40, stream=True)
                if r.status_code == 200:
                    temp_raw.parent.mkdir(parents=True, exist_ok=True)
                    with open(temp_raw, "wb") as f:
                        for chunk in r.iter_content(chunk_size=65536):
                            if chunk:
                                f.write(chunk)

                    if temp_raw.exists() and temp_raw.stat().st_size > 10000:
                        # Transcodificar a MP4 compatible si es webm u ogv
                        if raw_ext in ["webm", "ogv"]:
                            subprocess.run([
                                "ffmpeg", "-y", "-i", str(temp_raw),
                                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                                "-an", str(out_path)
                            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            if temp_raw.exists():
                                temp_raw.unlink()
                        else:
                            temp_raw.replace(out_path)

                        Messenger.success(f"✅ Video Wikimedia descargado ({out_path.stat().st_size / 1024:.1f} KB)")
                        return True

            return False
        except Exception as e:
            Messenger.warning(f"⚠️ Error en WikimediaTool: {e}")
            return False

    def fetch_image_clip(self, query: str, out_path: Path, duration: float = 4.0) -> bool:
        """
        Si no hay video, busca una imagen histórica/científica de alta resolución en Wikimedia
        y le aplica movimiento cinematográfico Ken Burns (zoom dinámico 9:16).
        """
        try:
            params = {
                "action": "query",
                "format": "json",
                "generator": "search",
                "gsrsearch": f"filetype:bitmap {query}",
                "gsrlimit": 3,
                "prop": "imageinfo",
                "iiprop": "url|mime|size"
            }
            headers = {"User-Agent": self.user_agent}
            resp = requests.get(self.base_url, params=params, headers=headers, timeout=12)
            if resp.status_code != 200:
                return False

            pages = resp.json().get("query", {}).get("pages", {})
            for pid, pdata in pages.items():
                imageinfo = pdata.get("imageinfo", [])
                if not imageinfo:
                    continue
                file_url = imageinfo[0].get("url")
                if not file_url:
                    continue

                temp_img = out_path.with_suffix(".temp.jpg")
                r = requests.get(file_url, headers=headers, timeout=20)
                if r.status_code == 200:
                    temp_img.write_bytes(r.content)
                    
                    # Convertir imagen a video vertical 1080x1920 con Ken Burns suave
                    cmd = [
                        "ffmpeg", "-y", "-loop", "1", "-i", str(temp_img),
                        "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0012,1.15)':d={int(duration*30)}:s=1080x1920:fps=30",
                        "-t", str(duration),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        str(out_path)
                    ]
                    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    if temp_img.exists():
                        temp_img.unlink()
                    Messenger.success(f"✅ Clip Ken Burns generado desde foto histórica de Wikimedia")
                    return True
            return False
        except Exception as e:
            Messenger.warning(f"⚠️ Error generando imagen clip de Wikimedia: {e}")
            return False
