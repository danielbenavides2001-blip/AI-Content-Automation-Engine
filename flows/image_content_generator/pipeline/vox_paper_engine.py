import asyncio
import datetime
import json
import os
import random
import re
import shutil
import subprocess
import sys
import threading
import time
import wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional

import numpy as np
import requests

BASE_DIR = Path(__file__).resolve().parents[3]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

from tools.common.messenger import Messenger
from tools.social_media.facebook import FacebookTool
from tools.video_generation.ai_image_master import AIImageMaster
from tools.video_generation.nasa import NASATool

PIPELINE_DIR = BASE_DIR / "flows" / "image_content_generator" / "pipeline"
CATALOG_FILE = PIPELINE_DIR / "vox_paper_catalog.json"
HISTORY_FILE = BASE_DIR / "flows" / "image_content_generator" / "out_short" / "automated_posts_history.csv"
QUEUE_FILE = BASE_DIR / "flows" / "image_content_generator" / "out_short" / "next_queued_action.json"
REMOTION_DIR = BASE_DIR / "flows" / "image_content_generator" / "remotion"
REPO_PRE_DIR = BASE_DIR / "flows" / "image_content_generator" / "out_short" / "pre_rendered"
REPO_PRE_DIR.mkdir(parents=True, exist_ok=True)
SCRATCH_DIR = BASE_DIR / "scratch" / "vox_v3"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

if os.getenv("GITHUB_ACTIONS") == "true" or os.getenv("CI") == "true":
    OUT_DIR = REPO_PRE_DIR
else:
    OUT_DIR = Path(r"C:\Users\Vanes\Downloads\Videos_VoxPaper_V3")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

VOX_PILLARS = [
    ("INGENIERÍA", "Obras maestras de ingeniería civil, puentes, túneles, presas o maquinaria extrema"),
    ("GEOGRAFÍA", "Fenómenos geográficos reales, ríos ocultos, fronteras raras o geología extrema"),
    ("FÍSICA", "Física cotidiana sorprendente, electricidad, magnetismo, sonido, presión o temperatura"),
    ("TECNOLOGÍA", "Cómo funcionan internamente inventos modernos (fibra óptica, trenes, microchips, GPS)"),
    ("OCÉANOS", "Abismos oceánicos, corrientes marinas, presiones extremas o descubrimientos reales del mar"),
]


def _norm_title(title: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]", "", title.lower())


def load_posted_history() -> tuple[dict[str, int], dict[str, int]]:
    counts: dict[str, int] = {}
    last_idx: dict[str, int] = {}
    if HISTORY_FILE.exists():
        try:
            lines = HISTORY_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()[1:]
            for idx, line in enumerate(lines):
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    norm = _norm_title(parts[2])
                    if norm:
                        counts[norm] = counts.get(norm, 0) + 1
                        last_idx[norm] = idx
        except Exception:
            pass
    return counts, last_idx


