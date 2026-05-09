import time
from pathlib import Path
from typing import Any, List, Optional

from google import genai
from google.genai import types

from tools.common.messenger import Messenger
from tools.image_generation.midjourney import ImageTask


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
        Generates a static image using Imagen 3 via Vertex AI.
        """
        Messenger.info(f"Generating Vertex AI Image: {prompt[:50]}...")
        
        response = self.client.models.generate_images(
            model='imagen-3.0-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=self.aspect_ratio,
            )
        )

        if not response or not response.generated_images:
            raise RuntimeError("❌ Vertex AI Imagen no devolvió imágenes")

        # Save the image
        with open(output_path, "wb") as f:
            f.write(response.generated_images[0].image.image_bytes)
        
        Messenger.image(f"Imagen generada con éxito: {output_path}")

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
        Batch processing for Vertex AI Images.
        """
        total = len(tasks)
        Messenger.info(f"Vertex AI Image Generation Batch: {total} images")

        for i, task in enumerate(tasks, start=1):
            out_path = task.output_path
            
            if out_path.exists():
                Messenger.info(f"Skipping {out_path.name}: File already exists.")
                continue

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
                # Delay to avoid 429 quota exhaustion (10 RPM limit for images, and video is slow anyway)
                time.sleep(7)
            except Exception as e:
                Messenger.error(f"Error in scene {i}: {str(e)}")
                # Continue with next scene instead of crashing the whole batch
                continue

        Messenger.step_success(f"Batch complete: {total} scenes processed.")
