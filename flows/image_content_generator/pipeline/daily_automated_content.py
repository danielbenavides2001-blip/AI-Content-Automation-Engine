import os
import sys
import random
import subprocess
from pathlib import Path
from dotenv import load_dotenv

from flows.image_content_generator.pipeline.prompt_shorts.finances.models import RiddlePost
from flows.image_content_generator.pipeline.prompt_shorts.finances import constants as finance_constants
from tools.common.messenger import Messenger
from tools.text_generation.gemini import GeminiTextGenerator
from tools.image_generation.vertex_ai import VertexAIImageGenerator
from tools.social_media.facebook import FacebookTool
import time

load_dotenv()

class DailyAutomator:
    def __init__(self):
        self.text_gen = GeminiTextGenerator()
        self.image_gen = VertexAIImageGenerator(
            project_id=os.getenv("GCP_PROJECT_ID"),
            location=os.getenv("GCP_LOCATION")
        )
        self.facebook = FacebookTool(
            page_id=os.getenv("FACEBOOK_PAGE_ID"),
            access_token=os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
        )
        self.out_dir = Path("flows/image_content_generator/out_short/daily_content")
        self.out_dir.mkdir(parents=True, exist_ok=True)
        
        self.history_file = Path("flows/image_content_generator/out_short/automated_posts_history.csv")
        if not self.history_file.exists():
            self.history_file.write_text("date,type,topic\n")

    def get_recent_topics(self) -> str:
        import pandas as pd
        topics = []
        # 1. Get automated posts history
        if self.history_file.exists():
            try:
                df_auto = pd.read_csv(self.history_file)
                topics.extend(df_auto["topic"].tail(50).tolist())
            except Exception:
                pass
        
        # 2. Get video titles history
        video_csv = Path("flows/image_content_generator/out_short/ideas_tracking.csv")
        if video_csv.exists():
            try:
                df_video = pd.read_csv(video_csv)
                topics.extend(df_video["title"].tail(50).tolist())
            except Exception:
                pass
            
        if not topics:
            return ""
        
        # Deduplicate and format
        unique_topics = list(set([str(t).strip() for t in topics if str(t).strip()]))
        avoid_list = "\n- ".join(unique_topics[-40:]) # Last 40 unique topics
        
        return f"\n\n**CRITICAL - ANTI-REPETITION RULES:**\nDO NOT repeat, reuse or get inspired by the following themes, metaphors or titles (THEY ARE ALREADY POSTED):\n- {avoid_list}\n\nBe creative. EXPLORE NEW VISUAL TERRITORIES."

    def sync_to_github(self):
        """
        Commits and pushes the history files back to GitHub to persist memory between runs.
        """
        Messenger.info("🔄 Syncing history and state to GitHub...")
        try:
            # Files to track
            files_to_sync = [
                str(self.history_file),
                ".last_post_type",
                "flows/image_content_generator/out_short/ideas_tracking.csv"
            ]
            
            # Check which files exist before adding
            existing_files = [f for f in files_to_sync if Path(f).exists()]
            
            if not existing_files:
                Messenger.warning("⚠️ No history files found to sync.")
                return

            # Git commands
            subprocess.run(["git", "config", "--global", "user.name", "Automated Bot"], check=True)
            subprocess.run(["git", "config", "--global", "user.email", "bot@automation.com"], check=True)
            
            for f in existing_files:
                subprocess.run(["git", "add", "-f", f], check=True)
            
            # Check if there are STAGED changes to commit
            staged = subprocess.run(["git", "diff", "--cached", "--quiet"])
            if staged.returncode == 0:
                Messenger.info("✨ No staged changes in history to sync.")
                return

            subprocess.run(["git", "commit", "-m", "chore: update post history and state [skip ci]"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            Messenger.success("✅ History successfully synced to GitHub!")
        except Exception as e:
            Messenger.error(f"❌ Failed to sync to GitHub: {e}")

    def log_post(self, post_type: str, topic: str):
        from datetime import datetime
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()},{post_type},{topic.replace(',', ' ')}\n")

    def generate_daily_text_post(self):
        Messenger.info("🤖 Generating daily finance tip (Text)...")
        avoid_msg = self.get_recent_topics()
        prompt = f"""
        Genera un post de Facebook corto y muy valioso sobre finanzas personales.
        Puede ser un consejo de ahorro, una estrategia de inversión, un hack de presupuesto o un dato psicológico sobre el dinero.
        Usa emojis y un tono cercano.
        Responde solo con el texto del post.{avoid_msg}
        """
        message = self.text_gen.generate(prompt)
        # Extract a "topic" from the message (first 5 words)
        topic = " ".join(message.split()[:5])
        self.facebook.create_text_post(message)
        self.log_post("text", topic)

    def generate_daily_image_post(self):
        Messenger.info("🤖 Generating daily finance RIDDLE image post...")
        avoid_msg = self.get_recent_topics()
        
        # 1. Generate Structured Riddle Data
        prompt = finance_constants.IMAGE_INTERACTION_PROMPT + avoid_msg
        riddle_data = self.text_gen.generate_text(prompt, RiddlePost)
        
        # 2. Generate Image with Vertex AI (Imagen 3)
        Messenger.info(f"🎨 Visual Idea: {riddle_data.idea_visual}")
        Messenger.info(f"🎯 Objective: {riddle_data.objetivo_psicologico}")
        
        image_path = self.out_dir / "daily_image.png"
        self.image_gen.generate_image(
            prompt=riddle_data.image_prompt,
            output_path=image_path
        )
        
        description = riddle_data.caption
        
        # 4. Upload with Retry Logic
        Messenger.info(f"🚀 Uploading photo to Facebook: {image_path.name}")
        
        # Convert to JPEG for better Facebook compatibility (prevents 500 errors)
        if image_path.suffix.lower() == ".png":
            from PIL import Image
            jpg_path = image_path.with_suffix(".jpg")
            with Image.open(image_path) as img:
                img.convert("RGB").save(jpg_path, "JPEG", quality=95)
            image_path = jpg_path

        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.facebook.upload_photo(image_path, description)
                self.log_post("image", riddle_data.idea_visual)
                Messenger.success("✅ Photo published successfully!")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    Messenger.warning(f"⚠️ Upload attempt {attempt+1} failed. Retrying in 10s... ({str(e)})")
                    time.sleep(10)
                else:
                    Messenger.error(f"❌ Failed to upload photo after {max_retries} attempts.")
                    raise e

    def run_daily_mix(self):
        Messenger.info("🚀 Starting Daily Automated Content Picker (Stable Cycle)...")
        
        # Determine choice: Force from Env or Cycle from file
        force_type = os.getenv("FORCE_POST_TYPE")
        state_file = Path(".last_post_type")
        
        if force_type and force_type.strip():
            try:
                choice = int(force_type)
                Messenger.info(f"⚠️ Forcing post type from environment: {choice}")
            except ValueError:
                Messenger.warning(f"❌ Invalid FORCE_POST_TYPE '{force_type}'. Falling back to cycle.")
                choice = None
        else:
            choice = None

        if choice is None:
            # DEFAULT: Historias Atrapantes (Choice 3)
            choice = 3
            
            # Guardar el nuevo estado
            state_file.write_text(str(choice))
            Messenger.info(f"🔄 Setting default post type to STORIES (Choice 3)")

        # --- NEW: CLEAR STUCK IDEAS ---
        # Before running, we ensure no half-finished ideas exist in the 'ideas' folder
        # to prevent reusing old/corrupt content.
        Messenger.info("🧹 Cleaning up stuck or incomplete ideas...")
        ideas_dir = Path("flows/image_content_generator/out_short/ideas")
        if ideas_dir.exists():
            import shutil
            # We check the ideas_tracking.csv to see what's NOT COMPLETED or UPLOADED
            video_csv = Path("flows/image_content_generator/out_short/ideas_tracking.csv")
            tracking_titles = []
            if video_csv.exists():
                try:
                    import pandas as pd
                    df = pd.read_csv(video_csv)
                    # We keep track of titles but we'll be aggressive: 
                    # If it's not UPLOADED, we consider it a failed attempt.
                    valid_ids = df[df["state"].isin(["UPLOADED", "COMPLETED"])]["id"].tolist()
                    for idea_path in ideas_dir.iterdir():
                        if idea_path.is_dir():
                            try:
                                idea_id = int(idea_path.name.split("_")[-1])
                                if idea_id not in valid_ids:
                                    Messenger.warning(f"🗑️ Deleting stuck idea: {idea_path.name}")
                                    shutil.rmtree(idea_path)
                            except ValueError:
                                pass
                except Exception as e:
                    Messenger.warning(f"Could not parse tracking CSV for cleanup: {e}")

        try:
            if choice == 0 or choice == 2:
                # Interaction or regular image
                Messenger.info("🧩 GENERATING INTERACTION IMAGE POST...")
                self.generate_daily_image_post()
            elif choice == 1 or choice == 3:
                # Video generation (Standard or Story)
                mode_name = "STORY REEL" if choice == 3 else "STANDARD REEL"
                Messenger.info(f"🎬 GENERATING NEW {mode_name} (Steps 1-8)...")
                avoid_msg = self.get_recent_topics()
                
                # Pass the choice as FORCE_POST_TYPE to the subprocess
                env = os.environ.copy()
                env["FORCE_POST_TYPE"] = str(choice)
                
                subprocess.run([sys.executable, "-m", "flows.image_content_generator.pipeline.main", "short", "all", "--avoid", avoid_msg], check=True, env=env)
            else:
                Messenger.warning(f"❓ Unknown choice {choice}. No action taken.")
            
            Messenger.success("✅ Automated task execution completed!")
            self.sync_to_github()
            
        except Exception as e:
            Messenger.error(f"Error during automated task: {e}")
            sys.exit(1)

if __name__ == "__main__":
    automator = DailyAutomator()
    automator.run_daily_mix()
