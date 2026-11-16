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
from tools.text_generation.gemini import GeminiTextGenerator
from tools.video_generation.pexels import PexelsTool
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
SCRATCH_DIR = BASE_DIR / "scratch" / "precision_batch"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
QUEUE_FILE = BASE_DIR / "flows" / "image_content_generator" / "out_short" / "next_queued_action.json"

BATCH_TOPICS = [
    {
        "num": "16",
        "id": "16_EnigmaIQ_Ventanas_Aviones",
        "title": "¿Por qué las ventanas de los aviones son redondas y nunca cuadradas? ✈️🪟",
        "headline_top": "¿POR QUÉ LAS VENTANAS DE AVIONES",
        "headline_bottom": "SON REDONDAS Y NO CUADRADAS?",
        "category": "INGENIERÍA & MISTERIOS",
        "core_premise": "En 1954, los primeros aviones comerciales a reacción (de Havilland Comet) se desintegraban en pleno vuelo. La causa no fue el motor: eran las ventanas cuadradas que acumulaban presión mortal en las esquinas.",
        "description": "Las ventanas de los aviones son redondas… y no por diseño estético. La aviación lo aprendió de la peor manera en 1954 con el desastre del Comet. La física de la concentración de tensión explicada paso a paso.\n\n#EnigmaIQ #ElPorquéDeTodo #Aviones #Ciencia #Ingenieria #Curiosidades #Aeronautica",
        "target_queries": [
            "airplane window exterior clouds",
            "commercial jet flying sky",
            "airplane cockpit dials pilot",
            "metal fracture test laboratory",
            "cracked glass corner pressure",
            "round airplane window passenger",
            "modern aircraft wing clouds",
            "airplane cabin passenger flight"
        ]
    },
    {
        "num": "17",
        "id": "17_EnigmaIQ_Cafe_Cerebro",
        "title": "El café no te da energía: ¿Cómo engaña a tu cerebro? ☕🧠",
        "headline_top": "EL CAFÉ NO TE DA ENERGÍA:",
        "headline_bottom": "¿CÓMO ENGAÑA A TU CEREBRO?",
        "category": "NEUROCIENCIA & CUERPO",
        "core_premise": "La cafeína no produce energía celular nueva. Tiene una estructura casi idéntica a la adenosina (la molécula del cansancio) y se acopla a sus receptores, bloqueando la señal de fatiga hasta que se desgasta.",
        "description": "El café no produce energía en tu cuerpo… solo sabotea temporalmente el freno de mano de tu cerebro ☕ Y cuando la cafeína desaparece, la fatiga acumulada te golpea de golpe. La neuroquímica de tu taza matutina.\n\n#EnigmaIQ #ElPorquéDeTodo #Cafe #Cerebro #Neurociencia #Curiosidades #Salud #Ciencia",
        "target_queries": [
            "espresso pouring hot coffee cup",
            "steam rising black coffee morning",
            "tired person yawning desk laptop",
            "brain neural synapse electricity glow",
            "coffee beans roasting steam macro",
            "person drinking coffee energy focus",
            "cellular molecular structure 3d animation",
            "happy productive person morning sun"
        ]
    },
    {
        "num": "18",
        "id": "18_EnigmaIQ_Relampago_Trueno",
        "title": "El relámpago y el trueno pasan al mismo tiempo: ¿Por qué primero ves la luz? ⚡👂",
        "headline_top": "RELÁMPAGO Y TRUENO OCURREN JUNTOS:",
        "headline_bottom": "¿POR QUÉ PRIMERO VES LA LUZ?",
        "category": "FÍSICA DE LA NATURALEZA",
        "core_premise": "La luz viaja a 300.000 kilómetros por segundo, mientras que el sonido viaja a solo 343 metros por segundo. Por eso ves el destello al instante y el trueno llega segundos después, revelando la distancia de la tormenta.",
        "description": "Ambos nacen exactamente en la misma milésima de segundo, pero la luz viaja casi un millón de veces más rápido que las ondas sonoras en el aire ⚡ Te explicamos cómo calcular a qué distancia caerá el siguiente rayo.\n\n#EnigmaIQ #ElPorquéDeTodo #Tormenta #Rayo #Trueno #Fisica #Naturaleza #Curiosidades",
        "target_queries": [
            "lightning bolt storm night clouds",
            "dark thunderstorm rain wind sky",
            "close up lightning strike ground",
            "sound wave ripple vibration water",
            "man looking at stormy sky thunder",
            "stopwatch countdown seconds ticking",
            "heavy rain storm city street night",
            "dramatic lightning flash skyline night"
        ]
    },
    {
        "num": "19",
        "id": "19_EnigmaIQ_Gatos_Caida",
        "title": "¿Por qué los gatos siempre caen de pie? El truco físico de 1894 🐈🐾",
        "headline_top": "¿POR QUÉ LOS GATOS SIEMPRE",
        "headline_bottom": "CAEN DE PIE? EL TRUCO FÍSICO",
        "category": "BIOLOGÍA & FÍSICA FELINA",
        "core_premise": "El reflejo de enderezamiento felino desafió la ley de conservación del momento angular. Los gatos doblan su columna vertebral por la mitad y giran el tren delantero y trasero en direcciones opuestas en menos de medio segundo.",
        "description": "Durante siglos la ciencia creyó que los gatos violaban las leyes de la física al girar en el aire sin nada sobre lo que apoyarse 🐈 En 1894 la cronofotografía reveló su asombrosa mecánica biomecánica.\n\n#EnigmaIQ #ElPorquéDeTodo #Gatos #Fisica #Animales #Mascotas #Biomecanica #Curiosidades",
        "target_queries": [
            "cat jumping slow motion landing",
            "cat eyes close up staring alert",
            "flexible cat stretching spine paws",
            "cat twisting body falling slow motion",
            "cat paws landing soft grass ground",
            "cat spine anatomy agility balance",
            "graceful domestic cat walking fence",
            "cute cat looking camera purring"
        ]
    },
    {
        "num": "20",
        "id": "20_EnigmaIQ_Bolsillo_Jeans",
        "title": "¿Para qué sirve realmente el bolsillo pequeño de tus jeans? 👖⏳",
        "headline_top": "¿PARA QUÉ SIRVE EL BOLSILLO",
        "headline_bottom": "PEQUEÑO DE TUS JEANS?",
        "category": "HISTORIA & DISEÑO OCULTO",
        "core_premise": "En 1873, Levi Strauss diseñó el diminuto bolsillo interior para que los mineros y vaqueros guardaran sus relojes de bolsillo sin rayarlos ni romperlos. Aunque hoy usamos móviles, el diseño original se mantiene intacto.",
        "description": "Ese pequeño bolsillo en el que apenas cabe un dedo no fue creado para monedas ni para encendedores 👖 Nació en la fiebre del oro de 1873 para proteger los objetos más valiosos de los vaqueros: sus relojes de cadena.\n\n#EnigmaIQ #ElPorquéDeTodo #Jeans #Moda #Historia #Inventos #Curiosidades #Diseno",
        "target_queries": [
            "blue jeans denim pocket close up",
            "vintage pocket watch golden chain ticking",
            "cowboy walking desert gold rush 1800s",
            "miner digging gold rocks historical",
            "artisan tailor sewing denim trousers",
            "person putting fingers tiny jeans pocket",
            "modern person wearing stylish denim jeans",
            "old mechanical pocket watch opening gears"
        ]
    }
]

