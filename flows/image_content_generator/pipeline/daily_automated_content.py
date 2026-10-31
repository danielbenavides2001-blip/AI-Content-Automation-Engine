import os
import sys
import subprocess
import random
from pathlib import Path
from dotenv import load_dotenv

from flows.image_content_generator.pipeline.prompt_shorts.finances.models import RiddlePost
from flows.image_content_generator.pipeline.prompt_shorts.finances import constants as finance_constants
from tools.common.messenger import Messenger
from tools.text_generation.gemini import GeminiTextGenerator
from tools.image_generation.free_hybrid import FreeHybridImageGenerator
from tools.social_media.facebook import FacebookTool
from tools.common.topic_validator import TopicValidator

load_dotenv()

class DailyAutomator:
    def __init__(self):
        self.text_gen = GeminiTextGenerator()
        self.image_gen = FreeHybridImageGenerator(aspect_ratio="9:16")
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
        """Returns a string of recent topics to avoid repetition."""
        topics = []
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()[1:]
                    for line in lines[-15:]:
                        parts = line.strip().split(",")
                        if len(parts) >= 3:
                            topics.append(parts[2])
            except Exception:
                pass
        
        video_csv = Path("flows/image_content_generator/out_short/ideas_tracking.csv")
        if video_csv.exists():
            try:
                import pandas as pd
                df = pd.read_csv(video_csv)
                if not df.empty and "title" in df.columns:
                    recent_titles = df["title"].dropna().tolist()[-10:]
                    topics.extend(recent_titles)
            except Exception:
                pass

        if not topics:
            return "Ninguno aún."
        return "; ".join(topics)

    def log_post(self, post_type: str, topic: str):
        """Logs the published content to prevent duplication."""
        import datetime
        today = datetime.date.today().isoformat()
        clean_topic = topic.replace(",", " - ").strip()
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(f"{today},{post_type},{clean_topic}\n")

    def generate_daily_standard_image(self):
        """Generates 1 high-retention ¿SABÍAS QUE...? image with question caption."""
        Messenger.info("Generating Daily ¿SABÍAS QUE...? Image Post...")
        recent_topics = self.get_recent_topics()

        prompt = finance_constants.IDEA_PROMPT_FINANCE.format(
            avoid_list=recent_topics,
            selected_concept="CURIOSIDAD FINANCIERA / PSICOLOGÍA DEL DINERO"
        )
        
        try:
            riddle_idea = self.text_gen.generate_object(
                prompt=prompt,
                response_schema=RiddlePost
            )
            Messenger.info(f"Generated Idea: {riddle_idea.question}")

            validator = TopicValidator()
            is_valid, reason = validator.validate(riddle_idea.question, recent_topics)
            if not is_valid:
                Messenger.warning(f"⚠️ Topic rejected: {reason}. Trying with a fallback angle...")
                riddle_idea.question = f"¿Sabías que el 90% de las decisiones de compra no las toma tu lógica?"

            img_filename = f"daily_curiosity_{riddle_idea.question[:15].strip().replace(' ', '_')}.png"
            img_filename = "".join(c for c in img_filename if c.isalnum() or c in ('_', '.')).rstrip()
            img_path = self.out_dir / img_filename

            full_prompt = (
                f"{riddle_idea.image_prompt}, cinematic 8k, photorealistic hyper-detailed, "
                f"cyberpunk neon accents, editorial magazine quality, dramatic volumetric lighting, "
                f"dark sophisticated background, high contrast, clean visual storytelling"
            )
            self.image_gen.generate(full_prompt, img_path)

            caption = (
                f"💡 ¿SABÍAS ESTO? 🤔\n\n"
                f"{riddle_idea.question}\n\n"
                f"{riddle_idea.caption_explanation}\n\n"
                f"👇 Cuéntanos en los comentarios si ya conocías este dato.\n\n"
                f"👉 Síguenos en @EnigmaIQ para descubrir la verdad detrás de lo cotidiano.\n\n"
                f"#enigmaiq #curiosidades #sabiasque #datoscuriosos #conocimiento #mente #psicologia #aprender"
            )

            res = self.facebook.upload_photo(image_path=img_path, caption=caption)
            Messenger.success(f"Successfully posted standard image to Facebook! ID: {res}")
            self.log_post("image", riddle_idea.question)
            self.sync_to_github()

        except Exception as e:
            Messenger.error(f"Failed to generate/post daily standard image: {e}")
            sys.exit(1)

    def run_daily_mix(self):
        """
        Main execution orchestrator:
        Autonomous EnigmaIQ Video Generation (> 60 seconds) with procedural Remotion graphics,
        vector country silhouettes, geological cuts, and Gemini TTS ("Fenrir").
        """
        post_type = os.getenv("POST_TYPE", "video").lower()

        if post_type == "video":
            env_mode = os.getenv("MODE", "").lower()
            if env_mode:
                mode = env_mode
            else:
                mode = "mecanica"

            forced_topic = os.getenv("TOPIC", "").strip()
            forced_pillar = os.getenv("PILLAR", "").strip()

            if forced_topic:
                Messenger.info(f"🎯 Forced Topic override: '{forced_topic}'")
            if forced_pillar:
                Messenger.info(f"🏛️ Forced Pillar override: '{forced_pillar}'")

            Messenger.info(f"🎬 GENERATING NEW ENIGMAIQ MASTER REEL (> 60s) [Mode: {mode.upper()}]...")

            # Check if user specifically requested an older static composition
            static_compositions = [
                "ElPorqueDeTodoAmazonas", "ElPorqueDeTodoSierraNevada", "ElPorqueDeTodoOrquideas",
                "ElPorqueDeTodoCatatumbo", "ElPorqueDeTodoAjolote", "ElPorqueDeTodoMedusa"
            ]

            try:
                if forced_topic in static_compositions:
                    Messenger.info(f"✨ Executing Legacy Static Composition: '{forced_topic}'...")
                    cmd = [sys.executable, "-m", "flows.image_content_generator.pipeline.master_remotion_publisher", "--composition", forced_topic]
                    subprocess.run(cmd, check=True)
                    last_title = f"Legacy Remotion Reel ({forced_topic})"
                else:
                    # 100% Autonomous AI Remotion Engine (> 60 seconds)
                    Messenger.info("🚀 Launching Autonomous AI Remotion Engine (> 60s procedural render)...")
                    cmd = [sys.executable, "-m", "flows.image_content_generator.pipeline.autonomous_ai_remotion_engine"]
                    if forced_topic:
                        cmd.extend(["--topic", forced_topic])
                    if forced_pillar and forced_pillar != "auto":
                        cmd.extend(["--pillar", forced_pillar])
                    subprocess.run(cmd, check=True)
                    last_title = f"Autonomous AI Remotion Reel ({forced_topic or 'Gemini Autonomous'})"

                Messenger.success(f"✅ EnigmaIQ Reel completed successfully!")
                self.sync_to_github()
            except Exception as e:
                Messenger.error(f"Error during video task: {e}")
                sys.exit(1)
        else:
            self.generate_daily_standard_image()

    def sync_to_github(self):
        """Commits and pushes the history update to prevent repeated topics."""
        try:
            cmd_add = ["git", "add", "flows/image_content_generator/out_short/automated_posts_history.csv"]
            subprocess.run(cmd_add, check=True)
            cmd_commit = ["git", "commit", "-m", "chore: update tracking history [skip ci]"]
            subprocess.run(cmd_commit, check=False)
            cmd_push = ["git", "push"]
            subprocess.run(cmd_push, check=True)
            Messenger.info("Synced tracking history with GitHub.")
        except Exception as e:
            Messenger.warning(f"Could not sync with git: {e}")

if __name__ == "__main__":
    automator = DailyAutomator()
    automator.run_daily_mix()
