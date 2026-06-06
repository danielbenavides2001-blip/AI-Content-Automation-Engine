"""
Repair script for idea_000002:
- Regenerate scene 1 TTS with fixed narration
- Remix audio (SFX + concat)
- Re-render Remotion subtitles (word-by-word)
- Compose with raw video
- Add background music
- Upload to Facebook
"""
import sys, json, subprocess, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))

IDEA_ID = 2
BASE = ROOT / "flows/image_content_generator/out_short/ideas" / f"idea_{IDEA_ID:06d}"
AUDIOS = BASE / "audios"
EDITIONS = BASE / "editions"
REMOTION_DIR = ROOT / "flows/image_content_generator/remotion"
REMOTION_FRAMES = EDITIONS / "remotion_frames"

# --- 1. Generate new TTS for scene 1 ---
print("=== Step 1: Generating TTS for scene 1 ===")
script_path = BASE / "script.json"
script = json.loads(script_path.read_text(encoding="utf-8"))
scene1 = script["scenes"][0]
print(f"  Narration: {scene1['narration']}")

from tools.audio_generation.gemini import GeminiAudioGenerator
tts = GeminiAudioGenerator()
chunk_audio = AUDIOS / "chunk_fixed.wav"
tts.text_to_speech(scene1["narration"], chunk_audio)

# --- 2. Get duration and split to scene_1.wav ---
print("=== Step 2: Aligning scene 1 audio ===")
from tools.video_editing.ffmpeg import FFmpegTool
from tools.video_editing.whisper import WhisperTool
ffmpeg = FFmpegTool()
whisper = WhisperTool()

total_dur = ffmpeg.get_audio_duration(chunk_audio)
print(f"  Total duration: {total_dur:.2f}s")

scene1_audio = AUDIOS / "scene_1.wav"
ffmpeg.split_audio(chunk_audio, scene1_audio, 0, total_dur)

# --- 3. Add SFX to scene 1 ---
print("=== Step 3: Adding SFX to scene 1 ===")
scene1_sfx = AUDIOS / "scene_01_sfx.wav"
# Get the original non-fixed TTS duration to match SFX timing if possible
# Use wind desert SFX per script
sfx_path = ROOT / "flows/image_content_generator/resource/sfx/wind_desert.mp3"
if not sfx_path.exists():
    # Try to find any wind SFX
    sfx_candidates = list(ROOT.glob("flows/image_content_generator/resource/sfx/wind*"))
    sfx_path = sfx_candidates[0] if sfx_candidates else None

if sfx_path and sfx_path.exists():
    # Mix SFX at low volume underneath narration
    scene_dur = ffmpeg.get_audio_duration(scene1_audio)
    cmd = [
        "ffmpeg", "-y",
        "-i", str(scene1_audio),
        "-i", str(sfx_path),
        "-filter_complex",
        f"[1:a]atrim=0:{scene_dur},volume=0.12[sfx];[0:a][sfx]amix=inputs=2:duration=first[out]",
        "-map", "[out]",
        str(scene1_sfx)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"  SFX mixed: {scene1_sfx}")
else:
    shutil.copy(scene1_audio, scene1_sfx)
    print(f"  No SFX found, copied dry audio: {scene1_sfx}")

# --- 4. Concatenate all scene SFX into final_audio.wav ---
print("=== Step 4: Concatenating final audio ===")
sfx_files = sorted(AUDIOS.glob("scene_*_sfx.wav"))
if not sfx_files:
    print("  ERROR: No SFX files found!")
    sys.exit(1)

final_audio = EDITIONS / "final_audio.wav"
cmd = ["ffmpeg", "-y"]
for s in sfx_files:
    cmd.extend(["-i", str(s)])
if len(sfx_files) > 1:
    fc = "".join([f"[{i}:a]" for i in range(len(sfx_files))]) + f"concat=n={len(sfx_files)}:v=0:a=1[a]"
    cmd.extend(["-filter_complex", fc, "-map", "[a]"])
else:
    cmd.extend(["-c:a", "copy"])
cmd.append(str(final_audio))
subprocess.run(cmd, check=True, capture_output=True)
print(f"  Final audio: {final_audio} ({ffmpeg.get_audio_duration(final_audio):.2f}s)")

# --- 5. Transcribe final audio with Whisper ---
print("=== Step 5: Transcribing with Whisper ===")
full_narration = " ".join([s["narration"] for s in script["scenes"]])
words_raw = whisper.get_word_tokens(final_audio, prompt=full_narration)
word_data = [{"text": w.text, "start": w.start, "end": w.end} for w in words_raw]
print(f"  Words detected: {len(word_data)}")

# --- 6. Build level markers from audio durations ---
print("=== Step 6: Building level markers ===")
level_markers = []
current_time = 0.0
for scene in script["scenes"]:
    scene_num = scene.get("nivel", scene["scene_number"])
    sfx_file = AUDIOS / f"scene_{scene_num:02d}_sfx.wav"
    if not sfx_file.exists():
        sfx_file = AUDIOS / f"scene_{scene_num}.wav"
    duration = ffmpeg.get_audio_duration(sfx_file) if sfx_file.exists() else 5.0

    level_markers.append({
        "nivel": scene_num,
        "titulo": scene.get("titulo_nivel", ""),
        "impacto": scene.get("impacto", "Medio"),
        "startTime": current_time * 1000,
        "endTime": (current_time + duration) * 1000,
    })
    current_time += duration

intrigue_text = script.get("intrigue_header", None)