def format_ass_time(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int((sec - int(sec)) * 100)
    return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"

def generate_script_blueprint(topic: dict, text_gen: GeminiTextGenerator) -> dict:
    prompt = f"""
Eres el Guionista y Director de 'EnigmaIQ' (estilo 'El porqué de todo' en Facebook Reels).
Crea un guion audiovisual fascinante, científico y de intriga viral sobre este tema:

TÍTULO: {topic['title']}
PREMISA CIENTÍFICA: {topic['core_premise']}
LÍNEA SUPERIOR: {topic['headline_top']}
LÍNEA INFERIOR: {topic['headline_bottom']}

REGLAS CRÍTICAS DE DURACIÓN (> 60 SEGUNDOS OBLIGATORIO):
1. Debes generar exactamente 8 escenas consecutivas.
2. Cada escena DEBE tener una narración de entre 18 y 22 palabras concisas, rítmicas y con intriga.
3. El total acumulado de las 8 escenas debe estar entre 148 y 165 palabras. Esto garantiza que el audio dure exactamente entre 68 y 76 segundos (> 60s obligatorio para monetización en Meta Reels).
4. La Escena 8 debe cerrar con el llamado a la acción: "Esto es EnigmaIQ. ¿Conocías este secreto? Cuéntanos en los comentarios."

REGLA DE CONGRUENCIA VISUAL ABSOLUTA:
5. CADA ESCENA DEBE MOSTRAR EXACTAMENTE LO QUE SE NARRA EN ESE INSTANTE:
   - Proporciona en 'stock_query' de 2 a 3 palabras clave en INGLÉS directas y comerciales.

Responde ÚNICAMENTE en JSON con la estructura:
{{
  "title": "{topic['title']}",
  "headline_top": "{topic['headline_top']}",
  "headline_bottom": "{topic['headline_bottom']}",
  "scenes": [
    {{"scene_number": 1, "narration": "...", "stock_query": "..."}},
    ... (hasta escena 8)
  ]
}}
"""
    for model_name in ["gemini-2.5-flash", "gemini-3-flash-preview", "gemini-3.1-flash-lite"]:
        try:
            resp = text_gen._execute_with_retry(
                "models.generate_content",
                model=model_name,
                contents=[prompt],
                config={"response_mime_type": "application/json"}
            )
            data = json.loads(resp.text)
            if len(data.get("scenes", [])) == 8:
                return data
        except Exception as e:
            Messenger.warning(f"Model {model_name} failed: {e}")
            continue

    # Fallback to local template if Gemini is unavailable
    Messenger.warning(f"Using fallback structured blueprint for {topic['id']}")
    words = topic['core_premise'].split()
    scenes = []
    chunk_sz = max(18, len(words) // 7)
    for i in range(7):
        sub_words = words[i*chunk_sz:(i+1)*chunk_sz]
        if not sub_words:
            sub_words = words[:18]
        scenes.append({
            "scene_number": i + 1,
            "narration": " ".join(sub_words),
            "stock_query": topic["target_queries"][i]
        })
    scenes.append({
        "scene_number": 8,
        "narration": "Esto es EnigmaIQ. La ciencia detrás de lo cotidiano. ¿Conocías este secreto? Cuéntanos en los comentarios.",
        "stock_query": topic["target_queries"][7]
    })
    return {
        "title": topic["title"],
        "headline_top": topic["headline_top"],
        "headline_bottom": topic["headline_bottom"],
        "scenes": scenes
    }

def generate_question_card(topic: dict, out_png: Path):
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font_pill = ImageFont.truetype(str(FONT_PATH), 22)
    font_category = ImageFont.truetype(str(FONT_PATH), 20)
    font_top = ImageFont.truetype(str(FONT_PATH), 42)
    font_bottom = ImageFont.truetype(str(FONT_PATH), 50)

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
    cat_text = topic["category"].upper()
    cat_b = draw.textbbox((0, 0), cat_text, font=font_category)
    cat_w = cat_b[2] - cat_b[0]
    cat_x0 = (1080 - cat_w - 36) // 2
    draw.rounded_rectangle([(cat_x0, box_y0 - 18), (cat_x0 + cat_w + 36, box_y0 + 18)], radius=18, fill=(245, 158, 11, 255))
    draw.text((cat_x0 + 18, box_y0 - 11), cat_text, font=font_category, fill=(2, 9, 20, 255))

    # Top & bottom lines
    t_top = topic["headline_top"]
    b_top = draw.textbbox((0, 0), t_top, font=font_top)
    draw.text(((1080 - (b_top[2] - b_top[0])) // 2, box_y0 + 55), t_top, font=font_top, fill=(255, 255, 255, 255))

    t_bot = topic["headline_bottom"]
    b_bot = draw.textbbox((0, 0), t_bot, font=font_bottom)
    draw.text(((1080 - (b_bot[2] - b_bot[0])) // 2, box_y0 + 120), t_bot, font=font_bottom, fill=(245, 158, 11, 255))

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

def produce_topic_video(topic: dict, text_gen: GeminiTextGenerator, media_hub: MediaHub, vb_client: VoiceboxClient) -> Path:
    final_dest = DOWNLOADS_DIR / f"{topic['id']}.mp4"
    repo_dest = REPO_PRE_DIR / f"{topic['id']}.mp4"

    if final_dest.exists() and final_dest.stat().st_size > 15 * 1024 * 1024:
        Messenger.success(f"Video already fully rendered: {final_dest.name}")
        if not repo_dest.exists() or repo_dest.stat().st_size != final_dest.stat().st_size:
            shutil.copy(final_dest, repo_dest)
        return final_dest

    work_dir = SCRATCH_DIR / topic["id"]
    work_dir.mkdir(parents=True, exist_ok=True)
    Messenger.info(f"\n==========================================")
    Messenger.info(f"Producing Master: {topic['id']}")
    Messenger.info(f"Topic: {topic['title']}")
    Messenger.info(f"==========================================")

    # 1. Blueprint Script
    blueprint = generate_script_blueprint(topic, text_gen)
    scenes = blueprint["scenes"]

    # 2. Master Narration Synthesis with Voicebox
    full_narration = " ".join([s["narration"].strip() for s in scenes])
    audio_wav = work_dir / "narration.wav"
    dur = vb_client.synthesize_full_narration(full_narration, audio_wav)
    Messenger.info(f"Narration duration: {dur:.2f}s (Rule > 60s verified: {dur >= 60.0})")

    # 3. Subtitles ASS
    ass_path = work_dir / f"{topic['id']}.ass"
    transcribe_and_make_ass(audio_wav, ass_path)

    # 4. Download 8 Visual Stock Clips matching Narration Sentence-by-Sentence
    num_scenes = len(scenes)
    dur_per_scene = round(dur / num_scenes, 2)
    scene_durations = [dur_per_scene] * num_scenes
    scene_durations[-1] = round(dur - sum(scene_durations[:-1]), 2)

    clips = []
    for idx, sc in enumerate(scenes):
        raw_clip = work_dir / f"raw_scene_{idx+1}.mp4"
        norm_clip = work_dir / f"norm_scene_{idx+1}.mp4"
        t_dur = scene_durations[idx]
        
        q = sc.get("stock_query") or topic["target_queries"][idx]
        if not raw_clip.exists() or raw_clip.stat().st_size < 10000:
            ok = media_hub.fetch_best_clip(query=q, out_path=raw_clip, scene_topic=topic["title"], duration=t_dur)
            if not ok or not raw_clip.exists() or raw_clip.stat().st_size < 10000:
                fallback_q = topic["target_queries"][idx]
                media_hub.fetch_best_clip(query=fallback_q, out_path=raw_clip, scene_topic=topic["title"], duration=t_dur)

        # Normalize clip to 1080x1920 30fps
        cmd_norm = [
            "ffmpeg", "-y", "-stream_loop", "3", "-i", str(raw_clip),
            "-t", str(t_dur),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30",
            "-an", "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
            str(norm_clip)
        ]
        subprocess.run(cmd_norm, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=str(BASE_DIR))
        clips.append(norm_clip)

    # Concat list
    concat_txt = work_dir / "concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in clips:
            f.write(f"file '{c.resolve().as_posix()}'\n")

    # Question Card PNG
    card_png = work_dir / "card.png"
    generate_question_card(topic, card_png)

    # 5. Master Render with Subtitles, Card, and Ambient Bed
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

    cmd_master = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-i", str(card_png),
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
    subprocess.run(cmd_master, check=True, cwd=str(BASE_DIR))
    Messenger.success(f"🎉 MASTER EXPORT COMPLETE: {final_dest.name} ({final_dest.stat().st_size / (1024*1024):.1f} MB, {dur:.2f}s)")

    # Copy to repo pre-rendered queue
    shutil.copy(final_dest, repo_dest)
    return final_dest

def main():
    Messenger.info("🚀 Starting Production Batch (Videos 16 to 20) with Precision Congruence & Cloned Voice...")
    text_gen = GeminiTextGenerator()
    media_hub = MediaHub()
    vb_client = VoiceboxClient()

    rendered_files = []
    for topic in BATCH_TOPICS:
        try:
            m_path = produce_topic_video(topic, text_gen, media_hub, vb_client)
            rendered_files.append((topic, m_path))
        except Exception as e:
            Messenger.error(f"Failed producing {topic['id']}: {e}")
            import traceback
            traceback.print_exc()

    # Update next_queued_action.json
    Messenger.info("📝 Updating next_queued_action.json with the new videos...")
    queue_data = {"pre_rendered_queue": []}
    if QUEUE_FILE.exists():
        try:
            with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                queue_data = json.load(f)
        except Exception:
            pass

    existing_paths = {item.get("file_path") for item in queue_data.get("pre_rendered_queue", [])}
    for topic, m_path in rendered_files:
        rel_path = f"flows/image_content_generator/out_short/pre_rendered/{topic['id']}.mp4"
        if rel_path not in existing_paths:
            queue_data["pre_rendered_queue"].append({
                "file_path": rel_path,
                "title": topic["title"],
                "description": topic["description"]
            })
            existing_paths.add(rel_path)

    queue_data["note"] = "Cola secuencial de videos editados originales con máxima congruencia visual, voz cinematográfica 'El Porqué de Todo' y branding EnigmaIQ."
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue_data, f, indent=2, ensure_ascii=False)

    Messenger.success(f"✅ next_queued_action.json updated! Total videos in queue: {len(queue_data['pre_rendered_queue'])}")

if __name__ == "__main__":
    main()
