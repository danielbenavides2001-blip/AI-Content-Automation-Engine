import requests
import subprocess
import urllib.parse
from pathlib import Path
from tools.common.messenger import Messenger
from tools.common.base_model import BaseModelTool

class GenerativeVisualTool(BaseModelTool):
    """
    Generador visual por IA de respaldo ilimitado ($0.00 costo):
    Genera imágenes hiperrealistas 9:16 mediante FLUX/Stable Diffusion abierto (Pollinations)
    y las transforma con FFmpeg en clips de video cinematográficos con movimiento Ken Burns 2.5D.
    """

    def generate_clip(self, visual_prompt: str, out_path: Path, duration: float = 4.0) -> bool:
        """
        Genera un clip de video vertical 1080x1920 exacto a partir del prompt.
        """
        if not visual_prompt or not visual_prompt.strip():
            return False

        clean_prompt = visual_prompt.strip()
        Messenger.info(f"🎨 [IA Visual Generativa] Creando metraje exacto para: '{clean_prompt}'...")

        try:
            # 1. Descargar imagen 9:16 hiperrealista de Pollinations AI con User-Agent
            encoded_prompt = urllib.parse.quote(f"{clean_prompt}, cinematic documentary 8k, photorealistic, sharp focus, vertical 9:16")
            img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true"

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            temp_img = out_path.with_suffix(".gen.jpg")
            r = requests.get(img_url, headers=headers, timeout=30)
            if r.status_code != 200 or len(r.content) < 5000:
                # Reintento con prompt simplificado
                simple_prompt = urllib.parse.quote(clean_prompt)
                fallback_url = f"https://image.pollinations.ai/prompt/{simple_prompt}?width=1080&height=1920&nologo=true"
                r = requests.get(fallback_url, headers=headers, timeout=25)
                if r.status_code != 200 or len(r.content) < 5000:
                    Messenger.warning("⚠️ No se pudo descargar la imagen generada por IA.")
                    return False

            temp_img.parent.mkdir(parents=True, exist_ok=True)
            temp_img.write_bytes(r.content)

            # 2. Convertir en clip de video cinematográfico con zoompan Ken Burns (ultrafast)
            frames = int(duration * 30)
            cmd = [
                "ffmpeg", "-y", "-loop", "1", "-i", str(temp_img),
                "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0014,1.16)':d={frames}:s=1080x1920:fps=30",
                "-t", str(duration),
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
                "-pix_fmt", "yuv420p",
                str(out_path)
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            if temp_img.exists():
                temp_img.unlink()

            if out_path.exists() and out_path.stat().st_size > 10000:
                Messenger.success(f"✨ Clip IA generado con éxito ({out_path.stat().st_size / 1024:.1f} KB)")
                return True

            return False
        except Exception as e:
            Messenger.warning(f"⚠️ Error generando clip IA: {e}")
            return False