def generate_vox_episode(catalog: list) -> Optional[dict]:
    """Generates a 100% original Vox Paper-Collage episode JSON via Gemini."""
    api_keys = [k.strip() for k in (os.getenv("GEMINI_API_KEY", ""), os.getenv("GEMINI_API_KEY_2", "")) if k.strip()]
    if not api_keys:
        return None
    try:
        from google import genai
        from google.genai import types
    except Exception as e:
        Messenger.warning(f"⚠️ google-genai no disponible: {e}")
        return None

    pillar_label, pillar_desc = random.choice(VOX_PILLARS)
    recent_titles = "\n".join(f"- {v['title']}" for v in catalog[-30:])
    ep_id = f"VX_{len(catalog) + 1:02d}_{re.sub(r'[^a-z]', '', pillar_label.lower())[:8]}"

    prompt = f"""Eres el director editorial de un canal viral estilo Vox ("Curiosidades del Mundo" en Reels).
Debes diseñar UN (1) micro-documental visual de **UN SOLO TEMA FASCINANTE** sobre: {pillar_label} ({pillar_desc}).

NO repitas ninguno de estos temas ya creados:
{recent_titles}

REGLAS EDITORIALES ESTRICTAS:
1. Duración total hablada: 75 a 95 palabras en español neutro (ritmo ágil de 26s a 34s).
2. Exactamente 6 beats (escenas) que alternen tipos visuales Vox de esta lista exacta:
   - "paper_highlight": requiere "headline", "highlightPhrase" (2-4 palabras exactas dentro del headline), "kicker"
   - "data_bars": requiere "headline", "chartTitle", "bars": [{{"label":"...","value":123,"unit":"...","highlight":false}}, {{"label":"...","value":999,"unit":"...","highlight":true}}]
   - "big_stat": requiere "headline", "statValue" (ej. "4,000" o "92%"), "statUnit" (ej. "M" o "%"), "statSub", "kicker"
   - "split_process": requiere "headline", "kicker", "steps": [3 pasos cortos de máx 6 palabras cada uno]
   - "media_cutout": requiere "headline", "highlightPhrase", "kicker", "caption"
   - "vox_map": SOLO úsalo si el tema involucra claramente uno de estos países exactos: colombia, ecuador, mexico, usa, brasil, peru, chile, argentina, venezuela ("mapCountry", "mapLabel", "mapCoords", "headline").
3. El beat 1 debe enganchar desde el segundo 00:00 (prohibido saludar o decir "en este video").
4. Cada beat tiene "narration" (12-17 palabras en español) y búsquedas reales de video stock en inglés "q" y "fb" (3-5 palabras concretas).
5. Descripción sin engagement bait (prohibido pedir likes o "comenta").

Responde ÚNICAMENTE con un objeto JSON válido con esta estructura:
{{
  "id": "{ep_id}",
  "pillar": "{pillar_label}",
  "title": "Título viral con 2 emojis",
  "description": "Descripción informativa breve + 4 hashtags",
  "beats": [ ... 6 beats ... ]
}}"""

    for key in api_keys:
        for model_name in ("gemini-2.5-flash", "gemini-2.5-flash-lite"):
            try:
                client = genai.Client(api_key=key)
                resp = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.85, response_mime_type="application/json"),
                )
                data = json.loads(resp.text.strip())
                if isinstance(data, dict) and isinstance(data.get("beats"), list) and len(data["beats"]) >= 5:
                    if not any(_norm_title(data.get("title", "")) == _norm_title(c["title"]) for c in catalog):
                        data["id"] = ep_id
                        return data
            except Exception as e:
                Messenger.warning(f"⚠️ Gemini {model_name} error: {e}")
    return None


def _get_wav_dur(wav_path: Path) -> float:
    with wave.open(str(wav_path), "rb") as wf:
        return wf.getnframes() / float(wf.getframerate())


async def _edge_tts_beat(text: str, mp3_path: Path, voice: str = "es-MX-JorgeNeural", rate: str = "+14%"):
    import edge_tts
    comm = edge_tts.Communicate(text, voice, rate=rate)
    await comm.save(str(mp3_path))


