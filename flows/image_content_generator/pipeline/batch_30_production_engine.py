import os
import sys
import json
import time
import shutil
import subprocess
import re
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Setup paths
BASE_DIR = Path(__file__).resolve().parents[3]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

from tools.common.messenger import Messenger
from tools.video_generation.media_hub import MediaHub
from tools.video_generation.ai_image_master import AIImageMaster
from tools.audio_generation.voicebox_client import VoiceboxClient
from tools.social_media.facebook import FacebookTool
from PIL import Image, ImageDraw, ImageFont

FONTS_DIR = BASE_DIR / "flows" / "curiosity_image_generator" / "resources" / "fonts"
FONT_PATH = FONTS_DIR / "Montserrat-Bold.ttf"
AMBIENT_AUDIO = BASE_DIR / "flows" / "image_content_generator" / "remotion" / "public" / "mar_salado_assets" / "ambient_bed.mp3"
REPO_PRE_DIR = BASE_DIR / "flows" / "image_content_generator" / "out_short" / "pre_rendered"
REPO_PRE_DIR.mkdir(parents=True, exist_ok=True)
SCRATCH_DIR = BASE_DIR / "scratch" / "batch_30_production"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
SHARED_CACHE_DIR = BASE_DIR / "scratch" / "shared_clip_cache"
SHARED_CACHE_DIR.mkdir(parents=True, exist_ok=True)
QUEUE_FILE = BASE_DIR / "flows" / "image_content_generator" / "out_short" / "next_queued_action.json"
CATALOG_FILE = BASE_DIR / "flows" / "image_content_generator" / "pipeline" / "curiosities_30_catalog.json"
HISTORY_FILE = BASE_DIR / "flows" / "image_content_generator" / "out_short" / "automated_posts_history.csv"

# Cloud-compatible output directory (works in GitHub Actions Ubuntu and local PC)
if os.getenv("GITHUB_ACTIONS") == "true" or os.getenv("CI") == "true":
    DOWNLOADS_DIR = REPO_PRE_DIR
else:
    DOWNLOADS_DIR = Path(r"C:\Users\Vanes\Downloads\Videos_EnigmaIQ_Editados")
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

XPRESSTV_PROFILE_ID = "e294f4c2-3dc3-42af-bfa5-51a6492a28b9"

# Singleton Whisper model for zero reloading latency
_GLOBAL_WHISPER_MODEL = None

def get_whisper_model():
    global _GLOBAL_WHISPER_MODEL
    if _GLOBAL_WHISPER_MODEL is None:
        import whisper
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        Messenger.info(f"⚡ [Whisper] Inicializando modelo en memoria ({device})...")
        _GLOBAL_WHISPER_MODEL = whisper.load_model("base", device=device)
    return _GLOBAL_WHISPER_MODEL

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
    t0 = time.time()
    try:
        model = get_whisper_model()
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
        Messenger.info(f"  ⚡ [Subtítulos ASS] Generados en {time.time()-t0:.2f}s ({len(words)} palabras)")
    except Exception as e:
        Messenger.warning(f"⚠️ [Whisper] Advertencia en subtítulos: {e}. Generando plantilla ASS de seguridad...")
        fallback_lines = [
            "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
            "Style: Default,Montserrat,76,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,-1,0,1,9,0,2,90,90,540,1", "",
            "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
        ]
        with open(out_ass, "w", encoding="utf-8") as f:
            f.write("\n".join(fallback_lines))

def get_dynamic_intro(video: dict) -> dict:
    """
    Generates a dynamic narrative hook and visual query derived DIRECTLY
    from the curiosities of this specific video. The opening visual doubles as the
    high-impact thumbnail on Facebook Reels (eliminating any clock completely).
    """
    import random
    title = video.get("title", "")
    curiosities = video.get("curiosities", [])
    
    h_top = sanitize_card_text(video.get("headline_top", "")).strip()
    h_bottom = sanitize_card_text(video.get("headline_bottom", "")).strip()
    
    narration_options = [
        f"¡{h_top.capitalize()} {h_bottom.lower()} que cambiarán por completo cómo ves el mundo!",
        f"¡{h_top.capitalize()} {h_bottom.lower()} que la gran mayoría de personas desconoce!",
        f"¡{h_top.capitalize()} {h_bottom.lower()} que desafían todo lo que creías saber!",
        f"¡{h_top.capitalize()} {h_bottom.lower()} que te dejarán con la boca abierta!"
    ]
    narration = random.choice(narration_options)

    # Metraje y Miniatura: Extraído DIRECTAMENTE de las curiosidades de este video
    if curiosities:
        c1 = curiosities[0]
        base_q = c1.get("q1", "").strip()
        fallback = c1.get("q2", "").strip()
        if base_q:
            query = f"{base_q} cinematic 4k"
        else:
            query = f"{title} cinematic vertical"
    else:
        query = f"{title} cinematic vertical"
        fallback = "dramatic scientific discovery cinematic"

    return {
        "narration": narration,
        "query": query,
        "fallback": fallback,
        "is_intro": True  # NUNCA reutilizar en caché compartida
    }

    return {
        "narration": narration,
        "query": query,
        "fallback": fallback,
        "is_intro": True
    }

