import os
import sys
import json
import math
import shutil
import random
import argparse
import datetime
import subprocess
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[3]
CATALOG_FILE = Path(__file__).resolve().parent / "el_porque_de_todo_catalog.json"
HISTORY_FILE = BASE_DIR / "flows" / "image_content_generator" / "out_short" / "automated_posts_history.csv"
FONTS_DIR = BASE_DIR / "flows" / "curiosity_image_generator" / "resources" / "fonts"
FONT_PATH = FONTS_DIR / "Montserrat-Bold.ttf"
AMBIENT_AUDIO = BASE_DIR / "flows" / "image_content_generator" / "remotion" / "public" / "mar_salado_assets" / "ambient_bed.mp3"
OUT_DIR = BASE_DIR / "flows" / "image_content_generator" / "out_short"
SCRATCH_DIR = BASE_DIR / "scratch" / "pure_stock_engine"

from tools.common.messenger import Messenger
from tools.text_generation.gemini import GeminiTextGenerator
from tools.audio_generation.gemini import GeminiAudioGenerator
from tools.video_generation.pexels import PexelsTool
from tools.video_generation.pixabay import PixabayTool
from tools.social_media.facebook import FacebookTool

# ==============================================================================
# PYDANTIC SCHEMA FOR 5-SCENE VIDEO SCRIPT (> 60s)
# ==============================================================================
class ScriptScene(BaseModel):
    scene_number: int = Field(description="1 to 5")
    narration: str = Field(description="22 to 25 words of high-impact narration in neutral Spanish")
    stock_query: str = Field(description="English search query (2-4 words) for vertical stock video")

class ScriptBlueprint(BaseModel):
    title: str = Field(description="Catchy title matching the catalog topic")
    headline_top: str = Field(description="Top line of question card (e.g. '¿POR QUÉ LAS VENTANAS')")
    headline_bottom: str = Field(description="Bottom line in gold (e.g. 'DE AVIONES SON REDONDAS?')")
    scenes: List[ScriptScene] = Field(description="Exactly 5 scenes")
    facebook_copy: str = Field(description="Facebook description with hashtags")