def synthesize_beats_voice(beats: list[dict], work_dir: Path) -> tuple[Path, list[float], float]:
    beat_wavs: list[Path] = []
    beat_durs: list[float] = []

    for i, beat in enumerate(beats):
        raw_mp3 = work_dir / f"beat_{i+1:02d}.mp3"
        clean_wav = work_dir / f"beat_{i+1:02d}.wav"
        asyncio.run(_edge_tts_beat(beat["narration"], raw_mp3))
        subprocess.run([
            "ffmpeg", "-y", "-i", str(raw_mp3),
            "-af", "silenceremove=start_periods=1:start_silence=0.05:start_threshold=-42dB,areverse,silenceremove=start_periods=1:start_silence=0.05:start_threshold=-42dB,areverse,apad=pad_dur=0.14",
            "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(clean_wav),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        beat_wavs.append(clean_wav)
        beat_durs.append(_get_wav_dur(clean_wav))

    concat_txt = work_dir / "voice_concat.txt"
    concat_txt.write_text("\n".join(f"file '{w.resolve().as_posix()}'" for w in beat_wavs) + "\n", encoding="utf-8")
    voice_wav = work_dir / "voice_master.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(voice_wav),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return voice_wav, beat_durs, sum(beat_durs)


def build_vox_soundbed(total_dur: float, beat_durs: list[float], out_wav: Path):
    """Copyright-free editorial documentary rhythm + paper-cut whooshes (48kHz stereo)."""
    sr = 48000
    n = max(1, int(total_dur * sr))
    t = np.arange(n, dtype=np.float32) / sr

    beat_period = 0.500  # 120 BPM crisp editorial groove
    phase_mod = 0.52 + 0.48 * np.exp(-((t % beat_period) * 7.2))
    bed = (
        0.044 * np.sin(2 * np.pi * 65.41 * t)
        + 0.025 * np.sin(2 * np.pi * 130.81 * t + 0.5)
        + 0.014 * np.sin(2 * np.pi * 196.00 * t + 1.0)
    ) * phase_mod

    tick_t = 0.0
    rng = np.random.default_rng(19)
    idx = 0
    while tick_t < total_dur - 0.12:
        i0 = int(tick_t * sr)
        m = min(int(0.035 * sr), n - i0)
        if m > 20:
            lt = np.arange(m, dtype=np.float32) / sr
            freq = 1650.0 if idx % 2 == 0 else 1240.0
            amp = 0.044 if idx % 2 == 0 else 0.022
            bed[i0:i0 + m] += amp * np.exp(-lt * 135.0) * np.sin(2 * np.pi * freq * lt)
        tick_t += beat_period * 0.5
        idx += 1

    # Tactile paper-slap / whoosh at every visual scene change
    cursor = 0.0
    for d in beat_durs[:-1]:
        cursor += d
        d_len = 0.24
        i0 = int((cursor - d_len * 0.5) * sr)
        m = int(d_len * sr)
        if 0 <= i0 and i0 + m < n:
            lt = np.arange(m, dtype=np.float32) / sr
            env = np.sin(np.pi * lt / d_len) ** 2
            noise = rng.normal(0, 1, m).astype(np.float32)
            smooth = np.convolve(noise, np.ones(28, dtype=np.float32) / 28.0, mode="same")
            bed[i0:i0 + m] += smooth * env * 0.12

    fi = min(int(0.18 * sr), n)
    fo = min(int(0.50 * sr), n)
    bed[:fi] *= np.linspace(0.0, 1.0, fi, dtype=np.float32)
    bed[-fo:] *= np.linspace(1.0, 0.0, fo, dtype=np.float32)

    pcm = np.clip(bed * 32767.0, -32767, 32767).astype(np.int16)
    stereo = np.column_stack([pcm, pcm]).ravel()
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(stereo.tobytes())


def extract_whisper_words(audio_wav: Path) -> list[dict]:
    import torch
    import whisper

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("base", device=device)
    res = model.transcribe(str(audio_wav), word_timestamps=True, language="es")

    words: list[dict] = []
    for seg in res.get("segments", []):
        for w in seg.get("words", []):
            txt = w["word"].strip().strip(".,;:!?¿¡").upper()
            if txt:
                words.append({"text": txt, "startSec": round(float(w["start"]), 3), "endSec": round(float(w["end"]), 3)})
    Messenger.info(f"  ⚡ Tiempos Whisper extraídos ({len(words)} palabras)")
    return words


def _download_stream(url: str, dst: Path) -> bool:
    try:
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(dst, "wb") as f:
                for chunk in r.iter_content(chunk_size=131072):
                    if chunk:
                        f.write(chunk)
        return dst.exists() and dst.stat().st_size > 25_000
    except Exception:
        return False


def _claim_id(vid: str, used_ids: set[str], lock: threading.Lock) -> bool:
    with lock:
        if vid in used_ids:
            return False
        used_ids.add(vid)
        return True


def _release_id(vid: str, used_ids: set[str], lock: threading.Lock) -> None:
    with lock:
        used_ids.discard(vid)


def _search_pexels_unused(query: str, used_ids: set[str], out_path: Path, lock: threading.Lock) -> bool:
    pkey = os.getenv("PEXELS_API_KEY", "").strip()
    if not pkey:
        return False
    stop = {"in", "the", "at", "of", "and", "a", "an", "on", "with", "for", "to", "from", "by"}
    words = [w for w in query.lower().split() if w not in stop]
    variants = [query.strip()]
    if len(words) >= 3:
        variants.append(" ".join(words[:3]))
    if len(words) >= 2:
        variants.append(" ".join(words[:2]))

    for qv in dict.fromkeys(variants):
        try:
            r = requests.get("https://api.pexels.com/videos/search", headers={"Authorization": pkey}, params={"query": qv, "per_page": 10}, timeout=12)
            if r.status_code != 200:
                continue
            for v in r.json().get("videos", []):
                vid = f"pexels_{v['id']}"
                if not _claim_id(vid, used_ids, lock):
                    continue
                files = [f for f in v.get("video_files", []) if (f.get("width") or 0) >= 720 or (f.get("height") or 0) >= 720]
                if not files:
                    files = v.get("video_files", [])
                if not files:
                    _release_id(vid, used_ids, lock)
                    continue
                files.sort(key=lambda f: abs(min(f.get("width", 0), f.get("height", 0)) - 960))
                if _download_stream(files[0]["link"], out_path):
                    Messenger.info(f"  📹 Pexels clip único [{vid}] para '{qv}'")
                    return True
                _release_id(vid, used_ids, lock)
        except Exception:
            continue
    return False


def _search_pixabay_unused(query: str, used_ids: set[str], out_path: Path, lock: threading.Lock) -> bool:
    pxkey = os.getenv("PIXABAY_API_KEY", "").strip()
    if not pxkey:
        return False
    words = query.strip().split()
    variants = [query.strip(), " ".join(words[:2])] if len(words) >= 2 else [query.strip()]
    for qv in dict.fromkeys(variants):
        try:
            r = requests.get("https://pixabay.com/api/videos/", params={"key": pxkey, "q": qv, "per_page": 10}, timeout=12)
            if r.status_code != 200:
                continue
            for h in r.json().get("hits", []):
                vid = f"pixabay_{h['id']}"
                if not _claim_id(vid, used_ids, lock):
                    continue
                url = (h.get("videos", {}).get("medium") or h.get("videos", {}).get("large") or {}).get("url")
                if url and _download_stream(url, out_path):
                    Messenger.info(f"  📹 Pixabay clip único [{vid}] para '{qv}'")
                    return True
                _release_id(vid, used_ids, lock)
        except Exception:
            continue
    return False


def _probe_dur(media_path: Path) -> float:
    try:
        out = subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=nk=1:nw=1", str(media_path),
        ], text=True, stderr=subprocess.DEVNULL).strip()
        return float(out)
    except Exception:
        return 0.0


