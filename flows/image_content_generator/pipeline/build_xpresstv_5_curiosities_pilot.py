import os
import sys
import json
import time
import shutil
import subprocess
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
SCRATCH_DIR = BASE_DIR / "scratch" / "pilot_5_curiosities"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

XPRESSTV_PROFILE_ID = "e294f4c2-3dc3-42af-bfa5-51a6492a28b9"

VIDEO_META = {
    "id": "21_EnigmaIQ_5_Cosas_Que_No_Sabias_Vol1",
    "title": "5 Cosas que NO sabías hace un minuto 🤯⏳",
    "headline_top": "5 COSAS ASOMBROSAS QUE",
    "headline_bottom": "NO SABÍAS HACE UN MINUTO 🤯",
    "category": "CURIOSIDADES DEL MUNDO",
    "description": "5 Cosas y datos curiosos que te volarán la cabeza en menos de un minuto 🤯 Desde el color real de los espejos hasta el secreto del parche pirata.\n\n#EnigmaIQ #XpressTV #Curiosidades #DatosCuriosos #Aprender #Ciencia #SabiasQue #Misterios"
}

# 12 Scene Cuts across 5 Curiosities + Intro & Outro
SCENES = [
    # Intro
    {
        "segment": "INTRO",
        "narration": "¡Cinco cosas alucinantes que probablemente no sabías hace apenas un minuto!",
        "query": "fast clock countdown ticking",
        "fallback": "hourglass sand falling macro"
    },
    # Dato 1: Espejos verdes
    {
        "segment": "DATO 1/5",
        "narration": "Número uno. Aunque creas que un espejo es plateado, en realidad es verde.",
        "query": "woman looking in mirror reflection",
        "fallback": "person face mirror bathroom"
    },
    {
        "segment": "DATO 1/5",
        "narration": "Al rebotar en un túnel de espejos infinitos, la luz se absorbe y el fondo siempre se torna verde oscuro.",
        "query": "infinity mirror tunnel green lights",
        "fallback": "optical laser neon tunnel"
    },
    # Dato 2: Parche pirata
    {
        "segment": "DATO 2/5",
        "narration": "Número dos. Los piratas no usaban parche por ser tuertos, sino para tener un ojo adaptado a la oscuridad.",
        "query": "old pirate ship sailing ocean waves",
        "fallback": "wooden ship deck sea storm"
    },
    {
        "segment": "DATO 2/5",
        "narration": "Al abordar y saltar a las bodegas enemigas, se cambiaban el parche y veían perfectamente al instante.",
        "query": "human eye pupil dilating dark close up",
        "fallback": "dark wooden ship hold lantern"
    },
    # Dato 3: Ojos no se congelan
    {
        "segment": "DATO 3/5",
        "narration": "Número tres. Aunque estés en el Polo Norte a cuarenta grados bajo cero, tus ojos jamás se congelarán.",
        "query": "snowstorm blizzard freezing winter face",
        "fallback": "polar explorer winter snow heavy"
    },
    {
        "segment": "DATO 3/5",
        "narration": "Las sales y grasas de tus lágrimas, junto al calor de tu sangre, evitan que se forme hielo en ellos.",
        "query": "eye blinking close up macro tears",
        "fallback": "human eye iris detail macro"
    },
    # Dato 4: Petricor y el tiburón
    {
        "segment": "DATO 4/5",
        "narration": "Número cuatro. El olor a tierra mojada se llama petricor.",
        "query": "rain drops falling dry soil slow motion",
        "fallback": "heavy rain green forest leaves"
    },
    {
        "segment": "DATO 4/5",
        "narration": "Tu nariz es tan sensible a esta bacteria que puedes detectarla mejor que un tiburón oliendo sangre en el océano.",
        "query": "shark swimming deep blue ocean water",
        "fallback": "tiger shark underwater marine life"
    },
    # Dato 5: Los huesos de los bebés
    {
        "segment": "DATO 5/5",
        "narration": "Número cinco. Un bebé nace con aproximadamente trescientos huesos blandos.",
        "query": "cute baby crawling playing happy",
        "fallback": "newborn baby small feet close up"
    },
    {
        "segment": "DATO 5/5",
        "narration": "De adulto solo tienes doscientos seis. ¿A dónde fueron los demás? No desaparecieron, se fusionaron al crecer.",
        "query": "medical x-ray skeleton human bones 3d",
        "fallback": "human skeleton anatomy medical model"
    },
    # Outro
    {
        "segment": "OUTRO",
        "narration": "¿Cuál de estos datos te voló más la cabeza? Cuéntanos en los comentarios y síguenos en EnigmaIQ.",
        "query": "dramatic golden sunset clouds landscape",
        "fallback": "cinematic sunset time lapse sky"
    }
]

