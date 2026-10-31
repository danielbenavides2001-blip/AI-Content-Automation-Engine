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
        # 1. Automated history
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()[1:]
                    for line in lines[-10:]:
                        parts = line.strip().split(",")
                        if len(parts) >= 3:
                            topics.append(parts[2])
            except Exception:
                pass
        
        # 2. Video titles history
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

        # Step 1: Generate Riddle Idea using the dedicated system
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

            # Topic Validation
            validator = TopicValidator()
            is_valid, reason = validator.validate(riddle_idea.question, recent_topics)
            if not is_valid:
                Messenger.warning(f"⚠️ Topic rejected: {reason}. Trying with a fallback angle...")
                riddle_idea.question = f"¿Sabías que el 90% de las decisiones de compra no las toma tu lógica?"

            # Step 2: Generate Composite Image
            img_filename = f"daily_curiosity_{riddle_idea.question[:15].strip().replace(' ', '_')}.png"
            # Sanitize filename
            img_filename = "".join(c for c in img_filename if c.isalnum() or c in ('_', '.')).rstrip()
            img_path = self.out_dir / img_filename

            caption_full = riddle_idea.to_facebook_caption()
            
            # Use visual prompt with fallbacks
            visual_prompt = getattr(riddle_idea, 'visual_prompt', '') or riddle_idea.to_image_prompt()
            
            # FreeHybrid handles Pexels search query or Pollinations FLUX automatically
            search_query = getattr(riddle_idea, 'pexels_query', '') or FreeHybridImageGenerator.extract_search_keywords(visual_prompt)

            self.image_gen.generate_composite_image(
                prompt=visual_prompt,
                output_path=img_path,
                top_text="¿SABÍAS QUE...?",
                bottom_text=riddle_idea.question,
                search_query=search_query
            )

            # Step 3: Publish to Facebook Page
            Messenger.info("Publishing Composite Image to Facebook Page...")
            result = self.facebook.publish_photo(
                image_path=str(img_path),
                caption=caption_full
            )
            
            last_title = riddle_idea.question
            Messenger.success("✅ Curiosity Image post completed!")
            self.log_post("image", f"Curiosity Image: {last_title}")
            self.sync_to_github()
        except Exception as e:
            Messenger.error(f"❌ Failed to generate/upload Curiosity Image: {e}")
            sys.exit(1)

    def run_daily_mix(self):
        """
        Main entry point for GitHub Actions.
        Determines type based on POST_TYPE env var.
        """
        post_type = os.getenv("POST_TYPE", "video").lower()
        Messenger.info(f"🚀 Starting Automated Post (Type: {post_type.upper()})...")
        
        self.cleanup_stuck_ideas()

        if post_type == "video":
            env_mode = os.getenv("MODE", "").lower()
            if env_mode:
                mode = env_mode
            else:
                # 100% Remotion Master (mapas vectoriales, cortes transversales, EnigmaIQ)
                mode = "mecanica"
            forced_topic = os.getenv("TOPIC", "").strip()
            if forced_topic:
                Messenger.info(f"🎯 Forced Topic override: '{forced_topic}'")
            Messenger.info(f"🎬 GENERATING NEW CURIOSITY REEL (Full Pipeline | Mode: {mode.upper()})...")
            avoid_msg = self.get_recent_topics()
            try:
                if mode in ["mecanica", "master"]:
                    Messenger.info("✨ Executing EnigmaIQ Master Remotion Publisher...")
                    cmd = [sys.executable, "-m", "flows.image_content_generator.pipeline.master_remotion_publisher"]
                    if forced_topic:
                        cmd.extend(["--composition", forced_topic])
                    subprocess.run(cmd, check=True)
                    last_title = f"EnigmaIQ Master Remotion Reel ({forced_topic or 'Auto'})"
                else:
                    cmd = [sys.executable, "-m", "flows.image_content_generator.pipeline.main", "short", "all", "--avoid", avoid_msg, "--mode", mode]
                    if forced_topic:
                        cmd.extend(["--topic", forced_topic])
                    subprocess.run(cmd, check=True)
                    try:
                        import pandas as pd
                        video_csv = Path("flows/image_content_generator/out_short/ideas_tracking.csv")
                        df = pd.read_csv(video_csv)
                        last_title = df.iloc[-1]["title"]
                    except Exception:
                        last_title = f"Curiosity Reel ({mode})"
                Messenger.success(f"✅ Curiosity Reel ({mode.upper()}) completed!")
                self.log_post("video", last_title)
                self.sync_to_github()
            except Exception as e:
                Messenger.error(f"Error during video task: {e}")
                sys.exit(1)
        else:
            self.generate_daily_standard_image()


    def cleanup_stuck_ideas(self):
        """
        Cleans up incomplete ideas to prevent redundancy.
        Removes both physical folders AND orphan CSV entries (folders already deleted).
        """
        Messenger.info("🧹 Cleaning up stuck or incomplete ideas...")
        ideas_dir = Path("flows/image_content_generator/out_short/ideas")
        video_csv = Path("flows/image_content_generator/out_short/ideas_tracking.csv")

        if not video_csv.exists():
            return

        import shutil
        import pandas as pd

        try:
            df = pd.read_csv(video_csv)
            safe_states = ["UPLOADED", "COMPLETED"]

            # Phase 1: Delete physical folders of non-safe ideas
            if ideas_dir.exists():
                valid_ids = df[df["state"].isin(safe_states)]["id"].tolist()
                for idea_path in ideas_dir.iterdir():
                    if idea_path.is_dir():
                        try:
                            idea_id = int(idea_path.name.split("_")[-1])
                            if idea_id not in valid_ids:
                                Messenger.warning(f"🗑️ Deleting stuck idea folder: {idea_path.name}")
                                shutil.rmtree(idea_path)
                        except (ValueError, IndexError):
                            pass

            # Phase 2: Remove orphan CSV rows whose folders no longer exist
            rows_to_keep = []
            removed_ids = []
            for _, row in df.iterrows():
                idea_id = int(row["id"])
                state = str(row["state"])
                if state in safe_states:
                    rows_to_keep.append(row)
                    continue
                folder_name = f"idea_{idea_id:06d}"
                idea_path = ideas_dir / folder_name
                if idea_path.exists():
                    rows_to_keep.append(row)
                else:
                    removed_ids.append(idea_id)

            if removed_ids:
                Messenger.warning(f"🧹 Removed {len(removed_ids)} orphan rows from ideas_tracking.csv: {removed_ids}")
                df_clean = pd.DataFrame(rows_to_keep)
                df_clean.to_csv(video_csv, index=False)

        except Exception as e:
            Messenger.warning(f"Cleanup non-fatal error: {e}")

    def sync_to_github(self):
        """Commits and pushes the history update to prevent repeated topics."""
        try:
            cmd_add = ["git", "add", "flows/image_content_generator/out_short/automated_posts_history.csv", "flows/image_content_generator/out_short/ideas_tracking.csv"]
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
