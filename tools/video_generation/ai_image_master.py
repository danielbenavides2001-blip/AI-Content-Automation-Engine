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
    Motor Maestro de Imágenes con IA, Fotografía de Stock y Movimiento Ken Burns:
    1. Primario IA: Hugging Face gradio_client conectado al Space Oficial de FLUX.1 [schnell]
    2. Backup IA: Google Imagen 3 vía google-genai (Vertex AI y Google AI Studio)
    3. Fotografía de Respaldo Inmediata: Pexels & Pixabay Photo API para la curiosidad exacta
    4. Movimiento cinematográfico Ken Burns con FFmpeg a 1080x1920 30fps (sin pantallas negras)
    """

    def generate_image_flux_gradio(self, prompt: str, out_img: Path) -> bool:
        """Genera imagen con el Space Oficial de FLUX.1 [schnell] de Black Forest Labs."""
        spaces_to_try = [
            "black-forest-labs/FLUX.1-schnell",
            "multimodalart/FLUX.1-merged",
        ]
        
        try:
            from gradio_client import Client
        except ImportError:
            Messenger.warning("⚠️ [FLUX.1] gradio_client no está instalado en este entorno.")
            return False

        hf_token = os.getenv("HF_TOKEN")
        
        for space_name in spaces_to_try:
            try:
                Messenger.info(f"🎨 [FLUX.1 Gradio Client] Intentando Space '{space_name}' para: '{prompt[:50]}...'")
                t0 = time.time()
                client = Client(space_name, hf_token=hf_token)
                
                # Formato vertical optimizado para velocidad e inferencia en nube
                result = client.predict(
                    prompt=prompt,
                    seed=random.randint(1, 9999999),
                    randomize_seed=True,
                    width=768,
                    height=1360,
                    num_inference_steps=4,
                    api_name="/infer"
                )
                
                # Gradio puede retornar una tupla (filepath, seed) o un string
                if isinstance(result, (tuple, list)) and len(result) > 0:
                    img_res = result[0]
                else:
                    img_res = result
                
                if img_res and Path(img_res).exists() and Path(img_res).stat().st_size > 10000:
                    out_img.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(img_res, out_img)
                    Messenger.success(f"✨ [FLUX.1] Imagen creada con éxito en {time.time()-t0:.1f}s ({out_img.stat().st_size/1024:.1f} KB)")
                    return True
            except Exception as e:
                Messenger.warning(f"⚠️ [FLUX.1 Gradio Client] Space '{space_name}' no disponible ({str(e)[:90]}). Probando alternativa...")
                continue
                
        return False

    def generate_image_google_imagen3(self, prompt: str, out_img: Path) -> bool:
        """Genera imagen con Google Imagen 3 vía google-genai (Vertex AI y Google AI Studio)."""
        # 1. Intentar Vertex AI si las credenciales o proyecto están configurados
        gcp_project = os.getenv("GCP_PROJECT_ID")
        gcp_cred = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if gcp_project or gcp_cred:
            try:
                from google import genai
                from google.genai import types
                Messenger.info(f"🎨 [Google Imagen 3 - Vertex AI] Generando imagen para: '{prompt[:50]}...'")
                t0 = time.time()
                client = genai.Client(
                    vertexai=True,
                    project=gcp_project or "automatizacion-475715",
                    location=os.getenv("GCP_LOCATION", "us-central1")
                )
                response = client.models.generate_images(
                    model="imagen-3.0-generate-001",
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
                        Messenger.success(f"✨ [Vertex AI Imagen 3] Creada con éxito en {time.time()-t0:.1f}s ({len(img_bytes)/1024:.1f} KB)")
                        return True
            except Exception as e:
                Messenger.warning(f"⚠️ [Vertex AI Imagen 3] Error: {str(e)[:100]}")

        # 2. Intentar Google AI Studio con GEMINI_API_KEY
        try:
            from google import genai
            from google.genai import types
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY_2")
            if api_key:
                Messenger.info(f"🎨 [Google AI Studio Imagen 3] Generando imagen para: '{prompt[:50]}...'")
                t0 = time.time()
                client = genai.Client(api_key=api_key)
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
                        Messenger.success(f"✨ [Google AI Studio Imagen 3] Creada con éxito en {time.time()-t0:.1f}s ({len(img_bytes)/1024:.1f} KB)")
                        return True
        except Exception as e:
            Messenger.warning(f"⚠️ [Google AI Studio Imagen 3] Error: {str(e)[:100]}")

        return False

    def fetch_stock_photo(self, query: str, out_img: Path) -> bool:
        """Descarga fotografía vertical HD de Pexels o Pixabay de la curiosidad exacta."""
        if not query or not query.strip():
            return False
        clean_q = query.strip()
        try:
            from tools.video_generation.pexels import PexelsTool
            px = PexelsTool()
            if px.fetch_photo(clean_q, out_img):
                return True
        except Exception:
            pass

        try:
            from tools.video_generation.pixabay import PixabayTool
            pb = PixabayTool()
            if pb.fetch_photo(clean_q, out_img):
                return True
        except Exception:
            pass

        return False

    def generate_master_image(self, prompt: str, out_img: Path, query: str = "", fallback_query: str = "") -> bool:
        """
        Cascada maestra infalible:
        1. FLUX.1 Oficial (Gradio Space de Black Forest Labs)
        2. Google Imagen 3 (Vertex AI / Google AI Studio vía google-genai)
        3. Fotografía de Stock de Pexels / Pixabay para la curiosidad exacta
        4. Fotografía de Stock de respaldo
        """
        # 1. Intentar Primario (FLUX.1 Oficial Gradio)
        if self.generate_image_flux_gradio(prompt, out_img):
            return True
        
        # 2. Intentar Backup (Google Imagen 3)
        if self.generate_image_google_imagen3(prompt, out_img):
            return True
        
        # 3. Intentar Fotografía de Stock HD (Pexels / Pixabay) con la curiosidad exacta
        if query:
            Messenger.info(f"📸 [Respaldo Fotográfico] Buscando foto real de alta resolución para: '{query}'...")
            if self.fetch_stock_photo(query, out_img):
                Messenger.success(f"✨ [Stock Photo] Fotografía HD obtenida para '{query}' ({out_img.stat().st_size/1024:.1f} KB)")
                return True

        # 4. Intentar Fotografía de Stock con fallback query
        if fallback_query:
            Messenger.info(f"📸 [Respaldo Fotográfico Secundario] Buscando foto para: '{fallback_query}'...")
            if self.fetch_stock_photo(fallback_query, out_img):
                Messenger.success(f"✨ [Stock Photo] Fotografía HD obtenida para '{fallback_query}' ({out_img.stat().st_size/1024:.1f} KB)")
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

        # Fallback si el filtro zoompan falla: escala estática con loop
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

    def generate_ken_burns_scene(self, prompt: str, out_clip: Path, duration: float, motion_style: int, work_dir: Path, query: str = "", fallback_query: str = "") -> bool:
        """Genera la imagen con FLUX.1 / Imagen 3 / Stock Photo y la convierte en clip Ken Burns."""
        temp_img = work_dir / f"{out_clip.stem}.jpg"
        ok_img = self.generate_master_image(prompt, temp_img, query=query, fallback_query=fallback_query)
        if not ok_img or not temp_img.exists() or temp_img.stat().st_size < 5000:
            # NUNCA generar fondo negro ficticio: retornar False para activar MediaHub
            Messenger.warning(f"⚠️ [Scene] No se obtuvo imagen directa para '{prompt[:40]}'. Activando rescate en MediaHub...")
            return False

        ok_clip = self.create_ken_burns_clip(temp_img, out_clip, duration=duration, motion_style=motion_style)
        return ok_clip