def format_ass_time(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int((sec - int(sec)) * 100)
    return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"

import re

def sanitize_card_text(text: str) -> str:
    return re.sub(r'[\U00010000-\U0010ffff\u2600-\u27bf\u2300-\u23ff\u2b50\u200d\ufe0f]', '', text).strip()

def generate_intro_card(out_png: Path):
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font_pill = ImageFont.truetype(str(FONT_PATH), 22)
    font_category = ImageFont.truetype(str(FONT_PATH), 20)
    font_top = ImageFont.truetype(str(FONT_PATH), 42)
    font_bottom = ImageFont.truetype(str(FONT_PATH), 48)

    # Header pill
    draw.rounded_rectangle([(65, 75), (235, 120)], radius=22, fill=(245, 158, 11, 255))
    draw.text((85, 83), "ENIGMAIQ", font=font_pill, fill=(2, 9, 20, 255))

    box_w = 940
    box_x0 = (1080 - box_w) // 2
    box_x1 = box_x0 + box_w
    box_y0 = 360
    box_y1 = 570

    # Glass card
    draw.rounded_rectangle([(box_x0, box_y0), (box_x1, box_y1)], radius=28, fill=(14, 25, 48, 246), outline=(245, 158, 11, 255), width=4)

    # Category badge
    cat_text = "5 CURIOSIDADES VIRALES"
    cat_b = draw.textbbox((0, 0), cat_text, font=font_category)
    cat_w = cat_b[2] - cat_b[0]
    cat_x0 = (1080 - cat_w - 36) // 2
    draw.rounded_rectangle([(cat_x0, box_y0 - 18), (cat_x0 + cat_w + 36, box_y0 + 18)], radius=18, fill=(245, 158, 11, 255))
    draw.text((cat_x0 + 18, box_y0 - 11), cat_text, font=font_category, fill=(2, 9, 20, 255))

    # Top & bottom lines (sanitized to remove any emojis causing tofu boxes)
    t_top = sanitize_card_text(VIDEO_META["headline_top"])
    b_top = draw.textbbox((0, 0), t_top, font=font_top)
    draw.text(((1080 - (b_top[2] - b_top[0])) // 2, box_y0 + 55), t_top, font=font_top, fill=(255, 255, 255, 255))

    t_bot = sanitize_card_text(VIDEO_META["headline_bottom"])
    b_bot = draw.textbbox((0, 0), t_bot, font=font_bottom)
    draw.text(((1080 - (b_bot[2] - b_bot[0])) // 2, box_y0 + 120), t_bot, font=font_bottom, fill=(245, 158, 11, 255))

    img.save(out_png)

def generate_persistent_header(out_png: Path):
    """Clean persistent top branding badge that stays throughout the entire video."""
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_pill = ImageFont.truetype(str(FONT_PATH), 22)

    # Top-left EnigmaIQ gold pill
    draw.rounded_rectangle([(65, 75), (235, 120)], radius=22, fill=(245, 158, 11, 255))
    draw.text((85, 83), "ENIGMAIQ", font=font_pill, fill=(2, 9, 20, 255))
    img.save(out_png)

def transcribe_and_make_ass(audio_path: Path, out_ass: Path):
    import whisper
    model = whisper.load_model("base", device="cpu")
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

def main():
    Messenger.info("🚀 Generando Video Piloto: 5 Curiosidades con la Voz Clonada de XpressTV...")
    work_dir = SCRATCH_DIR / VIDEO_META["id"]
    work_dir.mkdir(parents=True, exist_ok=True)
    
    final_dest = DOWNLOADS_DIR / f"{VIDEO_META['id']}.mp4"
    repo_dest = REPO_PRE_DIR / f"{VIDEO_META['id']}.mp4"

    # 1. Narración con Voicebox usando el perfil XpressTV
    vb_client = VoiceboxClient(profile_id=XPRESSTV_PROFILE_ID)
    full_narration = " ".join([s["narration"] for s in SCENES])
    audio_wav = work_dir / "narration_xpresstv.wav"
    
    dur = vb_client.synthesize_full_narration(full_narration, audio_wav)
    Messenger.success(f"🎙️ Audio total con Voz XpressTV: {dur:.2f}s (Regla > 60s cumplida: {dur >= 60.0})")

    # 2. Generar Subtítulos sincronizados
    ass_path = work_dir / f"{VIDEO_META['id']}.ass"
    transcribe_and_make_ass(audio_wav, ass_path)

    # 3. Descarga y normalización de los 12 clips de video correspondientes
    media_hub = MediaHub()
    num_scenes = len(SCENES)
    dur_per_scene = round(dur / num_scenes, 2)
    scene_durations = [dur_per_scene] * num_scenes
    scene_durations[-1] = round(dur - sum(scene_durations[:-1]), 2)

    clips = []
    for idx, sc in enumerate(SCENES):
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

    # 4. Overlays: Intro Card y Persistent Header
    card_png = work_dir / "intro_card.png"
    generate_intro_card(card_png)

    header_png = work_dir / "persistent_header.png"
    generate_persistent_header(header_png)

    # 5. Render Maestro FFmpeg
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
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        str(final_dest)
    ]
    Messenger.info("🎬 Ensamblando master final con FFmpeg...")
    subprocess.run(cmd_master, check=True, cwd=str(BASE_DIR))
    
    sz_mb = final_dest.stat().st_size / (1024 * 1024)
    Messenger.success(f"🎉 MASTER PILOTO CREADO CON ÉXITO: {final_dest.name} ({sz_mb:.1f} MB, {dur:.2f}s)")
    shutil.copy(final_dest, repo_dest)

if __name__ == "__main__":
    main()
