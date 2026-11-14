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
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
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
from tools.video_generation.media_hub import MediaHub
from tools.social_media.facebook import FacebookTool

# ==============================================================================
# PYDANTIC SCHEMA FOR 5-SCENE VIDEO SCRIPT (> 60s)
# ==============================================================================
class ScriptScene(BaseModel):
    scene_number: int = Field(description="1 to 5")
    narration: str = Field(description="22 to 25 words of high-impact narration in neutral Spanish")
    stock_query: str = Field(description="English search query (2-4 words) for vertical stock video")

class CatalogItemSchema(BaseModel):
    id: str = Field(description="Unique snake_case slug without spaces")
    title: str = Field(description="Viral curiosity question title with emojis")
    headline_top: str = Field(description="Top line of question card (e.g. '¿POR QUÉ EL AGUA CALIENTE')")
    headline_bottom: str = Field(description="Bottom line in gold (e.g. 'SE CONGELA MÁS RÁPIDO?')")
    category: str = Field(description="Category (e.g. 'FÍSICA & TERMODINÁMICA', 'BIOLOGÍA & CUERPO', etc.)")
    core_premise: str = Field(description="2-3 sentences explaining the rigorous scientific mechanism in simple words")
    facebook_copy: str = Field(description="Engaging caption for Facebook with hashtags")
    stock_queries: List[str] = Field(description="5 English search queries for vertical stock video clips")

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
        self.media_hub = MediaHub()
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
        history_text = ""
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    history_text = f.read().lower()
            except Exception as e:
                Messenger.warning(f"Error reading history: {e}")

        for item in catalog:
            item_id = item["id"].lower()
            item_title = item["title"].lower()
            if item_id not in history_text and item_title not in history_text:
                Messenger.info(f"🎯 Selected next unposted topic: '{item['title']}' ({item['id']})")
                return item

        # If all predefined catalog topics have been published, autonomously generate a brand-new topic with Gemini!
        Messenger.info("🧠 All predefined catalog topics have been published! Autonomously conceiving a brand-new viral topic with Gemini...")
        new_topic = self.generate_autonomous_topic(history_text)
        catalog.append(new_topic)
        try:
            with open(CATALOG_FILE, "w", encoding="utf-8") as f:
                json.dump(catalog, f, indent=2, ensure_ascii=False)
            Messenger.success(f"💾 Persisted new autonomous topic to catalog: '{new_topic['title']}'")
        except Exception as e:
            Messenger.warning(f"Could not persist new topic to catalog: {e}")
        return new_topic

    def generate_autonomous_topic(self, history_text: str) -> dict:
        """Autonomously researches and conceives a brand-new, non-repeated topic with Gemini."""
        prompt = f"""Eres el Investigador y Director Científico de 'EnigmaIQ' (estilo 'El porqué de todo' en Facebook Reels).
Diseña 1 tema fascinante y 100% original sobre una curiosidad científica cotidiana, física, medicina, ingeniería o fenómenos naturales que la gente da por sentados.

Temas e historial reciente que NO debes repetir bajo ninguna circunstancia:
{history_text[-2500:]}

Reglas estrictas:
1. Plantea una pregunta intrigante de la vida cotidiana o fenómeno científico.
2. Formato exacto JSON según el esquema CatalogItemSchema.
3. Proporciona 5 consultas precisas en inglés para clips de video vertical (stock) que muestren exactamente lo que se va a narrar.
"""
        item_schema = self.text_gen.generate_text(prompt=prompt, schema=CatalogItemSchema)
        return item_schema.model_dump()

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

REGLA DE ORO DE CONGRUENCIA VISUAL ABSOLUTA (SIN MARGEN DE ERROR):
5. CADA ESCENA DEBE MOSTRAR EXACTAMENTE LO QUE SE ESTÁ NARRANDO. Cero margen de error.
   - Si la narración menciona una acción (abrir nevera, café cayendo, avión volando, hielo derritiéndose, gato saltando), el metraje DEBE mostrar esa acción u objeto literal en primer plano.
   - Prohibido usar metáforas abstractas o conceptos difusos.
   - En el campo 'stock_query' de cada escena escribe una búsqueda en INGLÉS (2-4 palabras) hiper-específica y directa que garantice metraje cinematográfico vertical en Pexels/Pixabay.

