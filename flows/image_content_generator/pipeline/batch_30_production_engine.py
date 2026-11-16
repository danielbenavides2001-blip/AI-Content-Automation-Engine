import os
import sys
import json
import time
import shutil
import subprocess
import re
from pathlib import Path

# Setup paths
BASE_DIR = Path(r"C:\Users\Vanes\.gemini\antigravity\scratch\AI-Content-Automation-Engine1")
sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

from tools.common.messenger import Messenger
from tools.video_generation.media_hub import MediaHub
from tools.audio_generation.voicebox_client import VoiceboxClient
from PIL import Image, ImageDraw, ImageFont

FONTS_DIR = BASE_DIR / "flows" / "curiosity_image_generator" / "resources" / "fonts"
FONT_PATH = FONTS_DIR / "Montserrat-Bold.ttf"
AMBIENT_AUDIO = BASE_DIR / "flows" / "image_content_generator" / "remotion" / "public" / "mar_salado_assets" / "ambient_bed.mp3"
DOWNLOADS_DIR = Path(r"C:\Users\Vanes\Downloads\Videos_EnigmaIQ_Editados")
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
REPO_PRE_DIR = BASE_DIR / "flows" / "image_content_generator" / "out_short" / "pre_rendered"
REPO_PRE_DIR.mkdir(parents=True, exist_ok=True)
SCRATCH_DIR = BASE_DIR / "scratch" / "batch_30_production"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
QUEUE_FILE = BASE_DIR / "flows" / "image_content_generator" / "out_short" / "next_queued_action.json"
CATALOG_FILE = BASE_DIR / "flows" / "image_content_generator" / "pipeline" / "curiosities_30_catalog.json"

XPRESSTV_PROFILE_ID = "e294f4c2-3dc3-42af-bfa5-51a6492a28b9"

def sanitize_card_text(text: str) -> str:
    """Strips all emoji and unsupported unicode glyphs to completely eliminate tofu boxes."""
    return re.sub(r'[\U00010000-\U0010ffff\u2600-\u27bf\u2300-\u23ff\u2b50\u200d\ufe0f]', '', text).strip()

def get_video_duration(path: Path) -> float:
    try:
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, check=True
        )
        return float(res.stdout.strip())
    except Exception:
        return 0.0