def get_dynamic_outro() -> dict:
    import random
    outro_queries = [
        {"q": "earth from space sunset golden hour cinematic", "fb": "planet earth orbit sunrise"},
        {"q": "starry night sky milky way timelapse cinematic", "fb": "galaxy stars moving night"},
        {"q": "neon glowing particle vortex abstract 4k", "fb": "futuristic technology digital background"},
        {"q": "cinematic sunset time lapse mountain landscape", "fb": "golden hour clouds flying drone"}
    ]
    pick = random.choice(outro_queries)
    return {
        "narration": "¿Cuál de estas cinco curiosidades te sorprendió más? Déjanos tu opinión en los comentarios y sigue a EnigmaIQ.",
        "query": pick["q"],
        "fallback": pick["fb"],
        "is_intro": False
    }

def fetch_and_norm_scene(idx: int, sc: dict, t_dur: float, work_dir: Path, media_hub: MediaHub) -> Path:
    raw_clip = work_dir / f"raw_scene_{idx+1}.mp4"
    norm_clip = work_dir / f"norm_scene_{idx+1}.mp4"

    is_intro = sc.get("is_intro", False)
    q = sc["query"].strip()
    cache_key = hashlib.md5(f"{q}_{round(t_dur, 1)}".encode("utf-8")).hexdigest()
    cached_file = SHARED_CACHE_DIR / f"{cache_key}.mp4"

    # 1. Reusar de la caché compartida global (EXCEPTO si es la escena de intro)
    if not is_intro and cached_file.exists() and cached_file.stat().st_size > 50000:
        shutil.copy(cached_file, norm_clip)
        return norm_clip

    # 2. Descargar video si no existe localmente
    if not raw_clip.exists() or raw_clip.stat().st_size < 10000:
        ok = media_hub.fetch_best_clip(query=q, out_path=raw_clip, scene_topic=sc["narration"], duration=t_dur)
        if not ok or not raw_clip.exists() or raw_clip.stat().st_size < 10000:
            fallback_q = sc["fallback"]
            media_hub.fetch_best_clip(query=fallback_q, out_path=raw_clip, scene_topic=sc["narration"], duration=t_dur)

    # 3. Normalizar con FFmpeg a 1080x1920 30fps ultrafast si tenemos raw_clip
    if raw_clip.exists() and raw_clip.stat().st_size >= 10000:
        cmd_norm = [
            "ffmpeg", "-y", "-stream_loop", "3", "-i", str(raw_clip),
            "-t", str(t_dur),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30",
            "-an", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
            str(norm_clip)
        ]
        subprocess.run(cmd_norm, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=str(BASE_DIR))
        if norm_clip.exists() and norm_clip.stat().st_size > 10000:
            if not is_intro:
                try:
                    shutil.copy(norm_clip, cached_file)
                except Exception:
                    pass
            return norm_clip

    # 4. Respaldo definitivo infalible: Fotografía HD de Pexels/Pixabay animada con Ken Burns
    Messenger.info(f"📸 [Scene {idx+1}] Obteniendo fotografía de rescate para '{q}'...")
    from tools.video_generation.ai_image_master import AIImageMaster
    ai_master = AIImageMaster()
    temp_photo = work_dir / f"fallback_photo_{idx+1}.jpg"
    ok_photo = ai_master.fetch_stock_photo(q, temp_photo) or ai_master.fetch_stock_photo(sc.get("fallback", ""), temp_photo)
    if ok_photo and temp_photo.exists() and temp_photo.stat().st_size > 5000:
        if ai_master.create_ken_burns_clip(temp_photo, norm_clip, duration=t_dur, motion_style=idx):
            return norm_clip

    # 5. Si todas las redes fallaran, reutilizar una imagen previa generada en el video para evitar pantalla negra
    existing_imgs = list(work_dir.glob("*.jpg"))
    if existing_imgs:
        ai_master.create_ken_burns_clip(existing_imgs[0], norm_clip, duration=t_dur, motion_style=idx)
        return norm_clip

    return norm_clip

