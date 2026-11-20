import os
import time
import random
import shutil
import subprocess
from pathlib import Path
from tools.common.messenger import Messenger
from tools.common.base_model import BaseModelTool

class AIImageMaster(BaseModelTool):
    """
    Motor Maestro de Imágenes con IA y Movimiento Ken Burns:
    1. Primario: Hugging Face gradio_client conectado al Space Oficial de FLUX.1 [schnell]
    2. Backup: Google Imagen 3 (imagen-3.0-generate-002) vía google-genai
    3. Movimiento cinematográfico Ken Burns con FFmpeg a 1080x1920 30fps
    """

    def generate_image_flux_gradio(self, prompt: str, out_img: Path) -> bool:
        """Genera imagen con el Space Oficial de FLUX.1 [schnell] de Black Forest Labs."""
        try:
            from gradio_client import Client
            Messenger.info(f"🎨 [FLUX.1 Gradio Client] Generando imagen con Space Oficial para: '{prompt[:55]}...'")
            t0 = time.time()
            client = Client("black-forest-labs/FLUX.1-schnell")
            
            # Formato vertical 1024x1792 (múltiplo de 16, nativo en FLUX)
            result = client.predict(
                prompt=prompt,
                seed=random.randint(1, 9999999),
                randomize_seed=True,
                width=1024,
                height=1792,
                num_inference_steps=4,
                api_name="/infer"
            )
            
            if result and Path(result).exists() and Path(result).stat().st_size > 10000:
                out_img.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(result, out_img)
                Messenger.success(f"✨ [FLUX.1] Imagen creada con éxito en {time.time()-t0:.1f}s ({out_img.stat().st_size/1024:.1f} KB)")
                return True
            return False
        except Exception as e:
            Messenger.warning(f"⚠️ [FLUX.1 Gradio Client] No disponible o timeout ({e}). Activando Backup Google Imagen 3...")
            return False

    def generate_image_google_imagen3(self, prompt: str, out_img: Path) -> bool:
        """Genera imagen con Google Imagen 3 (imagen-3.0-generate-002) vía google-genai."""
        try:
            from google import genai
            from google.genai import types
            from PIL import Image
            from io import BytesIO
            
            Messenger.info(f"🎨 [Google Imagen 3 Backup] Generando imagen para: '{prompt[:55]}...'")
            t0 = time.time()
            
            # Usa GEMINI_API_KEY del entorno
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY_2")
            if api_key:
                client = genai.Client(api_key=api_key)
            else:
                client = genai.Client()
                
            response = client.models.generate_images(
                model="imagen-3.0-generate-002",
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    output_mime_type="image/jpeg",
                    aspect_ratio="9:16",
                ),
            )
            
            if response.generated_images:
                img_bytes = response.generated_images[0].image.image_bytes
                if len(img_bytes) > 5000:
                    out_img.parent.mkdir(parents=True, exist_ok=True)
                    out_img.write_bytes(img_bytes)
                    Messenger.success(f"✨ [Google Imagen 3] Imagen creada con éxito en {time.time()-t0:.1f}s ({len(img_bytes)/1024:.1f} KB)")
                    return True
            return False
        except Exception as e:
            Messenger.warning(f"⚠️ [Google Imagen 3] Error: {e}")
            return False

    def generate_image_hf_inference_fallback(self, prompt: str, out_img: Path) -> bool:
        """Tercera capa de seguridad: HuggingFace Inference Client directo o descarga rápida."""
        try:
            import urllib.parse
            import requests
            Messenger.info(f"🎨 [Inference Fallback] Solicitando imagen de alta resolución...")
            clean_p = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{clean_p}?model=flux&width=1080&height=1920&nologo=true&seed={random.randint(1,99999)}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            r = requests.get(url, headers=headers, timeout=25)
            if r.status_code == 200 and len(r.content) > 10000:
                out_img.parent.mkdir(parents=True, exist_ok=True)
                out_img.write_bytes(r.content)
                return True
            return False
        except Exception:
            return False

    def generate_master_image(self, prompt: str, out_img: Path) -> bool:
        """Cascada maestra: 1. FLUX.1 Gradio -> 2. Google Imagen 3 -> 3. Fallback."""
        # 1. Intentar Primario (FLUX.1 Oficial Gradio)
        if self.generate_image_flux_gradio(prompt, out_img):
            return True
        
        # 2. Intentar Backup (Google Imagen 3)
        if self.generate_image_google_imagen3(prompt, out_img):
            return True
        
        # 3. Fallback de Red
        if self.generate_image_hf_inference_fallback(prompt, out_img):
            return True
            
        return False

    def create_ken_burns_clip(self, img_path: Path, out_clip: Path, duration: float, motion_style: int = 0) -> bool:
        """
        Convierte una imagen 9:16 en un clip de video vertical 1080x1920 30fps
        con movimiento dinámico Ken Burns (zoom suave y paneos cinematográficos).
        motion_style:
          0 -> Zoom In lento hacia el centro
          1 -> Zoom Out lento alejándose
          2 -> Paneo suave de izquierda a derecha con zoom leve
          3 -> Paneo suave de abajo hacia arriba con zoom leve
        """
        if not img_path.exists() or img_path.stat().st_size < 5000:
            return False

        frames = int(max(duration, 1.0) * 30)
        
        # Selección de movimiento cinematográfico alternado
        style = motion_style % 4
        if style == 0:
            # Zoom In lento
            z_expr = "min(zoom+0.0013,1.20)"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "ih/2-(ih/zoom/2)"
        elif style == 1:
            # Zoom Out lento
            z_expr = "if(lte(zoom,1.0),1.20,max(1.001,zoom-0.0013))"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "ih/2-(ih/zoom/2)"
        elif style == 2:
            # Paneo horizontal con zoom constante
            z_expr = "1.15"
            x_expr = "if(lte(on,1),(iw-iw/zoom)*0.2,x+((iw-iw/zoom)*0.6)/" + str(frames) + ")"
            y_expr = "ih/2-(ih/zoom/2)"
        else:
            # Paneo vertical con zoom constante
            z_expr = "1.15"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "if(lte(on,1),(ih-ih/zoom)*0.7,y-((ih-ih/zoom)*0.5)/" + str(frames) + ")"

        # FFmpeg Ken Burns filterchain optimizado para 1080x1920 vertical
        vf_filter = (
            f"scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920,"
            f"zoompan=z='{z_expr}':x='{x_expr}':y='{y_expr}':d={frames}:s=1080x1920:fps=30,"
            f"setsar=1"
        )

        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-i", str(img_path),
            "-vf", vf_filter,
            "-t", str(duration),
            "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
            "-pix_fmt", "yuv420p",
            str(out_clip)
        ]

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if out_clip.exists() and out_clip.stat().st_size > 10000:
                return True
        except Exception as e:
            Messenger.warning(f"⚠️ Error generando Ken Burns: {e}")

        # Fallback de emergencia si el filtro zoompan falla: escala estática con loop
        try:
            cmd_simple = [
                "ffmpeg", "-y", "-loop", "1", "-i", str(img_path),
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1",
                "-t", str(duration),
                "-an", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                str(out_clip)
            ]
            subprocess.run(cmd_simple, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return out_clip.exists() and out_clip.stat().st_size > 10000
        except Exception:
            return False

    def generate_ken_burns_scene(self, prompt: str, out_clip: Path, duration: float, motion_style: int, work_dir: Path) -> bool:
        """Genera la imagen con FLUX.1 / Imagen 3 y la convierte en clip Ken Burns."""
        temp_img = work_dir / f"{out_clip.stem}.jpg"
        ok_img = self.generate_master_image(prompt, temp_img)
        if not ok_img or not temp_img.exists() or temp_img.stat().st_size < 5000:
            # Fondo de emergencia en caso extremo
            cmd_emergency = [
                "ffmpeg", "-y", "-f", "lavfi",
                "-i", f"color=c=#0B1528:s=1080x1920:d={duration}:r=30",
                "-vf", "noise=alls=10:allf=t+u",
                "-an", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                str(out_clip)
            ]
            subprocess.run(cmd_emergency, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return out_clip.exists()

        ok_clip = self.create_ken_burns_clip(temp_img, out_clip, duration=duration, motion_style=motion_style)
        return ok_clip