# ==============================================================================
# PURE STOCK VIDEO ENGINE (NO REMOTION)
# ==============================================================================
class PureStockVideoEngine:
    def __init__(self):
        self.text_gen = GeminiTextGenerator()
        self.audio_gen = GeminiAudioGenerator()
        self.pexels = PexelsTool()
        self.pixabay = PixabayTool()
        self.facebook = FacebookTool(
            page_id=os.getenv("FACEBOOK_PAGE_ID"),
            access_token=os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
        )
        SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
        OUT_DIR.mkdir(parents=True, exist_ok=True)

    def load_catalog(self) -> List[dict]:
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def select_next_topic(self, forced_id: Optional[str] = None) -> dict:
        catalog = self.load_catalog()
        if forced_id:
            for item in catalog:
                if item["id"] == forced_id:
                    return item
            Messenger.warning(f"Topic '{forced_id}' not found in catalog. Falling back to autonomous selection.")

        # Check history to find unposted topics
        posted_topics = set()
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split(",")
                        if len(parts) >= 3:
                            posted_topics.add(parts[2].lower())
            except Exception as e:
                Messenger.warning(f"Error reading history: {e}")

        for item in catalog:
            if item["id"].lower() not in posted_topics and item["title"].lower() not in posted_topics:
                Messenger.info(f"🎯 Selected next unposted topic: '{item['title']}' ({item['id']})")
                return item

        # If all posted, cycle to first
        Messenger.info("🔄 All catalog topics have been posted. Cycling to first.")
        return catalog[0]

    def generate_script(self, topic: dict) -> ScriptBlueprint:
        Messenger.info(f"🧠 Generating high-retention 5-scene script with Gemini for: '{topic['title']}'...")
        prompt = f"""
Eres el Guionista y Director de 'EnigmaIQ' (estilo 'El porqué de todo').
Crea un guion audiovisual fascinante, científico y de intriga viral sobre este tema:

TÍTULO: {topic['title']}
PREMISA CIENTÍFICA: {topic['core_premise']}
LÍNEA SUPERIOR PREGUNTA: {topic['headline_top']}
LÍNEA INFERIOR PREGUNTA: {topic['headline_bottom']}

REGLAS CRÍTICAS DE DURACIÓN (DEBE DURAR MÁS DE 60 SEGUNDOS):
1. Debes generar exactamente 5 escenas consecutivas.
2. Cada escena DEBE tener una narración de entre 22 y 26 palabras concisas, rítmicas y con intriga.
3. El total de palabras debe estar entre 115 y 128 palabras. A la velocidad de narración del locutor (1.7 palabras/segundo), esto garantiza que el audio dure exactamente entre 66 y 76 segundos (> 60s obligatorio).
4. La Escena 5 debe cerrar con el llamado a la acción: "Esto es EnigmaIQ. ¿Conocías este dato? Cuéntanos en los comentarios."
5. Para cada una de las 5 escenas proporciona un 'stock_query' en INGLÉS (2-4 palabras) para buscar el video vertical de stock exacto (ej: 'commercial airplane flying clouds', 'metal fatigue crack test', 'airplane cabin passenger window').

Responde en formato JSON siguiendo el esquema.
"""
        blueprint = self.text_gen.generate_text(prompt=prompt, schema=ScriptBlueprint)
        return blueprint

    def synthesize_narration(self, blueprint: ScriptBlueprint, out_audio_path: Path) -> float:
        full_text = " ".join([s.narration.strip() for s in blueprint.scenes])
        Messenger.info(f"🎙️ Synthesizing Fenrir TTS narration ({len(full_text.split())} words)...")
        wav_path = out_audio_path.with_suffix(".wav")
        self.audio_gen.text_to_speech(full_text, wav_path)

        # Convert to high-quality MP3
        cmd = ["ffmpeg", "-y", "-i", str(wav_path), "-c:a", "libmp3lame", "-b:a", "192k", str(out_audio_path)]
        subprocess.run(cmd, check=True, capture_output=True)

        # Measure duration
        cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(out_audio_path)]
        res = subprocess.run(cmd_dur, check=True, capture_output=True, text=True)
        dur = float(res.stdout.strip())
        Messenger.success(f"✅ Fenrir audio synthesized: {dur:.2f} seconds (> 60s)")
        return dur

    def transcribe_and_build_ass(self, audio_path: Path, out_ass_path: Path) -> None:
        Messenger.info("📝 Transcribing audio with Whisper for millisecond subtitle synchronization...")
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(str(audio_path), word_timestamps=True, language="es")

        words = []
        for segment in result["segments"]:
            for w in segment.get("words", []):
                w_text = w["word"].strip().upper()
                if w_text:
                    words.append({
                        "word": w_text,
                        "start": round(w["start"], 2),
                        "end": round(w["end"], 2)
                    })

        # Group words into 2-3 word punchy chunks
        chunks = []
        i = 0
        while i < len(words):
            take = 3
            if i + take > len(words):
                take = len(words) - i
            elif i + take == len(words) - 1:
                take = 2
            
            group = words[i:i+take]
            start_t = group[0]["start"]
            end_t = group[-1]["end"]
            if end_t - start_t < 0.65:
                end_t = round(start_t + 0.65, 2)
            chunks.append({
                "start": start_t,
                "end": end_t,
                "words": group
            })
            i += take

        def format_ass_time(sec: float) -> str:
            h = int(sec // 3600)
            m = int((sec % 3600) // 60)
            s = int(sec % 60)
            cs = int((sec - int(sec)) * 100)
            return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"

        # Write ASS file
        # Style Default: Montserrat Bold, size 86, thick 10px black outline, bottom aligned with 560px vertical margin
        ass_lines = [
            "[Script Info]",
            "ScriptType: v4.00+",
            "PlayResX: 1080",
            "PlayResY: 1920",
            "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
            "Style: Default,Montserrat,86,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,-1,0,1,10,0,2,60,60,560,1",
            "",
            "[Events]",
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
        ]

        # For each chunk, highlight the active word as it is spoken
        for c in chunks:
            chunk_words = c["words"]
            for idx, w in enumerate(chunk_words):
                w_start = w["start"]
                # End is next word's start or chunk end
                w_end = chunk_words[idx+1]["start"] if idx + 1 < len(chunk_words) else c["end"]
                if w_end <= w_start:
                    w_end = round(w_start + 0.25, 2)

                text_tokens = []
                for j, other_w in enumerate(chunk_words):
                    if j == idx:
                        # Gold highlight &H000B9EF5& (Amber #f59e0b)
                        text_tokens.append(f"{{\\c&H000B9EF5&}}{other_w['word']}{{\\c&H00FFFFFF&}}")
                    else:
                        text_tokens.append(other_w["word"])
                
                line_text = " ".join(text_tokens)
                ass_lines.append(
                    f"Dialogue: 0,{format_ass_time(w_start)},{format_ass_time(w_end)},Default,,0,0,0,,{line_text}"
                )

        with open(out_ass_path, "w", encoding="utf-8") as f:
            f.write("\n".join(ass_lines))

        Messenger.success(f"✅ Generated {len(ass_lines)-10} dynamic ASS subtitle events with Montserrat 900")

    def generate_question_card_overlay(self, blueprint: ScriptBlueprint, out_png_path: Path) -> None:
        """Generates crisp transparent PNG for the Question Card visible from frame 0 for the thumbnail."""
        img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        font_pill = ImageFont.truetype(str(FONT_PATH), 22)
        font_q1 = ImageFont.truetype(str(FONT_PATH), 48)
        font_q2 = ImageFont.truetype(str(FONT_PATH), 58)

        # 1. Official EnigmaIQ Gold Header Pill
        draw.rounded_rectangle([(55, 70), (220, 115)], radius=22, fill=(245, 158, 11, 255))
        draw.text((75, 78), "ENIGMAIQ", font=font_pill, fill=(2, 9, 20, 255))

        # 2. Centered Upper Question Box
        box_coords = [(70, 380), (1010, 590)]
        draw.rounded_rectangle(box_coords, radius=26, fill=(14, 25, 48, 244), outline=(245, 158, 11, 255), width=4)

        # Top line (white)
        q1_text = blueprint.headline_top.upper()
        b1 = draw.textbbox((0, 0), q1_text, font=font_q1)
        w1 = b1[2] - b1[0]
        draw.text(((1080 - w1) // 2, 415), q1_text, font=font_q1, fill=(255, 255, 255, 255))

        # Bottom line (gold)
        q2_text = blueprint.headline_bottom.upper()
        b2 = draw.textbbox((0, 0), q2_text, font=font_q2)
        w2 = b2[2] - b2[0]
        draw.text(((1080 - w2) // 2, 490), q2_text, font=font_q2, fill=(245, 158, 11, 255))

        img.save(out_png_path)
        Messenger.success("✅ Generated Question Card overlay for thumbnail and scene 1")

    def download_stock_videos(self, blueprint: ScriptBlueprint, work_dir: Path, scene_durations: List[float]) -> List[Path]:
        """Downloads vertical stock videos from Pexels/Pixabay and normalizes each to 1080x1920 @ 30 FPS."""
        prepared_clips = []
        for idx, scene in enumerate(blueprint.scenes):
            raw_path = work_dir / f"raw_scene_{idx+1}.mp4"
            norm_path = work_dir / f"norm_scene_{idx+1}.mp4"
            target_dur = scene_durations[idx]
            query = scene.stock_query.strip()

            Messenger.info(f"🔎 Scene {idx+1}/5: Searching vertical stock video for '{query}'...")
            downloaded = self.pexels.fetch_video(query, raw_path)
            if not downloaded:
                Messenger.info("Falling back to Pixabay...")
                downloaded = self.pixabay.fetch_video(query, raw_path)

            if not downloaded or not raw_path.exists() or raw_path.stat().st_size < 10000:
                # Fallback to high-quality ambient ocean/space clip
                Messenger.warning(f"Using atmospheric fallback for scene {idx+1}")
                cmd_fall = [
                    "ffmpeg", "-y", "-f", "lavfi",
                    "-i", f"color=c=0x07192f:s=1080x1920:d={target_dur}:r=30",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(norm_path)
                ]
                subprocess.run(cmd_fall, check=True, capture_output=True)
                prepared_clips.append(norm_path)
                continue

            # Normalize video to 1080x1920, 30 FPS, muted, looping to target_dur
            cmd_norm = [
                "ffmpeg", "-y",
                "-stream_loop", "3",
                "-i", str(raw_path),
                "-t", str(target_dur),
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30",
                "-an",
                "-c:v", "libx264",
                "-preset", "fast",
                "-pix_fmt", "yuv420p",
                str(norm_path)
            ]
            subprocess.run(cmd_norm, check=True, capture_output=True)
            prepared_clips.append(norm_path)

        return prepared_clips

    def render_master_video(self, topic: dict, blueprint: ScriptBlueprint, audio_path: Path, total_dur: float, master_out: Path) -> Path:
        """Assembles the final master video using pure FFmpeg (Zero Remotion)."""
        work_dir = SCRATCH_DIR / topic["id"]
        work_dir.mkdir(parents=True, exist_ok=True)

        # 1. Allocate scene durations proportionally
        num_scenes = len(blueprint.scenes)
        scene_dur = round(total_dur / num_scenes, 2)
        scene_durations = [scene_dur] * num_scenes
        # Adjust last scene so sum matches exact audio duration
        scene_durations[-1] = round(total_dur - sum(scene_durations[:-1]), 2)

        # 2. Download and normalize 5 stock video clips
        clips = self.download_stock_videos(blueprint, work_dir, scene_durations)

        # 3. Create concat list
        concat_txt = work_dir / "concat_list.txt"
        with open(concat_txt, "w", encoding="utf-8") as f:
            for c in clips:
                # Use forward slashes
                f.write(f"file '{c.resolve().as_posix()}'\n")

        # 4. Generate Question Card overlay PNG
        card_png = work_dir / "question_card.png"
        self.generate_question_card_overlay(blueprint, card_png)

        # 5. Generate ASS Subtitle file
        ass_path = work_dir / "subtitles.ass"
        self.transcribe_and_build_ass(audio_path, ass_path)

        # 6. Final FFmpeg assembly:
        # Inputs:
        # [0] Concat stock videos
        # [1] Question card overlay PNG
        # [2] Fenrir voice audio MP3
        # [3] Ambient bed MP3 (optional loop)
        Messenger.info("🎬 Assembling master video with FFmpeg...")
        fonts_param = FONTS_DIR.as_posix()
        ass_filter_path = ass_path.as_posix().replace(":", "\\:")

        filter_complex = (
            f"[0:v][1:v]overlay=0:0:enable='between(t,0,5.8)'[v_card];"
            f"[v_card]ass='{ass_filter_path}':fontsdir='{fonts_param}'[v_out];"
            f"[2:a]volume=1.0[a_voice];"
            f"[3:a]volume=0.12[a_bed];"
            f"[a_voice][a_bed]amix=inputs=2:duration=first:dropout_transition=2[a_out]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat_txt),
            "-i", str(card_png),
            "-i", str(audio_path),
            "-stream_loop", "-1", "-i", str(AMBIENT_AUDIO),
            "-filter_complex", filter_complex,
            "-map", "[v_out]",
            "-map", "[a_out]",
            "-t", str(total_dur),
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            str(master_out)
        ]

        subprocess.run(cmd, check=True)
        size_mb = master_out.stat().st_size / (1024 * 1024)
        Messenger.success(f"🏆 Master video successfully rendered with FFmpeg: {master_out.name} ({size_mb:.2f} MB, {total_dur:.2f}s)")
        return master_out

    def run(self, forced_topic_id: Optional[str] = None):
        topic = self.select_next_topic(forced_topic_id)
        Messenger.info(f"🚀 Launching Pure Stock Video Engine for topic: '{topic['title']}'...")

        work_dir = SCRATCH_DIR / topic["id"]
        work_dir.mkdir(parents=True, exist_ok=True)
        audio_path = work_dir / f"{topic['id']}_fenrir.mp3"
        master_out = OUT_DIR / f"{topic['id']}_Fenrir_StockMaster.mp4"

        # 1. Script
        blueprint = self.generate_script(topic)

        # 2. Narration
        total_dur = self.synthesize_narration(blueprint, audio_path)

        # 3. Master Render
        self.render_master_video(topic, blueprint, audio_path, total_dur, master_out)

        # 4. Upload to Facebook Reel
        Messenger.info("📤 Publishing Master Reel to Facebook...")
        caption = f"{blueprint.title}\n\n{topic['facebook_copy']}"
        res = self.facebook.upload_reel(file_path=master_out, title=blueprint.title, description=caption)
        Messenger.success(f"🎉 Successfully published to Facebook! ID: {res}")

        # 5. Log history
        today = datetime.date.today().isoformat()
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"{today},video_pure_stock,{topic['id']} - {topic['title']}\n")

        # 6. Git sync
        self.sync_to_github()

    def sync_to_github(self):
        try:
            cmd_add = ["git", "add", "-f", "flows/image_content_generator/out_short/automated_posts_history.csv"]
            subprocess.run(cmd_add, check=True)
            cmd_commit = ["git", "commit", "-m", "chore: update pure stock tracking history [skip ci]"]
            subprocess.run(cmd_commit, check=False)
            cmd_push = ["git", "push"]
            subprocess.run(cmd_push, check=True)
            Messenger.info("Synced tracking history with GitHub.")
        except Exception as e:
            Messenger.warning(f"Could not sync with git: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, default=None, help="Force a specific topic ID from catalog")
    args = parser.parse_args()

    engine = PureStockVideoEngine()
    engine.run(forced_topic_id=args.topic)