def produce_single_video(video: dict, media_hub: MediaHub, vb_client: VoiceboxClient, force: bool = False) -> Path:
    start_v = time.time()
    final_dest = DOWNLOADS_DIR / f"{video['id']}.mp4"
    repo_dest = REPO_PRE_DIR / f"{video['id']}.mp4"

    # Strict check: Video must exist AND be >= 60.0s to skip (a menos que se fuerce re-render)
    if not force and final_dest.exists() and final_dest.stat().st_size > 12 * 1024 * 1024:
        v_dur = get_video_duration(final_dest)
        if v_dur >= 60.0:
            Messenger.success(f"Video already rendered and valid (>60s): {final_dest.name} ({v_dur:.1f}s)")
            if not repo_dest.exists() or repo_dest.stat().st_size != final_dest.stat().st_size:
                shutil.copy(final_dest, repo_dest)
            return final_dest
        else:
            Messenger.warning(f"Video {final_dest.name} is {v_dur:.1f}s (<60s). Re-rendering to comply with >60s monetization rule...")

    work_dir = SCRATCH_DIR / video["id"]
    if force and work_dir.exists():
        shutil.rmtree(work_dir, ignore_errors=True)
    work_dir.mkdir(parents=True, exist_ok=True)
    Messenger.info(f"\n==========================================")
    Messenger.info(f"Produciendo Master: {video['id']}")
    Messenger.info(f"Tema: {video['title']}")
    Messenger.info(f"==========================================")

    # 1. Preparar lista de 12 escenas con Gancho de Intro Dinámico y Outro Variado
    intro_scene = get_dynamic_intro(video)
    intro_q = intro_scene["query"].strip()
    intro_vp = video.get("intro_visual_prompt") or f"Cinematic vertical 9:16 macro documentary shot of {intro_q}, dramatic lighting, 8k resolution, photorealistic, sharp focus"
    intro_scene["visual_prompt"] = intro_vp

    outro_scene = get_dynamic_outro()
    outro_q = outro_scene["query"].strip()
    outro_vp = video.get("outro_visual_prompt") or f"Cinematic vertical 9:16 shot of {outro_q}, golden bokeh, dramatic studio lighting, 8k resolution, photorealistic"
    outro_scene["visual_prompt"] = outro_vp

    scenes = [intro_scene]
    for c in video["curiosities"]:
        p1 = c.get("p1")
        p2 = c.get("p2")
        if not p1 or not p2:
            words = c["text"].split()
            mid = len(words) // 2
            p1 = " ".join(words[:mid])
            p2 = " ".join(words[mid:])

        q1 = c.get("q1", "").strip()
        q2 = c.get("q2", "").strip()

        # Ingeniería de Prompts Visuales de Alta Precisión:
        # Usa descriptores en inglés del catálogo ('q1' y 'q2') enriquecidos cinematográficamente
        vp1 = c.get("visual_prompt_1") or (
            f"Cinematic vertical 9:16 documentary photograph of {q1}, dramatic cinematic lighting, "
            f"National Geographic 8k, hyper-detailed, photorealistic, sharp focus, masterpiece"
        )
        vp2 = c.get("visual_prompt_2") or (
            f"Cinematic vertical 9:16 documentary photograph of {q2}, dramatic cinematic lighting, "
            f"National Geographic 8k, hyper-detailed, photorealistic, sharp focus, masterpiece"
        )

        scenes.append({"narration": p1, "visual_prompt": vp1, "query": q1, "fallback": q2, "is_intro": False})
        scenes.append({"narration": p2, "visual_prompt": vp2, "query": q2, "fallback": q1, "is_intro": False})
    scenes.append(outro_scene)

    # =========================================================================
    # PIPELINE FASE 1: Voz Realista en Nube (Edge-TTS / rany2)
    # =========================================================================
    full_narration = " ".join([s["narration"] for s in scenes])
    audio_wav = work_dir / "narration.wav"
    ass_path = work_dir / f"{video['id']}.ass"

    Messenger.info("⚡ [PIPELINE] Sintetizando voz realista (Edge-TTS)...")
    dur = vb_client.synthesize_full_narration(full_narration, audio_wav)
    Messenger.success(f"🎙️ Audio con Voz Realista: {dur:.2f}s (Cumple > 60s: {dur >= 60.0})")

    # =========================================================================
    # PIPELINE FASE 2: Subtítulos ASS + Generación Visual con FLUX.1 / Imagen 3 + Ken Burns
    # =========================================================================
    num_scenes = len(scenes)
    dur_per_scene = round(dur / num_scenes, 2)
    scene_durations = [dur_per_scene] * num_scenes
    scene_durations[-1] = round(dur - sum(scene_durations[:-1]), 2)

    ai_master = AIImageMaster()
    Messenger.info("🎨 [IA VISUAL MASTER] Generando escenas con FLUX.1 (Gradio) / Imagen 3 + Movimiento Ken Burns...")

    def make_ai_scene(idx_sc):
        idx, sc = idx_sc
        clip_path = work_dir / f"norm_scene_{idx+1}.mp4"
        sc_dur = scene_durations[idx]
        vp = sc.get("visual_prompt", "")
        q = sc.get("query", "")
        fb = sc.get("fallback", "")
        if clip_path.exists() and clip_path.stat().st_size > 10000:
            return clip_path
        Messenger.info(f"  🎬 [Escena {idx+1}/{len(scenes)}] Generando visual de la curiosidad: '{q}' (Estilo {idx%4})...")
        ok = ai_master.generate_ken_burns_scene(
            vp, clip_path, duration=sc_dur, motion_style=idx, work_dir=work_dir, query=q, fallback_query=fb
        )
        if not ok or not clip_path.exists() or clip_path.stat().st_size < 10000:
            norm_res = fetch_and_norm_scene(idx, sc, sc_dur, work_dir, media_hub)
            if norm_res.exists() and norm_res != clip_path:
                shutil.copy(norm_res, clip_path)
        return clip_path

    with ThreadPoolExecutor(max_workers=2) as executor:
        ass_future = executor.submit(transcribe_and_make_ass, audio_wav, ass_path)
        clips = list(executor.map(make_ai_scene, enumerate(scenes)))
        ass_future.result()

    concat_txt = work_dir / "concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in clips:
            f.write(f"file '{c.resolve().as_posix()}'\n")

    # 3. Overlays con texto 100% sanitizado
    card_png = work_dir / "intro_card.png"
    generate_intro_card(video, card_png)

    header_png = work_dir / "persistent_header.png"
    generate_persistent_header(header_png)

    # =========================================================================
    # FASE 3: Render Maestro Acelerado con GPU NVENC (NVIDIA RTX 2070)
    # =========================================================================
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

    # Dynamic encoder: NVENC on local PC GPU, libx264 ultrafast on GitHub Actions CPU
    is_ci = os.getenv("GITHUB_ACTIONS") == "true" or os.getenv("CI") == "true"
    has_nvenc = False
    if not is_ci:
        try:
            r = subprocess.run(["ffmpeg", "-encoders"], capture_output=True, text=True)
            has_nvenc = "h264_nvenc" in r.stdout
        except Exception:
            has_nvenc = False

    if has_nvenc:
        v_codec = ["-c:v", "h264_nvenc", "-preset", "p4", "-cq", "23"]
        Messenger.info("🎬 [FFmpeg NVENC] Ensamblando master final en GPU a máxima velocidad...")
    else:
        v_codec = ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "23"]
        Messenger.info("🎬 [FFmpeg CPU] Ensamblando master final en CPU (modo nube / GitHub Actions)...")

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
        *v_codec,
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        str(final_dest)
    ]
    t_render_start = time.time()
    subprocess.run(cmd_master, check=True, cwd=str(BASE_DIR))
    Messenger.info(f"  ⚡ Renderizado final completado en {time.time()-t_render_start:.2f}s!")

    sz_mb = final_dest.stat().st_size / (1024 * 1024)
    total_time = time.time() - start_v
    Messenger.success(f"🎉 MASTER CREADO CON ÉXITO: {final_dest.name} ({sz_mb:.1f} MB, {dur:.2f}s) en {total_time:.1f}s!")
    if final_dest.resolve() != repo_dest.resolve():
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
    # In GitHub Actions cloud run, the workflow itself handles git commit and push
    if os.getenv("GITHUB_ACTIONS") == "true" or os.getenv("CI") == "true":
        Messenger.info("☁️ [Cloud CI] Sincronización git delegada al workflow de GitHub Actions.")
        return

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
    import argparse
    parser = argparse.ArgumentParser(description="EnigmaIQ Production Engine (Local PC or GitHub Actions Cloud)")
    parser.add_argument("--single", action="store_true", help="Produce only 1 pending video from catalog (ideal for GitHub Actions)")
    parser.add_argument("--upload", action="store_true", help="Upload directly to Facebook Reels upon completion")
    parser.add_argument("--video-id", type=str, default="", help="Force specific video ID to produce")
    parser.add_argument("--force", action="store_true", help="Force re-rendering even if already cached")
    args = parser.parse_args()

    Messenger.info("🚀 Iniciando Motor de Producción EnigmaIQ (Multi-plataforma Local / Cloud CI)...")
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    media_hub = MediaHub()
    vb_client = VoiceboxClient(profile_id=XPRESSTV_PROFILE_ID)
    get_whisper_model()

    # Cargar historial para no repetir videos ya publicados en Facebook
    posted_titles = set()
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8", errors="ignore") as hf:
                for line in hf.readlines()[1:]:
                    parts = line.strip().split(",")
                    if len(parts) >= 3:
                        norm = re.sub(r'[^a-zA-Z0-9]', '', parts[2].lower())
                        if norm:
                            posted_titles.add(norm)
        except Exception:
            pass

    if args.single:
        # Modo Nube / GitHub Actions: busca el PRIMER video que NO haya sido publicado todavía
        target_video = None
        for v in catalog:
            if args.video_id:
                if v["id"] == args.video_id:
                    target_video = v
                    break
                continue
            norm_title = re.sub(r'[^a-zA-Z0-9]', '', v["title"].lower())
            if norm_title in posted_titles:
                continue
            target_video = v
            break

        if not target_video:
            Messenger.warning("⚠️ Todos los videos del catálogo ya fueron procesados una vez. Reiniciando ciclo continuo para nunca detener las publicaciones...")
            target_video = catalog[0]

        Messenger.info(f"🎯 [Modo Single Cloud] Produciendo video objetivo: {target_video['id']} - '{target_video['title']}'...")
        master_file = produce_single_video(target_video, media_hub, vb_client, force=args.force)

        if args.upload and master_file and master_file.exists():
            Messenger.info(f"🚀 [Meta API] Subiendo Reel generado en la nube a Facebook: {master_file.name}...")
            fb = FacebookTool(
                page_id=os.getenv("FACEBOOK_PAGE_ID", ""),
                access_token=os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
            )
            try:
                res_id = fb.upload_reel(
                    file_path=master_file,
                    title=target_video["title"],
                    description=target_video.get("description", "")
                )
                Messenger.success(f"🎉 Reel publicado con éxito desde GitHub Actions! Video ID: {res_id}")
                
                # Registrar en historial
                import datetime
                today = datetime.date.today().isoformat()
                clean_title = target_video["title"].replace(",", " - ").strip()
                with open(HISTORY_FILE, "a", encoding="utf-8") as hf:
                    hf.write(f"{today},video,{clean_title}\n")
            except Exception as e:
                Messenger.error(f"Falla subiendo a Facebook: {e}")
                sys.exit(1)

        sync_queue_and_git([target_video])
        Messenger.success(f"🎉 Video {target_video['id']} completado y sincronizado con éxito desde GitHub Actions.")
        return

    # Modo Lote (por defecto local):
    rendered = []
    for v in catalog:
        try:
            produce_single_video(v, media_hub, vb_client)
            rendered.append(v)
            sync_queue_and_git([v])
        except Exception as e:
            Messenger.error(f"Falla produciendo video {v['id']}: {e}")
            import traceback
            traceback.print_exc()

    Messenger.success("🎉 LOTE DE PRODUCCIÓN COMPLETADO CON ÉXITO.")

if __name__ == "__main__":
    main()