# --- 7. Render Remotion subtitle overlay ---
print("=== Step 7: Rendering Remotion subtitles ===")
if REMOTION_FRAMES.exists():
    shutil.rmtree(REMOTION_FRAMES)
REMOTION_FRAMES.mkdir(parents=True, exist_ok=True)

from tools.video_editing.remotion import RemotionTool
remotion = RemotionTool()
remotion.render_subtitles(
    remotion_path=REMOTION_DIR,
    output_path=REMOTION_FRAMES,
    words=word_data,
    intrigue_header=intrigue_text,
    composition_id="Subtitles",
    level_markers=level_markers,
)

# --- 8. Compose Remotion overlay on raw video ---
print("=== Step 8: Composing subtitles on video ===")
raw_video = EDITIONS / "raw_video.mp4"
pro_video = EDITIONS / "pro_subtitled_video.mp4"

frame_files = sorted(REMOTION_FRAMES.glob("*.png"))
if frame_files:
    first_name = frame_files[0].stem
    padding = len(first_name)
    remotion_pattern = REMOTION_FRAMES / f"%0{padding}d.png"
else:
    remotion_pattern = REMOTION_FRAMES / "%04d.png"

cmd = [
    "ffmpeg", "-y",
    "-i", str(raw_video),
    "-framerate", "30",
    "-i", str(remotion_pattern),
    "-filter_complex", "[0:v][1:v]overlay=shortest=1[out]",
    "-map", "[out]", "-map", "0:a",
    "-c:v", "libx264", "-c:a", "copy", "-pix_fmt", "yuv420p",
    str(pro_video)
]
subprocess.run(cmd, check=True)
pro_size = pro_video.stat().st_size
print(f"  PRO video: {pro_video} ({pro_size / 1024 / 1024:.2f} MB)")

# --- 9. Add background music with ducking ---
print("=== Step 9: Adding background music ===")
# Use the background music function from pipeline
bg_musics = list((ROOT / "flows/image_content_generator/resource/bg-music/siete_niveles").glob("*.mp3"))
if bg_musics:
    import random
    bg_music = random.choice(bg_musics)
    print(f"  Selected: {bg_music.name}")

    final_video = EDITIONS / "final_video.mp4"
    bg_volume = 0.15

    filter_complex = (
        f"[0:a]asplit[voice][voice_side];"
        f"[1:a]volume={bg_volume}[bg_a];"
        f"[bg_a][voice_side]sidechaincompress=threshold=0.06:ratio=10:attack=0.5:release=100[bg_compressed];"
        f"[voice][bg_compressed]amix=inputs=2:duration=first:weights=1 0.4[fixed_a]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(pro_video),
        "-stream_loop", "-1",
        "-i", str(bg_music),
        "-filter_complex", filter_complex,
        "-map", "0:v", "-map", "[fixed_a]",
        "-c:v", "copy", "-c:a", "aac",
        str(final_video)
    ]
    subprocess.run(cmd, check=True)
    print(f"  Final video: {final_video}")
else:
    final_video = pro_video
    print("  No background music found, using PRO video as final")

# --- 10. Rename and thumbnail ---
print("=== Step 10: Renaming and thumbnail ===")
from tools.text_generation.gemini import GeminiTool
from flows.image_content_generator.pipeline.pipeline import ContentPipeline

# Generate thumbnail description
thumbnail_desc_prompt = f"Generate a short thumbnail title (max 40 chars) in Spanish for this video. Just the text, no quotes: {script['scenes'][0]['titulo_nivel']}"
gemini = GeminiTool()
thumbnail_title = gemini.generate_text(thumbnail_desc_prompt, str).strip().strip('"').strip("'")
print(f"  Thumbnail: {thumbnail_title}")

# Get Facebook uploader
import importlib
facebook_module = importlib.import_module("tools.social_media.facebook")
FacebookTool = facebook_module.FacebookTool
fb = FacebookTool()

# Idea data
idea_data_path = BASE / "idea.json"
idea_data = json.loads(idea_data_path.read_text(encoding="utf-8"))

# --- 11. Upload to Facebook ---
print("=== Step 11: Uploading to Facebook ===")
# Generate AI description
desc_prompt = f"""Escribe una descripción atractiva en ESPAÑOL para este video de YouTube Shorts/Reels/TikTok. MÁXIMO 40 palabras. Usa emojis. Termina con 3 hashtags relevantes.

Título: {idea_data['title']}
Hook: {idea_data['hook']}
Categoría: {idea_data['category']}"""

description = gemini.generate_text(desc_prompt, str)
print(f"  Description: {description}")

# Upload
output_name = f"scene_1_{scene1['titulo_nivel'].lower().replace(' ', '_')}.mp4"
video_path = final_video

video_id = fb.upload_video(
    video_path=str(video_path),
    title=idea_data["title"],
    description=description,
    published=True,
)
print(f"  Uploaded! Video ID: {video_id}")

# Set thumbnail
if thumbnail_title:
    fb.set_video_thumbnail(video_id, thumbnail_title)

# Generate auto-comment
comment_prompt = f"""Escribe 1 comentario atractivo en ESPAÑOL para este video. Máximo 15 palabras. Que invite a la audiencia a participar:

Título: {idea_data['title']}
Hook: {idea_data['hook']}"""

auto_comment = gemini.generate_text(comment_prompt, str)
if auto_comment:
    post_id = fb.get_post_id_from_video(video_id)
    if post_id:
        fb.add_comment(post_id, auto_comment)
        print(f"  Auto-comment: {auto_comment}")

print("\n=== REPAIR COMPLETE ===")
print(f"Video published: {video_id}")
