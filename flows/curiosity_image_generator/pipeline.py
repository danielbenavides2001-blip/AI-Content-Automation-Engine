import os
from pathlib import Path
import time
from dotenv import load_dotenv

from tools.common.messenger import Messenger
from tools.text_generation.gemini import GeminiTextGenerator
from tools.image_generation.vertex_ai import VertexAIImageGenerator
from tools.social_media.facebook import FacebookTool
from flows.curiosity_image_generator.models import CuriosityPost

class CuriosityPipeline:
    def __init__(self) -> None:
        load_dotenv()
        
        # Read settings from environment
        self.project_id = os.getenv("GCP_PROJECT_ID", "enigmaiq-bot")
        self.location = os.getenv("GCP_LOCATION", "us-central1")
        self.page_id = os.getenv("FACEBOOK_PAGE_ID")
        self.access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
        
        # Output directory
        self.output_dir = Path(__file__).parent / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Tools initialization
        self.text_gen = GeminiTextGenerator()
        
        # Initialize Vertex Image Generator (using 1:1 aspect ratio for Facebook feed)
        self.image_gen = VertexAIImageGenerator(
            project_id=self.project_id,
            location=self.location,
            aspect_ratio="1:1"
        )
        
        if self.page_id and self.access_token:
            self.fb_tool = FacebookTool(
                page_id=self.page_id,
                access_token=self.access_token
            )
        else:
            self.fb_tool = None
            Messenger.warning("⚠️ Facebook credentials missing in .env. Publishing will not be available.")

    def run(self, publish: bool = False) -> None:
        Messenger.info("✨ Starting Curiosity Photo Post Pipeline...")
        
        # 1. Generate Curiosity Text & Prompt using Gemini
        prompt = (
            "Identify a recent, viral, or highly fascinating curiosity or discovery that occurred in the world "
            "(e.g., a rare animal color variant like a pink dolphin or blue lobster, a strange natural phenomenon, "
            "or a bizarre scientific discovery). Generate a compelling Facebook post about it in Spanish."
        )
        
        Messenger.info("🧠 Generating curiosity story via Gemini...")
        post_data: CuriosityPost = self.text_gen.generate_text(prompt, CuriosityPost)
        
        Messenger.info(f"📌 Topic: {post_data.title}")
        Messenger.info(f"📝 Caption preview:\n{post_data.caption[:150]}...")
        Messenger.info(f"🎨 Image Prompt: {post_data.image_prompt}")
        
        # 2. Generate Image via Vertex AI
        timestamp = int(time.time())
        image_path = self.output_dir / f"curiosity_{timestamp}.jpg"
        
        Messenger.info("🎨 Sending request to Vertex AI (Imagen 3)...")
        try:
            self.image_gen.generate_image(
                prompt=post_data.image_prompt,
                output_path=image_path
            )
        except Exception as e:
            Messenger.error(f"❌ Failed to generate image via Vertex AI: {str(e)}")
            raise e
            
        # 3. Publish to Facebook if requested
        if publish:
            if not self.fb_tool:
                raise ValueError("❌ Cannot publish: Facebook credentials are missing in .env")
                
            Messenger.info("🚀 Publishing photo post to EnigmaIQ Facebook page...")
            try:
                photo_id = self.fb_tool.upload_photo(
                    file_path=image_path,
                    caption=post_data.caption
                )
                Messenger.success(f"🎉 Success! Photo post published to Facebook. ID: {photo_id}")
            except Exception as e:
                Messenger.error(f"❌ Failed to publish photo post: {str(e)}")
                raise e
        else:
            Messenger.success(f"💾 Dry-run complete. Image saved locally at: {image_path}")
