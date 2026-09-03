import random
import time
from pathlib import Path
from typing import Any, List, Optional

from google import genai
from google.genai import types

from tools.common.messenger import Messenger
from tools.image_generation.midjourney import ImageTask
from tools.utils.time import retry


class VertexAIImageGenerator:
    """
    Generator that uses the NEW google-genai SDK to generate 
    "Live Images" (animated 4-second video clips) via generate_videos.
    """

    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        aspect_ratio: str = "9:16",
        **kwargs: Any
    ) -> None:
        self.project_id = project_id
        self.location = location
        self.aspect_ratio = aspect_ratio
        
        # Initialize the new GenAI Client
        self.client = genai.Client(
            vertexai=True, 
            project=self.project_id, 
            location=self.location
        )

    def generate_image(
        self,
        prompt: str,
        output_path: Path,
    ) -> None:
        """
        Generates a static image using gemini-2.5-flash-image via Vertex AI.
        Uses generate_content() with IMAGE modality (new API as of 2025).
        Includes robust exponential backoff to handle rate limit errors.
        """
        Messenger.info(f"Generating Vertex AI Image: {prompt[:50]}...")
        
        max_attempts = 5
        base_delay = 4.0
        current_prompt = prompt
        
        for attempt in range(1, max_attempts + 1):
            try:
                # Si falló en el primer intento, simplificar el prompt para eludir filtros de seguridad o sobrecarga
                if attempt >= 2:
                    words = prompt.split()
                    simplified = " ".join(words[:25])
                    current_prompt = f"{simplified}, cinematic lighting, photorealistic, 8k vertical"
                    Messenger.info(f"   🔄 Reintentando con prompt simplificado (intento {attempt}): {current_prompt[:60]}...")

                response = self.client.models.generate_content(
                    model='gemini-2.5-flash-image',
                    contents=current_prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                    )
                )

                # Extract image bytes from the response parts
                image_bytes = None
                if response and response.candidates and response.candidates[0].content:
                    for part in response.candidates[0].content.parts:
                        if getattr(part, "inline_data", None) is not None:
                            image_bytes = part.inline_data.data
                            break

                if not image_bytes:
                    raise RuntimeError("Vertex AI no devolvió imagen en la respuesta")

                # Save the image
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(image_bytes)
                
                Messenger.image(f"Imagen generada con éxito: {output_path.name}")
                return
            except Exception as e:
                error_str = str(e)
                Messenger.warning(f"Attempt {attempt}/{max_attempts} failed: {error_str[:120]}")
                
                if attempt == max_attempts:
                    raise e
                
                # Check for rate limits / 429
                is_rate_limit = "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower()
                sleep_time = (base_delay * (2 ** (attempt - 1))) + random.uniform(1.0, 2.5)
                time.sleep(sleep_time)

    @retry(max_attempts=3, delay=10.0)
    def generate_video(
        self,
        prompt: str,
        output_path: Path,
    ) -> None:
        """
        Generates an animated clip using Veo 2 (veo-2.0-generate-001) via Vertex AI.
        """
        Messenger.info(f"Generating Vertex AI Video (Veo 2): {prompt[:50]}...")
        
        # Trigger Asynchronous Generation
        operation = self.client.models.generate_videos(
            model='veo-2.0-generate-001',
            prompt=prompt,
            config=types.GenerateVideosConfig(
                aspect_ratio=self.aspect_ratio,
            )
        )

        # Polling for Completion
        while not operation.done:
            Messenger.info("⏳ Waiting for Veo 2 video generation (polling)...")
            time.sleep(15)
            operation = self.client.operations.get(operation)

        if operation.error:
            raise RuntimeError(f"❌ Video generation failed: {operation.error}")

        if not operation.response or not operation.response.generated_videos:
            raise RuntimeError("❌ Vertex AI Veo no devolvió videos")

        # Save the video
        video_metadata = operation.response.generated_videos[0]
        video_obj = video_metadata.video
        
        if video_obj.video_bytes:
            with open(output_path, "wb") as f:
                f.write(video_obj.video_bytes)
        else:
            # Fallback to save method if bytes are not directly available
            video_obj.save(str(output_path))
        
        Messenger.success(f"Video animado generado con éxito: {output_path}")

    def generate_images(self, tasks: List[ImageTask]) -> None:
        """
        Batch processing for Vertex AI Images using ThreadPoolExecutor.
        Garantiza que toda escena tenga una imagen válida en disco.
        """
        total = len(tasks)
        Messenger.info(f"Vertex AI Image Generation Batch: {total} images (Sequential with max_workers=1)")

        def process_task(item):
            i, task = item
            out_path = task.output_path
            
            if out_path.exists() and out_path.stat().st_size > 5120:
                Messenger.info(f"Skipping {out_path.name}: File already exists.")
                return True

            Messenger.info(f"Processing Scene {i}/{total}: {out_path.name}")
            try:
                if task.is_video:
                    self.generate_video(
                        prompt=task.prompt,
                        output_path=out_path
                    )
                else:
                    self.generate_image(
                        prompt=task.prompt,
                        output_path=out_path
                    )
                time.sleep(1.5)
                return True
            except Exception as e:
                Messenger.error(f"Error in scene {i}: {str(e)[:120]}")
                
                # --- RESCATE INMEDIATO DE IMAGEN ---
                # Intentar descargar una foto de respaldo desde Pexels usando palabras clave del prompt
                try:
                    from tools.video_generation.pexels import PexelsTool
                    px = PexelsTool()
                    prompt_words = [w for w in task.prompt.split() if len(w) > 4 and w.lower() not in ["image", "style", "cinematic", "photorealistic", "national", "geographic"]]
                    fallback_query = " ".join(prompt_words[:2]) if prompt_words else "ancient mystery"
                    if px.fetch_photo(fallback_query, out_path):
                        Messenger.success(f"   🛡️ Respaldo Pexels aplicado exitosamente para escena {i}")
                        return True
                except Exception as px_e:
                    Messenger.warning(f"   Fallback Pexels falló: {px_e}")

                return False

        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            results = list(executor.map(process_task, enumerate(tasks, start=1)))

        successful = sum(results)
        failed = total - successful
        Messenger.step_success(f"Batch complete: {successful}/{total} scenes processed successfully.")

        # Si alguna escena falló pero otras tuvieron éxito, reutilizar una imagen válida para no dejar escenas vacías
        if failed > 0:
            valid_images = [t.output_path for t in tasks if t.output_path.exists() and t.output_path.stat().st_size > 5120]
            if valid_images:
                import shutil
                for task in tasks:
                    if not task.output_path.exists() or task.output_path.stat().st_size < 5120:
                        donor = random.choice(valid_images)
                        shutil.copyfile(donor, task.output_path)
                        Messenger.info(f"   🔄 Escena {task.output_path.name} completada con respaldo visual de {donor.name}")

        if successful == 0 and not any(t.output_path.exists() for t in tasks):
            raise RuntimeError(f"❌ ALL {total} images failed to generate. Stopping pipeline.")