def format_ass_time(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int((sec - int(sec)) * 100)
    return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"

def generate_intro_card(video: dict, out_png: Path):
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font_pill = ImageFont.truetype(str(FONT_PATH), 22)
    font_category = ImageFont.truetype(str(FONT_PATH), 20)
    font_top = ImageFont.truetype(str(FONT_PATH), 42)
    font_bottom = ImageFont.truetype(str(FONT_PATH), 48)

    # 1. EnigmaIQ Gold Header Pill
    draw.rounded_rectangle([(65, 75), (235, 120)], radius=22, fill=(245, 158, 11, 255))
    draw.text((85, 83), "ENIGMAIQ", font=font_pill, fill=(2, 9, 20, 255))

    box_w = 940
    box_x0 = (1080 - box_w) // 2
    box_x1 = box_x0 + box_w
    box_y0 = 360
    box_y1 = 570

    # Navy glass card with amber border
    draw.rounded_rectangle([(box_x0, box_y0), (box_x1, box_y1)], radius=28, fill=(14, 25, 48, 246), outline=(245, 158, 11, 255), width=4)

    # Category badge
    cat_text = sanitize_card_text(video.get("category", "5 CURIOSIDADES VIRALES")).upper()
    cat_b = draw.textbbox((0, 0), cat_text, font=font_category)
    cat_w = cat_b[2] - cat_b[0]
    cat_x0 = (1080 - cat_w - 36) // 2
    draw.rounded_rectangle([(cat_x0, box_y0 - 18), (cat_x0 + cat_w + 36, box_y0 + 18)], radius=18, fill=(245, 158, 11, 255))
    draw.text((cat_x0 + 18, box_y0 - 11), cat_text, font=font_category, fill=(2, 9, 20, 255))

    # Top & bottom lines
    t_top = sanitize_card_text(video["headline_top"])
    b_top = draw.textbbox((0, 0), t_top, font=font_top)
    draw.text(((1080 - (b_top[2] - b_top[0])) // 2, box_y0 + 55), t_top, font=font_top, fill=(255, 255, 255, 255))

    t_bot = sanitize_card_text(video["headline_bottom"])
    b_bot = draw.textbbox((0, 0), t_bot, font=font_bottom)
    draw.text(((1080 - (b_bot[2] - b_bot[0])) // 2, box_y0 + 120), t_bot, font=font_bottom, fill=(245, 158, 11, 255))

    img.save(out_png)

def generate_persistent_header(out_png: Path):
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_pill = ImageFont.truetype(str(FONT_PATH), 22)
    draw.rounded_rectangle([(65, 75), (235, 120)], radius=22, fill=(245, 158, 11, 255))
    draw.text((85, 83), "ENIGMAIQ", font=font_pill, fill=(2, 9, 20, 255))
    img.save(out_png)

def transcribe_and_make_ass(audio_path: Path, out_ass: Path):
    import whisper
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("base", device=device)
    res = model.transcribe(str(audio_path), word_timestamps=True, language="es")
    
    words = []
    for s in res.get("segments", []):
        for w in s.get("words", []):
            txt = w["word"].strip().upper()
            if txt:
                words.append({"word": txt, "start": round(w["start"], 2), "end": round(w["end"], 2)})

    chunks = []
    i = 0
    while i < len(words):
        group = words[i:i+3]
        start_t = group[0]["start"]
        end_t = max(group[-1]["end"], start_t + 0.6)
        chunks.append({"start": start_t, "end": end_t, "words": group})
        i += len(group)

    lines = [
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

    for c in chunks:
        c_words = c["words"]
        for idx, w in enumerate(c_words):
            w_start = w["start"]
            w_end = c_words[idx+1]["start"] if idx + 1 < len(c_words) else c["end"]
            if w_end <= w_start: w_end = round(w_start + 0.25, 2)
            
            tokens = []
            for j, ow in enumerate(c_words):
                if j == idx:
                    tokens.append(f"{{\\c&H000B9EF5&}}{ow['word']}{{\\c&H00FFFFFF&}}")
                else:
                    tokens.append(ow["word"])
            line_str = " ".join(tokens)
            lines.append(f"Dialogue: 0,{format_ass_time(w_start)},{format_ass_time(w_end)},Default,,0,0,0,,{line_str}")

    with open(out_ass, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def produce_single_video(video: dict, media_hub: MediaHub, vb_client: VoiceboxClient) -> Path:
    final_dest = DOWNLOADS_DIR / f"{video['id']}.mp4"
    repo_dest = REPO_PRE_DIR / f"{video['id']}.mp4"

    # Strict check: Video must exist AND be >= 60.0s to skip
    if final_dest.exists() and final_dest.stat().st_size > 12 * 1024 * 1024:
        v_dur = get_video_duration(final_dest)
        if v_dur >= 60.0:
            Messenger.success(f"Video already rendered and valid (>60s): {final_dest.name} ({v_dur:.1f}s)")
            if not repo_dest.exists() or repo_dest.stat().st_size != final_dest.stat().st_size:
                shutil.copy(final_dest, repo_dest)
            return final_dest
        else:
            Messenger.warning(f"Video {final_dest.name} is {v_dur:.1f}s (<60s). Re-rendering to comply with >60s monetization rule...")

    work_dir = SCRATCH_DIR / video["id"]
    work_dir.mkdir(parents=True, exist_ok=True)
    Messenger.info(f"\n==========================================")
    Messenger.info(f"Produciendo Master: {video['id']}")
    Messenger.info(f"Tema: {video['title']}")
    Messenger.info(f"==========================================")

    # 1. Preparar lista de 12 escenas
    scenes = [
        {"narration": "¡Cinco cosas completamente asombrosas que probablemente no sabías hace apenas un minuto!", "query": "fast clock countdown ticking", "fallback": "hourglass sand falling macro"}
    ]
    for c in video["curiosities"]:
        p1 = c.get("p1")
        p2 = c.get("p2")
        if not p1 or not p2:
            words = c["text"].split()
            mid = len(words) // 2
            p1 = " ".join(words[:mid])
            p2 = " ".join(words[mid:])
        scenes.append({"narration": p1, "query": c["q1"], "fallback": c["q2"]})
        scenes.append({"narration": p2, "query": c["q2"], "fallback": c["q1"]})
    scenes.append({
        "narration": "¿Cuál de estas cinco curiosidades te sorprendió más? Déjanos tu opinión en los comentarios y sigue a EnigmaIQ.",
        "query": "dramatic golden sunset clouds landscape",
        "fallback": "cinematic sunset time lapse sky"
    })

    # 2. Audio Synthesis via Voicebox CUDA
    full_narration = " ".join([s["narration"] for s in scenes])
    audio_wav = work_dir / "narration.wav"
    dur = vb_client.synthesize_full_narration(full_narration, audio_wav)
    Messenger.success(f"🎙️ Audio con Voz XpressTV (CUDA): {dur:.2f}s (Regla > 60s cumplida: {dur >= 60.0})")

    # 3. Subtítulos ASS sincronizados
    ass_path = work_dir / f"{video['id']}.ass"
    transcribe_and_make_ass(audio_wav, ass_path)

    # 4. Descarga y normalización de los 12 clips
    num_scenes = len(scenes)
    dur_per_scene = round(dur / num_scenes, 2)
    scene_durations = [dur_per_scene] * num_scenes
    scene_durations[-1] = round(dur - sum(scene_durations[:-1]), 2)

    clips = []
    for idx, sc in enumerate(scenes):
        raw_clip = work_dir / f"raw_scene_{idx+1}.mp4"
        norm_clip = work_dir / f"norm_scene_{idx+1}.mp4"
        t_dur = scene_durations[idx]
        
        q = sc["query"]
        if not raw_clip.exists() or raw_clip.stat().st_size < 10000:
            ok = media_hub.fetch_best_clip(query=q, out_path=raw_clip, scene_topic=sc["narration"], duration=t_dur)
            if not ok or not raw_clip.exists() or raw_clip.stat().st_size < 10000:
                fallback_q = sc["fallback"]
                media_hub.fetch_best_clip(query=fallback_q, out_path=raw_clip, scene_topic=sc["narration"], duration=t_dur)

        # Normalizar con FFmpeg a 1080x1920 30fps
        cmd_norm = [
            "ffmpeg", "-y", "-stream_loop", "3", "-i", str(raw_clip),
            "-t", str(t_dur),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30",
            "-an", "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
            str(norm_clip)
        ]
        subprocess.run(cmd_norm, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=str(BASE_DIR))
        clips.append(norm_clip)

    concat_txt = work_dir / "concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in clips:
            f.write(f"file '{c.resolve().as_posix()}'\n")

    # 5. Overlays con texto 100% sanitizado (CERO cajas o errores de glifos)
    card_png = work_dir / "intro_card.png"
    generate_intro_card(video, card_png)

    header_png = work_dir / "persistent_header.png"
    generate_persistent_header(header_png)

    # 6. Render Maestro FFmpeg
    try:
        rel_fonts = FONTS_DIR.relative_to(BASE_DIR).as_posix()
    except Exception:
        rel_fonts = FONTS_DIR.as_posix().replace(":", "\\:")
    try:
        rel_ass = ass_path.relative_to(BASE_DIR).as_posix()
    except Exception:
        rel_ass = ass_path.as_posix().replace(":", "\\:")

    filter_complex = (
        f"[0:v][1:v]overlay=0:0:enable='between(t,0,5.2)'[v_card];"
        f"[v_card][2:v]overlay=0:0[v_head];"
        f"[v_head]ass='{rel_ass}':fontsdir='{rel_fonts}'[v_out];"
        f"[3:a]volume=1.0[a_voice];"
        f"[4:a]volume=0.12[a_bed];"
        f"[a_voice][a_bed]amix=inputs=2:duration=first:dropout_transition=2[a_out]"
    )

    cmd_master = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-i", str(card_png),
        "-i", str(header_png),
        "-i", str(audio_wav),
        "-stream_loop", "-1", "-i", str(AMBIENT_AUDIO),
        "-filter_complex", filter_complex,
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-t", str(dur),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "25",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        str(final_dest)
    ]
    Messenger.info("🎬 Ensamblando master final con FFmpeg...")
    subprocess.run(cmd_master, check=True, cwd=str(BASE_DIR))
    
    sz_mb = final_dest.stat().st_size / (1024 * 1024)
    Messenger.success(f"🎉 MASTER CREADO CON ÉXITO: {final_dest.name} ({sz_mb:.1f} MB, {dur:.2f}s)")
    shutil.copy(final_dest, repo_dest)
    return final_dest

def sync_queue_and_git(rendered_videos: list):
    """Updates next_queued_action.json and pushes to GitHub in safe increments."""
    queue_data = {"pre_rendered_queue": []}
    if QUEUE_FILE.exists():
        try:
            with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                queue_data = json.load(f)
        except Exception:
            pass

    existing_paths = {item.get("file_path") for item in queue_data.get("pre_rendered_queue", [])}
    new_files = []
    for v in rendered_videos:
        rel_path = f"flows/image_content_generator/out_short/pre_rendered/{v['id']}.mp4"
        if rel_path not in existing_paths:
            queue_data["pre_rendered_queue"].append({
                "file_path": rel_path,
                "title": v["title"],
                "description": v["description"]
            })
            existing_paths.add(rel_path)
        new_files.append(rel_path)

    queue_data["note"] = "Cola secuencial de videos originales (5 curiosidades por video) con voz XpressTV y branding EnigmaIQ."
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue_data, f, indent=2, ensure_ascii=False)

    Messenger.success(f"✅ Cola actualizada en next_queued_action.json ({len(queue_data['pre_rendered_queue'])} videos en cola).")

    # Safe Git Commit & Push
    try:
        git_add_cmd = ["git", "add", "flows/image_content_generator/out_short/next_queued_action.json"]
        for rf in new_files:
            full_rf = BASE_DIR / rf
            if full_rf.exists():
                git_add_cmd.append(rf)
        subprocess.run(git_add_cmd, check=True, cwd=str(BASE_DIR))
        
        status_res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=str(BASE_DIR))
        if status_res.stdout.strip():
            video_ids = ", ".join([v["id"] for v in rendered_videos])
            subprocess.run(["git", "commit", "-m", f"feat: queue video {video_ids} [skip ci]"], check=True, cwd=str(BASE_DIR))
            subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True, cwd=str(BASE_DIR))
            subprocess.run(["git", "push", "origin", "main"], check=True, cwd=str(BASE_DIR))
            Messenger.success(f"🚀 Video {video_ids} subido con éxito a GitHub origin/main!")
    except Exception as ge:
        Messenger.warning(f"⚠️ Git push warning: {ge}")

def main():
    Messenger.info("🚀 Iniciando Motor de Producción en Lote (Voz XpressTV + Duración >60s + Tarjeta Sanitizada)...")
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    media_hub = MediaHub()
    vb_client = VoiceboxClient(profile_id=XPRESSTV_PROFILE_ID)

    rendered = []
    # Process batch
    for v in catalog:
        try:
            produce_single_video(v, media_hub, vb_client)
            rendered.append(v)
            # Sync to queue and push after each video
            sync_queue_and_git([v])
        except Exception as e:
            Messenger.error(f"Falla produciendo video {v['id']}: {e}")
            import traceback
            traceback.print_exc()

    Messenger.success("🎉 LOTE DE PRODUCCIÓN COMPLETADO CON ÉXITO.")

if __name__ == "__main__":
    main()