Responde en formato JSON siguiendo el esquema.
"""
        blueprint = self.text_gen.generate_text(prompt=prompt, schema=ScriptBlueprint)
        return blueprint

    def synthesize_narration(self, blueprint: ScriptBlueprint, out_audio_path: Path) -> float:
        full_text = " ".join([s.narration.strip() for s in blueprint.scenes])
        Messenger.info(f"🎙️ Synthesizing narration ({len(full_text.split())} words)...")
        wav_path = out_audio_path.with_suffix(".wav")
        try:
            self.audio_gen.text_to_speech(full_text, wav_path)
            # Convert to high-quality MP3
            cmd = ["ffmpeg", "-y", "-i", str(wav_path), "-c:a", "libmp3lame", "-b:a", "192k", str(out_audio_path)]
            subprocess.run(cmd, check=True, capture_output=True)
            Messenger.success("✅ Fenrir TTS narration generated.")
        except Exception as e:
            Messenger.warning(f"⚠️ Gemini TTS no disponible ({e}). Activando Neural Fallback (es-CO-GonzaloNeural)...")
            import asyncio
            import edge_tts
            async def _run_edge():
                comm = edge_tts.Communicate(full_text, "es-CO-GonzaloNeural", rate="+3%")
                await comm.save(str(out_audio_path))
            asyncio.run(_run_edge())
            Messenger.success("✅ Neural Fallback audio generated.")

        # Measure duration
        cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(out_audio_path)]
        res = subprocess.run(cmd_dur, check=True, capture_output=True, text=True)
        dur = float(res.stdout.strip())
        Messenger.success(f"✅ Audio duration: {dur:.2f} seconds")
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

        # Measure pixel width to ensure ZERO subtitle overflow (safe width <= 840px)
        font_sub = ImageFont.truetype(str(FONT_PATH), 76)
        dummy_draw = ImageDraw.Draw(Image.new("RGBA", (1080, 1920)))
        MAX_SUB_WIDTH = 840

        chunks = []
        i = 0
        while i < len(words):
            group = [words[i]]
            for next_idx in range(i + 1, min(i + 3, len(words))):
                test_str = " ".join([w["word"] for w in group + [words[next_idx]]])
                b = dummy_draw.textbbox((0, 0), test_str, font=font_sub)
                if b[2] - b[0] <= MAX_SUB_WIDTH:
                    group.append(words[next_idx])
                else:
                    break

            start_t = group[0]["start"]
            end_t = group[-1]["end"]
            if end_t - start_t < 0.65:
                end_t = round(start_t + 0.65, 2)
            chunks.append({
                "start": start_t,
                "end": end_t,
                "words": group
            })
            i += len(group)

        def format_ass_time(sec: float) -> str:
            h = int(sec // 3600)
            m = int((sec % 3600) // 60)
            s = int(sec % 60)
            cs = int((sec - int(sec)) * 100)
            return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"

        # Write ASS file
        # Style Default: Montserrat Bold, size 76, 9px black outline, bottom aligned with 540px vertical margin, 90px left/right margins
        ass_lines = [
            "[Script Info]",
            "ScriptType: v4.00+",
            "PlayResX: 1080",
            "PlayResY: 1920",
            "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
            "Style: Default,Montserrat,76,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,-1,0,1,9,0,2,90,90,540,1",
            "",
            "[Events]",
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
        ]

        # For each chunk, highlight the active word as it is spoken
        for c in chunks:
            chunk_words = c["words"]
            for idx, w in enumerate(chunk_words):
                w_start = w["start"]
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

        Messenger.success(f"✅ Generated {len(ass_lines)-10} dynamic ASS subtitle events (Safe width <= 840px, size 76)")

    def generate_question_card_overlay(self, topic: dict, blueprint: ScriptBlueprint, out_png_path: Path) -> None:
        """Generates crisp transparent PNG for the Question Card with dynamic auto-wrapping and auto-sizing."""
        img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        font_pill = ImageFont.truetype(str(FONT_PATH), 22)
        font_category = ImageFont.truetype(str(FONT_PATH), 20)

        # 1. Official EnigmaIQ Gold Header Pill
        draw.rounded_rectangle([(65, 75), (235, 120)], radius=22, fill=(245, 158, 11, 255))
        draw.text((85, 83), "ENIGMAIQ", font=font_pill, fill=(2, 9, 20, 255))

        # Safe text width: box width is 940 (70 to 1010), internal padding 50px -> max text width = 830px
        max_text_width = 830

        top_text = (blueprint.headline_top or topic.get("headline_top", "")).strip().upper()
        bottom_text = (blueprint.headline_bottom or topic.get("headline_bottom", "")).strip().upper()

        def wrap_to_width(txt: str, fnt: ImageFont.FreeTypeFont) -> list:
            words = txt.split()
            lines = []
            curr = []
            for w in words:
                test_str = " ".join(curr + [w])
                bbox = draw.textbbox((0, 0), test_str, font=fnt)
                if bbox[2] - bbox[0] <= max_text_width:
                    curr.append(w)
                else:
                    if curr:
                        lines.append(" ".join(curr))
                        curr = [w]
                    else:
                        lines.append(w)
                        curr = []
            if curr:
                lines.append(" ".join(curr))
            return lines

        size_top = 44
        size_bottom = 54
        font_top = ImageFont.truetype(str(FONT_PATH), size_top)
        font_bottom = ImageFont.truetype(str(FONT_PATH), size_bottom)

        top_lines = wrap_to_width(top_text, font_top)
        bottom_lines = wrap_to_width(bottom_text, font_bottom)

        if len(top_lines) + len(bottom_lines) > 4:
            size_top = 38
            size_bottom = 46
            font_top = ImageFont.truetype(str(FONT_PATH), size_top)
            font_bottom = ImageFont.truetype(str(FONT_PATH), size_bottom)
            top_lines = wrap_to_width(top_text, font_top)
            bottom_lines = wrap_to_width(bottom_text, font_bottom)

        line_spacing = 16
        gap_between = 22

        total_text_h = 0
        top_metrics = []
        for line in top_lines:
            b = draw.textbbox((0, 0), line, font=font_top)
            w = b[2] - b[0]
            h = b[3] - b[1]
            top_metrics.append((w, h))
            total_text_h += h + line_spacing
        total_text_h -= line_spacing

        total_text_h += gap_between

        bottom_metrics = []
        for line in bottom_lines:
            b = draw.textbbox((0, 0), line, font=font_bottom)
            w = b[2] - b[0]
            h = b[3] - b[1]
            bottom_metrics.append((w, h))
            total_text_h += h + line_spacing
        total_text_h -= line_spacing

        pad_y = 48
        box_w = 940
        box_x0 = (1080 - box_w) // 2  # 70
        box_x1 = box_x0 + box_w       # 1010
        box_h = total_text_h + pad_y * 2

        # Center box vertically around Y = 460
        box_y0 = 460 - box_h // 2
        box_y1 = box_y0 + box_h

        # Draw card box with deep navy glass fill and crisp amber outline
        draw.rounded_rectangle([(box_x0, box_y0), (box_x1, box_y1)], radius=28, fill=(14, 25, 48, 246), outline=(245, 158, 11, 255), width=4)

        # Draw category badge centered above top edge of box
        cat_text = topic.get("category", "CIENCIA & MISTERIOS").upper()
        cat_b = draw.textbbox((0, 0), cat_text, font=font_category)
        cat_w = cat_b[2] - cat_b[0]
        cat_pill_w = cat_w + 36
        cat_x0 = (1080 - cat_pill_w) // 2
        cat_y0 = box_y0 - 18
        draw.rounded_rectangle([(cat_x0, cat_y0), (cat_x0 + cat_pill_w, cat_y0 + 36)], radius=18, fill=(245, 158, 11, 255))
        draw.text((cat_x0 + 18, cat_y0 + 7), cat_text, font=font_category, fill=(2, 9, 20, 255))

        # Render top lines (white)
        curr_y = box_y0 + pad_y
        for i, line in enumerate(top_lines):
            w, h = top_metrics[i]
            draw.text(((1080 - w) // 2, curr_y), line, font=font_top, fill=(255, 255, 255, 255))
            curr_y += h + line_spacing
        curr_y -= line_spacing

        curr_y += gap_between

        # Render bottom lines (gold)
        for i, line in enumerate(bottom_lines):
            w, h = bottom_metrics[i]
            draw.text(((1080 - w) // 2, curr_y), line, font=font_bottom, fill=(245, 158, 11, 255))
            curr_y += h + line_spacing

        img.save(out_png_path)
        Messenger.success(f"✅ Generated Auto-Fit Question Card ({box_w}x{box_h}px, {len(top_lines)+len(bottom_lines)} lines) for thumbnail")

    def download_stock_videos(self, topic: dict, blueprint: ScriptBlueprint, work_dir: Path, scene_durations: List[float]) -> List[Path]:
        """Downloads vertical clips using MediaHub multi-source cascade matching narration with zero margin of error."""
        prepared_clips = []
        curated_queries = topic.get("stock_queries", [])
        scene_topic = topic.get("title", "")

        for idx, scene in enumerate(blueprint.scenes):
            raw_path = work_dir / f"raw_scene_{idx+1}.mp4"
            norm_path = work_dir / f"norm_scene_{idx+1}.mp4"
            target_dur = scene_durations[idx]

            # Priority query cascade: Curated queries tested for visual congruence come first
            candidate_queries = []
            if idx < len(curated_queries) and curated_queries[idx].strip():
                candidate_queries.append(curated_queries[idx].strip())
            if scene.stock_query and scene.stock_query.strip():
                candidate_queries.append(scene.stock_query.strip())

            downloaded = False
            for q in candidate_queries:
                Messenger.info(f"🔎 Scene {idx+1}/5: Searching visual clip for '{q}' via MediaHub...")
                downloaded = self.media_hub.fetch_best_clip(
                    query=q,
                    out_path=raw_path,
                    scene_topic=scene_topic,
                    duration=target_dur
                )
                if downloaded and raw_path.exists() and raw_path.stat().st_size > 10000:
                    Messenger.success(f"🎬 Scene {idx+1}/5: Exact visual match obtained for narration: '{q}'")
                    break

            if not downloaded or not raw_path.exists() or raw_path.stat().st_size < 10000:
                core_fallback = topic.get("id", "").replace("_", " ")
                Messenger.warning(f"Trying core topic search: '{core_fallback}'")
                downloaded = self.media_hub.fetch_best_clip(
                    query=core_fallback,
                    out_path=raw_path,
                    scene_topic=scene_topic,
                    duration=target_dur
                )

            # Ensure raw_path exists or synthesize Ken Burns clip
            if not downloaded or not raw_path.exists() or raw_path.stat().st_size < 10000:
                Messenger.warning(f"Using emergency visual generator for scene {idx+1}")
                self.media_hub.generative.generate_clip(
                    f"{scene.narration[:60]}, vertical documentary 4k",
                    raw_path,
                    duration=target_dur
                )

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
        clips = self.download_stock_videos(topic, blueprint, work_dir, scene_durations)

        # 3. Create concat list
        concat_txt = work_dir / "concat_list.txt"
        with open(concat_txt, "w", encoding="utf-8") as f:
            for c in clips:
                # Use forward slashes
                f.write(f"file '{c.resolve().as_posix()}'\n")

        # 4. Generate Question Card overlay PNG
        card_png = work_dir / "question_card.png"
        self.generate_question_card_overlay(topic, blueprint, card_png)

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
        try:
            rel_fonts = FONTS_DIR.relative_to(BASE_DIR).as_posix()
        except Exception:
            rel_fonts = FONTS_DIR.as_posix().replace(":", "\\:")
        try:
            rel_ass = ass_path.relative_to(BASE_DIR).as_posix()
        except Exception:
            rel_ass = ass_path.as_posix().replace(":", "\\:")

        filter_complex = (
            f"[0:v][1:v]overlay=0:0:enable='between(t,0,5.8)'[v_card];"
            f"[v_card]ass='{rel_ass}':fontsdir='{rel_fonts}'[v_out];"
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

    def run(self, forced_topic_id: Optional[str] = None, skip_upload: bool = False, copy_to: Optional[str] = None):
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

        # Copy to custom folder if specified
        if copy_to:
            dest_dir = Path(copy_to)
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_file = dest_dir / master_out.name
            shutil.copy2(master_out, dest_file)
            Messenger.success(f"📂 Master video copied to: {dest_file}")

        # 4. Upload to Facebook Reel (if not skipped)
        if not skip_upload:
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
        else:
            Messenger.info("⏭️ Skip-upload requested: video rendered locally and not published to Facebook.")

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
    parser.add_argument("--skip-upload", action="store_true", help="Skip Facebook upload and git sync")
    parser.add_argument("--copy-to", type=str, default=None, help="Copy final video to target directory")
    args = parser.parse_args()

    engine = PureStockVideoEngine()
    engine.run(forced_topic_id=args.topic, skip_upload=args.skip_upload, copy_to=args.copy_to)