def fetch_vox_scene_asset(
    idx: int, beat: dict, dur: float, work_dir: Path, public_assets_dir: Path,
    rel_prefix: str, used_ids: set[str], lock: threading.Lock, ai_master: AIImageMaster, nasa: NASATool
) -> tuple[str, int]:
    raw_mp4 = work_dir / f"raw_{idx+1:02d}.mp4"
    frames_dir = public_assets_dir / f"s{idx+1:02d}"
    frames_dir.mkdir(parents=True, exist_ok=True)
    q = beat["q"].strip()
    fb = beat.get("fb", q).strip()

    got = False
    if any(k in q.lower() for k in ("space", "planet", "orbit", "nasa", "rocket", "sun", "solar", "galaxy")):
        if nasa.fetch_video(q, raw_mp4):
            got = True
    if not got:
        got = _search_pexels_unused(q, used_ids, raw_mp4, lock) or _search_pixabay_unused(q, used_ids, raw_mp4, lock)
    if not got and fb != q:
        got = _search_pexels_unused(fb, used_ids, raw_mp4, lock) or _search_pixabay_unused(fb, used_ids, raw_mp4, lock)

    if got and raw_mp4.exists() and raw_mp4.stat().st_size > 20_000:
        need_dur = dur + 0.5
        vf = "scale=720:720:force_original_aspect_ratio=increase:flags=lanczos+accurate_rnd,crop=720:720,setsar=1,cas=strength=0.55,eq=contrast=1.08:saturation=1.14,fps=30"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(raw_mp4),
            "-t", f"{need_dur:.3f}", "-vf", vf,
            "-q:v", "4", str(frames_dir / "f_%04d.jpg"),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        n_frames = len(list(frames_dir.glob("f_*.jpg")))
        if n_frames > 0:
            return f"{rel_prefix}/{frames_dir.name}", n_frames

    photo = public_assets_dir / f"photo_{idx+1:02d}.jpg"
    if ai_master.fetch_stock_photo(q, photo) or ai_master.fetch_stock_photo(fb, photo):
        return f"{rel_prefix}/{photo.name}", 0

    fallback_mp4 = work_dir / f"fb_{idx+1:02d}.mp4"
    ai_master.generate_ken_burns_scene(
        f"Editorial documentary photography of {q}, high contrast natural light",
        fallback_mp4, duration=dur + 0.3, motion_style=idx, work_dir=work_dir, query=q, fallback_query=fb
    )
    subprocess.run([
        "ffmpeg", "-y", "-i", str(fallback_mp4),
        "-vf", "scale=720:720:force_original_aspect_ratio=increase:flags=lanczos,crop=720:720,fps=30",
        "-q:v", "4", str(frames_dir / "f_%04d.jpg"),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    n_frames = len(list(frames_dir.glob("f_*.jpg")))
    return f"{rel_prefix}/{frames_dir.name}", n_frames


def produce_vox_video(ep: dict, issue_num: int, force: bool = False) -> Path:
    t0 = time.time()
    out_mp4 = OUT_DIR / f"{ep['id']}.mp4"
    work_dir = SCRATCH_DIR / ep["id"]
    rel_prefix = f"vox_assets/{ep['id']}"
    episode_public_dir = work_dir / "public"
    public_assets_dir = episode_public_dir / "vox_assets" / ep["id"]
    fonts_dst = episode_public_dir / "fonts"

    if force and work_dir.exists():
        shutil.rmtree(work_dir, ignore_errors=True)
    work_dir.mkdir(parents=True, exist_ok=True)
    public_assets_dir.mkdir(parents=True, exist_ok=True)
    fonts_dst.mkdir(parents=True, exist_ok=True)
    font_src = REMOTION_DIR / "public" / "fonts" / "Montserrat-Bold.ttf"
    if font_src.exists():
        shutil.copy2(font_src, fonts_dst / "Montserrat-Bold.ttf")

    Messenger.info(f"\n📰 [VOX ENGINE V3] Produciendo: {ep['id']} — {ep['title']}")

    try:
        # 1. TTS voice per beat + editorial soundbed + Whisper exact word timestamps
        voice_wav, beat_durs, total_dur = synthesize_beats_voice(ep["beats"], work_dir)
        Messenger.success(f"🎙️ Locución lista: {total_dur:.2f}s ({len(ep['beats'])} golpes visuales)")

        bed_wav = work_dir / "vox_soundbed.wav"
        build_vox_soundbed(total_dur, beat_durs, bed_wav)
        words = extract_whisper_words(voice_wav)

        # 2. Fetch unique moving assets in parallel into remotion/public/vox_assets/<id>/
        used_ids: set[str] = set()
        lock = threading.Lock()
        ai_master = AIImageMaster()
        nasa = NASATool()
        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = [
                pool.submit(
                    fetch_vox_scene_asset, i, beat, dur, work_dir,
                    public_assets_dir, rel_prefix, used_ids, lock, ai_master, nasa
                )
                for i, (beat, dur) in enumerate(zip(ep["beats"], beat_durs))
            ]
            media_srcs = [f.result() for f in futures]

        # 3. Build exact frame-aligned VoxBlueprint JSON
        fps = 30
        cursor_frame = 0
        remotion_beats = []
        for i, (beat, dur, (src, n_frames)) in enumerate(zip(ep["beats"], beat_durs, media_srcs)):
            d_frames = max(15, int(round(dur * fps)))
            b_copy = dict(beat)
            b_copy["id"] = f"{ep['id']}_b{i+1}"
            b_copy["startFrame"] = cursor_frame
            b_copy["durationFrames"] = d_frames
            b_copy["mediaSrc"] = src
            b_copy["mediaFrames"] = n_frames
            remotion_beats.append(b_copy)
            cursor_frame += d_frames

        total_frames = max(cursor_frame, int(round(total_dur * fps)))
        blueprint = {
            "episodeId": ep["id"],
            "title": ep["title"],
            "pillarLabel": ep.get("pillar", "CIENCIA"),
            "issueNumber": f"ED. {issue_num:02d}",
            "fps": fps,
            "totalFrames": total_frames,
            "beats": remotion_beats,
            "words": words,
        }

        props_json = work_dir / "vox_props.json"
        props_json.write_text(json.dumps(blueprint, indent=2, ensure_ascii=False), encoding="utf-8")

        # 4. Render with Remotion (isolated --public-dir avoids copying 400MB+ legacy assets)
        silent_mp4 = work_dir / "remotion_visual.mp4"
        npx_bin = "npx.cmd" if os.name == "nt" else "npx"
        workers = str(min(4, max(2, (os.cpu_count() or 2))))
        Messenger.info(f"🎬 Renderizando composición Remotion VoxPaperMaster (concurrency={workers})...")
        subprocess.run([
            npx_bin, "remotion", "render", "src/index.ts", "VoxPaperMaster",
            str(silent_mp4), f"--props={props_json.resolve()}",
            f"--public-dir={episode_public_dir.resolve()}",
            "--codec=h264", "--pixel-format=yuv420p", "--crf=18", f"--concurrency={workers}", "--muted",
        ], check=True, cwd=str(REMOTION_DIR))

        # 5. Master audio mix & loudness calibration
        Messenger.info("🎚️ Mezclando voz + ritmo editorial Vox en AAC 48kHz...")
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(silent_mp4),
            "-i", str(voice_wav),
            "-i", str(bed_wav),
            "-filter_complex", "[1:a]volume=1.65[va];[2:a]volume=0.40[ba];[va][ba]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.92[a_out]",
            "-map", "0:v", "-map", "[a_out]",
            "-t", f"{total_dur:.3f}", "-shortest",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            str(out_mp4),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        sz = out_mp4.stat().st_size / (1024 * 1024)
        Messenger.success(f"🎉 VOX PAPER-COLLAGE LISTO: {out_mp4.name} ({sz:.1f} MB, {total_dur:.2f}s) en {time.time()-t0:.1f}s")
        return out_mp4
    finally:
        # Keep remotion/public clean
        shutil.rmtree(public_assets_dir, ignore_errors=True)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="100% Free Automated Vox Paper-Collage Engine V3 (Remotion)")
    parser.add_argument("--single", action="store_true", help="Generate & optionally upload 1 Vox Reel")
    parser.add_argument("--upload", action="store_true", help="Publish to Facebook Reels")
    parser.add_argument("--episode-id", type=str, default="", help="Force specific episode ID")
    parser.add_argument("--force", action="store_true", help="Force clean scratch rebuild")
    args = parser.parse_args()

    # 1. Respect priority manual/FilmCraft pre-rendered queue if set
    if args.single and not args.episode_id and QUEUE_FILE.exists():
        try:
            q_data = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
            pre_item = q_data.get("pre_rendered_video")
            if isinstance(pre_item, dict) and pre_item.get("file_path"):
                pre_path = BASE_DIR / pre_item["file_path"]
                if pre_path.exists():
                    pre_title = pre_item.get("title", "").strip()
                    pre_desc = pre_item.get("description", "").strip()
                    Messenger.info(f"🎯 [QUEUE PRIORITY] Video pre-renderizado: {pre_path.name}")
                    if args.upload:
                        fb = FacebookTool(page_id=os.getenv("FACEBOOK_PAGE_ID", ""), access_token=os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", ""))
                        res_id = fb.upload_reel(file_path=pre_path, title=pre_title, description=pre_desc)
                        Messenger.success(f"🎉 Video prioritario publicado! Video ID: {res_id}")
                        today = datetime.date.today().isoformat()
                        with open(HISTORY_FILE, "a", encoding="utf-8") as hf:
                            hf.write(f"{today},video,{pre_title.replace(',', ' - ')}\n")
                        q_data["pre_rendered_video"] = None
                        q_data["last_executed"] = pre_title
                        q_data["executed_at"] = datetime.datetime.now().isoformat()
                        QUEUE_FILE.write_text(json.dumps(q_data, indent=2, ensure_ascii=False), encoding="utf-8")
                    return
        except Exception as e:
            Messenger.error(f"Error procesando cola prioritaria: {e}")
            sys.exit(1)

    catalog = json.loads(CATALOG_FILE.read_text(encoding="utf-8")) if CATALOG_FILE.exists() else []
    counts, last_idx = load_posted_history()

    target_ep = None
    if args.episode_id:
        target_ep = next((e for e in catalog if e["id"] == args.episode_id), None)

    if not target_ep:
        for ep in catalog:
            if counts.get(_norm_title(ep["title"]), 0) == 0:
                target_ep = ep
                break

    if not target_ep:
        Messenger.info("✨ Catálogo Vox cubierto. Generando nuevo guión Vox con Gemini...")
        fresh = generate_vox_episode(catalog)
        if fresh:
            catalog.append(fresh)
            CATALOG_FILE.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")
            target_ep = fresh
            Messenger.success(f"🆕 Nuevo guión Vox creado: {fresh['id']} — {fresh['title']}")

    if not target_ep and catalog:
        target_ep = min(
            enumerate(catalog),
            key=lambda pair: (counts.get(_norm_title(pair[1]["title"]), 0), last_idx.get(_norm_title(pair[1]["title"]), -1), pair[0]),
        )[1]

    if not target_ep:
        Messenger.error("❌ No se pudo seleccionar ni generar episodio Vox.")
        sys.exit(1)

    issue_num = sum(counts.values()) + 1
    master_mp4 = produce_vox_video(target_ep, issue_num=issue_num, force=args.force)

    if args.upload and master_mp4.exists():
        fb = FacebookTool(page_id=os.getenv("FACEBOOK_PAGE_ID", ""), access_token=os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", ""))
        res_id = fb.upload_reel(file_path=master_mp4, title=target_ep["title"], description=target_ep.get("description", ""))
        Messenger.success(f"🎉 Reel Vox V3 publicado! Video ID: {res_id}")
        today = datetime.date.today().isoformat()
        with open(HISTORY_FILE, "a", encoding="utf-8") as hf:
            hf.write(f"{today},video,{target_ep['title'].replace(',', ' - ')}\n")


if __name__ == "__main__":
    main()
