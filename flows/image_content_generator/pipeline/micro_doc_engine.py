import asyncio
import datetime
import hashlib
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
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parents[3]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

from tools.common.messenger import Messenger
from tools.social_media.facebook import FacebookTool
from tools.video_generation.ai_image_master import AIImageMaster
from tools.video_generation.nasa import NASATool

FONTS_DIR = BASE_DIR / "flows" / "curiosity_image_generator" / "resources" / "fonts"
FONT_PATH = FONTS_DIR / "Montserrat-Bold.ttf"
CATALOG_FILE = BASE_DIR / "flows" / "image_content_generator" / "pipeline" / "micro_doc_catalog.json"
HISTORY_FILE = BASE_DIR / "flows" / "image_content_generator" / "out_short" / "automated_posts_history.csv"
QUEUE_FILE = BASE_DIR / "flows" / "image_content_generator" / "out_short" / "next_queued_action.json"
REPO_PRE_DIR = BASE_DIR / "flows" / "image_content_generator" / "out_short" / "pre_rendered"
REPO_PRE_DIR.mkdir(parents=True, exist_ok=True)
SCRATCH_DIR = BASE_DIR / "scratch" / "micro_doc_v2"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

if os.getenv("GITHUB_ACTIONS") == "true" or os.getenv("CI") == "true":
    OUT_DIR = REPO_PRE_DIR
else:
    OUT_DIR = Path(r"C:\Users\Vanes\Downloads\Videos_MicroDoc_V2")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

PILLARS = [
    ("ingenieria_extrema", "Ingeniería extrema, tuneladoras, puentes lanzadores, megaestructuras, presas, cables submarinos o trenes"),
    ("fisica_oculta", "Física sorprendente en objetos cotidianos o fenómenos extremos (electroquímica, cavitación, acústica, aeronáutica, rayos)"),
    ("biologia_insolita", "Biología animal asombrosa o camuflaje extremo, defensa química, récords de velocidad o adaptaciones raras"),
    ("tecnologia_mecanica", "Tecnología industrial fascinante (fibra óptica, ósmosis inversa, turbinas, manufactura de precisión, satélites)"),
    ("oceanos_cosmos", "Fenómenos reales del océano profundo, geología extrema o astronomía espacial verificable"),
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


def generate_micro_doc_episode(catalog: list, posted_norm_titles: set[str], pillar_hint: str = "") -> Optional[dict]:
    """Generates a single-topic 26-36s viral science micro-documentary via Gemini."""
    api_keys = [k.strip() for k in (os.getenv("GEMINI_API_KEY", ""), os.getenv("GEMINI_API_KEY_2", "")) if k.strip()]
    if not api_keys:
        return None
    try:
        from google import genai
        from google.genai import types
    except Exception as e:
        Messenger.warning(f"⚠️ google-genai no disponible: {e}")
        return None

    pillar_code, pillar_desc = random.choice(PILLARS)
    if pillar_hint:
        pillar_desc = pillar_hint

    recent_titles = "\n".join(f"- {v['title']}" for v in catalog[-30:])
    next_idx = len(catalog) + 1
    ep_id = f"MD_{next_idx:02d}_{pillar_code}"

    prompt = f"""Eres el guionista principal de una página viral de ciencia, ingeniería y curiosidades estilo "Enséñame de Ciencia" (7.5M seguidores).
Debes crear UN (1) micro-documental de **UN SOLO TEMA FASCINANTE** (NO listas de 5 cosas, NO saludos, NO "en este video").

Pilar asignado hoy: {pillar_desc}
NO repitas ninguno de estos temas ya usados:
{recent_titles}

Devuelve ÚNICAMENTE un JSON válido (sin markdown ni texto extra) con esta estructura exacta:
{{
  "id": "{ep_id}",
  "pillar": "{pillar_code}",
  "title": "Titular atrapante y directo al grano (máximo 72 caracteres, 2 emojis al final)",
  "description": "Explicación fascinante de 2 líneas + pregunta orgánica abierta (SIN pedir likes/comenta/comparte) + 5 hashtags relevantes",
  "beats": [
    {{
      "narration": "Frase directa al grano (10-14 palabras)...",
      "q": "concrete visual English query for real stock video (4-6 words)",
      "fb": "broader fallback English stock video query (3-5 words)"
    }}
  ]
}}

REGLAS ESTRICTAS DE RETENCIÓN VIRAL Y MONETIZACIÓN:
1. Exactamente **8 o 9 beats cortos** (total **80 a 102 palabras**, duración resultante **27 a 35 segundos**, ~2.8-3.8s por plano).
2. Regla de oro **"lo que se narra se muestra"**: cada beat DEBE describir UN solo objeto o acción visual concreta (8-12 palabras), y su `q` debe buscar exactamente ese objeto/acción en el video.
3. Beat 1 (0-3.5s) DEBE arrancar en frío describiendo exactamente lo que ocurre en pantalla (prohibido saludar o decir "en este video").
4. El último beat cierra con el remate o consecuencia impactante (NO digas "dale like", "comenta amén", "no lo ignores", ni "sígueme").
5. `q` y `fb` SIEMPRE deben describir objetos o acciones físicas reales filmables en Pexels/Pixabay (ej: "cargo ship ocean aerial", "metal welding sparks", "jellyfish deep sea glowing"). Nunca conceptos abstractos.
6. Español natural limpio sin abreviaturas raras ni números con símbolos (escribe "doscientos cincuenta" o "noventa y siete por ciento" en texto claro para voz neural).
"""

    for key in api_keys:
        for model_name in ("gemini-2.5-flash", "gemini-2.5-flash-lite"):
            try:
                client = genai.Client(api_key=key)
                resp = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.85,
                    ),
                )
                raw = (resp.text or "").strip()
                if raw.startswith("```"):
                    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.S)
                ep = json.loads(raw)
                beats = ep.get("beats") or []
                if (
                    isinstance(ep, dict)
                    and ep.get("title")
                    and isinstance(beats, list)
                    and 5 <= len(beats) <= 10
                    and all(b.get("narration") and b.get("q") for b in beats)
                    and _norm_title(ep["title"]) not in posted_norm_titles
                ):
                    ep["id"] = ep_id
                    return ep
            except Exception as e:
                Messenger.warning(f"⚠️ Gemini ({model_name}) falló: {e}")
    return None


def _probe_duration(path: Path) -> float:
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(res.stdout.strip())


async def _edge_tts_save(text: str, out_mp3: Path, rate: str = "+14%"):
    import edge_tts
    comm = edge_tts.Communicate(text, "es-MX-JorgeNeural", rate=rate, pitch="+0Hz")
    await comm.save(str(out_mp3))


def synthesize_beats_voice(beats: list[dict], work_dir: Path) -> tuple[Path, list[float], float]:
    """Synthesizes each beat with tight cadence (~3 words/sec), trims dead air, and returns exact beat durations."""
    clean_wavs: list[Path] = []
    beat_durs: list[float] = []

    for idx, b in enumerate(beats):
        raw_mp3 = work_dir / f"beat_{idx+1:02d}_raw.mp3"
        clean_wav = work_dir / f"beat_{idx+1:02d}_clean.wav"
        text = b["narration"].strip()
        for attempt in range(3):
            try:
                asyncio.run(_edge_tts_save(text, raw_mp3, rate="+14%"))
                if raw_mp3.exists() and raw_mp3.stat().st_size > 1000:
                    break
            except Exception as e:
                Messenger.warning(f"Edge-TTS reintento {attempt+1}: {e}")
                time.sleep(1.5)

        pad = 0.14 if idx < len(beats) - 1 else 0.35
        try:
            subprocess.run([
                "ffmpeg", "-y", "-i", str(raw_mp3),
                "-af", f"silenceremove=start_periods=1:start_duration=0.02:start_threshold=-42dB:stop_periods=-1:stop_duration=0.18:stop_threshold=-42dB,afade=t=in:st=0:d=0.01,apad=pad_dur={pad:.2f}",
                "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(clean_wav),
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            dur = _probe_duration(clean_wav)
            if dur < 0.4:
                raise ValueError("trimmed audio too short")
        except Exception:
            subprocess.run([
                "ffmpeg", "-y", "-i", str(raw_mp3),
                "-af", f"apad=pad_dur={pad:.2f}",
                "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(clean_wav),
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            dur = _probe_duration(clean_wav)
        beat_durs.append(dur)
        clean_wavs.append(clean_wav)

    concat_txt = work_dir / "voice_concat.txt"
    concat_txt.write_text("\n".join(f"file '{w.resolve().as_posix()}'" for w in clean_wavs) + "\n", encoding="utf-8")

    raw_voice = work_dir / "voice_raw.wav"
    dry_voice = work_dir / "voice_dry.wav"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c:a", "pcm_s16le", str(raw_voice)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        subprocess.run(["ffmpeg", "-y", "-i", str(raw_voice), "-af", "loudnorm=I=-14:TP=-1.5:LRA=8", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(dry_voice)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        shutil.copy2(raw_voice, dry_voice)
    total_dur = _probe_duration(dry_voice)
    return dry_voice, beat_durs, total_dur


def build_doc_soundbed(total_dur: float, beat_durs: list[float], out_wav: Path):
    """Synthesizes a 100% copyright-free energetic science documentary pulse & transition whooshes."""
    sr = 48000
    n = int(round(total_dur * sr))
    t = np.arange(n, dtype=np.float32) / sr

    # Deep rhythmic documentary bass pulse (~116 BPM -> beat every 0.517s)
    beat_period = 0.517
    phase_mod = 0.55 + 0.45 * np.exp(-((t % beat_period) * 6.5))
    bed = (
        0.048 * np.sin(2 * np.pi * 55.0 * t)
        + 0.028 * np.sin(2 * np.pi * 110.0 * t + 0.6)
        + 0.015 * np.sin(2 * np.pi * 164.81 * t + 1.2)
    ) * phase_mod

    # Soft muted percussive clock/tick on offbeats
    tick_t = 0.0
    rng = np.random.default_rng(7)
    idx = 0
    while tick_t < total_dur - 0.15:
        i0 = int(tick_t * sr)
        m = min(int(0.04 * sr), n - i0)
        if m > 20:
            lt = np.arange(m, dtype=np.float32) / sr
            freq = 1550.0 if idx % 2 == 0 else 1180.0
            amp = 0.042 if idx % 2 == 0 else 0.024
            bed[i0:i0 + m] += amp * np.exp(-lt * 120.0) * np.sin(2 * np.pi * freq * lt)
        tick_t += beat_period * 0.5
        idx += 1

    # Soft transition whoosh at every visual scene cut
    cursor = 0.0
    for d in beat_durs[:-1]:
        cursor += d
        d_len = 0.28
        i0 = int((cursor - d_len * 0.5) * sr)
        m = int(d_len * sr)
        if 0 <= i0 and i0 + m < n:
            lt = np.arange(m, dtype=np.float32) / sr
            env = np.sin(np.pi * lt / d_len) ** 2
            noise = rng.normal(0, 1, m).astype(np.float32)
            smooth = np.convolve(noise, np.ones(35, dtype=np.float32) / 35.0, mode="same")
            bed[i0:i0 + m] += smooth * env * 0.11

    fi = min(int(0.2 * sr), n)
    fo = min(int(0.6 * sr), n)
    bed[:fi] *= np.linspace(0.0, 1.0, fi, dtype=np.float32)
    bed[-fo:] *= np.linspace(1.0, 0.0, fo, dtype=np.float32)

    pcm = np.clip(bed * 32767.0, -32767, 32767).astype(np.int16)
    stereo = np.column_stack([pcm, pcm]).ravel()
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(stereo.tobytes())


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


def _claim_id(vid: str, used_ids: set[str], used_lock: Optional[threading.Lock]) -> bool:
    if used_lock:
        with used_lock:
            if vid in used_ids:
                return False
            used_ids.add(vid)
            return True
    if vid in used_ids:
        return False
    used_ids.add(vid)
    return True


def _release_id(vid: str, used_ids: set[str], used_lock: Optional[threading.Lock]) -> None:
    if used_lock:
        with used_lock:
            used_ids.discard(vid)
    else:
        used_ids.discard(vid)


def _relevance_score(query: str, text_blob: str) -> int:
    q_tokens = {t for t in re.findall(r"[a-z]{3,}", query.lower()) if t not in {"the", "and", "with", "for", "from"}}
    blob = text_blob.lower()
    return sum(1 for tok in q_tokens if tok in blob)


def _transcode_video_safe(raw_mp4: Path, norm_mp4: Path, dur: float) -> bool:
    try:
        if not raw_mp4.exists() or raw_mp4.stat().st_size < 20_000:
            return False
        raw_dur = _probe_duration(raw_mp4)
        src_args = ["-i", str(raw_mp4)]
        if 0.35 < raw_dur < dur + 0.15:
            reps = max(2, int((dur + 0.5) // raw_dur) + 1)
            loop_txt = raw_mp4.with_suffix(".concat.txt")
            loop_txt.write_text("\n".join(f"file '{raw_mp4.resolve().as_posix()}'" for _ in range(reps)) + "\n", encoding="utf-8")
            src_args = ["-f", "concat", "-safe", "0", "-i", str(loop_txt)]
        vf = "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos+accurate_rnd,crop=1080:1920,setsar=1,cas=strength=0.60,eq=contrast=1.10:saturation=1.16:brightness=-0.01,fps=30"
        subprocess.run([
            "ffmpeg", "-y", *src_args,
            "-t", f"{dur:.3f}", "-vf", vf,
            "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
            str(norm_mp4),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return norm_mp4.exists() and norm_mp4.stat().st_size > 20_000
    except Exception as e:
        Messenger.warning(f"  ⚠️ Clip descartado ({e}), probando siguiente fuente...")
        return False


def _search_pexels_unused(query: str, used_ids: set[str], out_raw: Path, norm_mp4: Path, dur: float, used_lock: Optional[threading.Lock] = None) -> bool:
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
        for orient in ("portrait", None):
            params = {"query": qv, "per_page": 12}
            if orient:
                params["orientation"] = orient
            try:
                r = requests.get("https://api.pexels.com/videos/search", headers={"Authorization": pkey}, params=params, timeout=12)
                if r.status_code != 200:
                    continue
                vids = r.json().get("videos", [])
                # Rank by literal keyword overlap with Pexels slug/URL so visuals match spoken narration
                vids.sort(key=lambda item: _relevance_score(query, str(item.get("url", ""))), reverse=True)
                for v in vids:
                    vid = f"pexels_{v['id']}"
                    if not _claim_id(vid, used_ids, used_lock):
                        continue
                    files = [f for f in v.get("video_files", []) if (f.get("width") or 0) >= 720 or (f.get("height") or 0) >= 720]
                    if not files:
                        files = v.get("video_files", [])
                    if not files:
                        _release_id(vid, used_ids, used_lock)
                        continue
                    files.sort(key=lambda f: abs(min(f.get("width", 0), f.get("height", 0)) - 1080))
                    if _download_stream(files[0]["link"], out_raw) and _transcode_video_safe(out_raw, norm_mp4, dur):
                        Messenger.info(f"  📹 Pexels clip único [{vid}] para '{qv}'")
                        return True
                    _release_id(vid, used_ids, used_lock)
            except Exception:
                continue
    return False


def _search_pixabay_unused(query: str, used_ids: set[str], out_raw: Path, norm_mp4: Path, dur: float, used_lock: Optional[threading.Lock] = None) -> bool:
    pxkey = os.getenv("PIXABAY_API_KEY", "").strip()
    if not pxkey:
        return False
    words = query.strip().split()
    variants = [query.strip(), " ".join(words[:2])] if len(words) >= 2 else [query.strip()]
    for qv in dict.fromkeys(variants):
        try:
            r = requests.get("https://pixabay.com/api/videos/", params={"key": pxkey, "q": qv, "per_page": 12}, timeout=12)
            if r.status_code != 200:
                continue
            hits = r.json().get("hits", [])
            hits.sort(key=lambda item: _relevance_score(query, str(item.get("tags", ""))), reverse=True)
            for h in hits:
                vid = f"pixabay_{h['id']}"
                if not _claim_id(vid, used_ids, used_lock):
                    continue
                v_info = h.get("videos", {}).get("large") or h.get("videos", {}).get("medium") or {}
                url = v_info.get("url")
                if url and _download_stream(url, out_raw) and _transcode_video_safe(out_raw, norm_mp4, dur):
                    Messenger.info(f"  📹 Pixabay clip único [{vid}] para '{qv}'")
                    return True
                _release_id(vid, used_ids, used_lock)
        except Exception:
            continue
    return False


def _create_emergency_motion_clip(norm_mp4: Path, dur: float, idx: int) -> Path:
    """Zero-network animated visual fallback so pipeline never crashes even if all APIs fail."""
    img_path = norm_mp4.with_suffix(".bg.jpg")
    palettes = [((18, 36, 68), (52, 118, 175)), ((42, 22, 62), (140, 62, 130)), ((16, 52, 54), (44, 148, 136))]
    c1, c2 = palettes[idx % len(palettes)]
    arr = np.zeros((1920, 1080, 3), dtype=np.uint8)
    y_grad = np.linspace(0.0, 1.0, 1920, dtype=np.float32)[:, None]
    for ch in range(3):
        arr[:, :, ch] = np.clip(c1[ch] * (1.0 - y_grad) + c2[ch] * y_grad, 0, 255).astype(np.uint8)
    Image.fromarray(arr).save(img_path, quality=92)
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(img_path),
        "-t", f"{dur:.3f}",
        "-vf", "scale=1200:2134,zoompan=z='min(zoom+0.0018,1.18)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,pix_fmt=yuv420p",
        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(norm_mp4),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return norm_mp4


def fetch_and_master_scene(idx: int, beat: dict, dur: float, work_dir: Path, used_ids: set[str], ai_master: AIImageMaster, nasa: NASATool, used_lock: Optional[threading.Lock] = None) -> Path:
    raw_mp4 = work_dir / f"raw_{idx+1:02d}.mp4"
    norm_mp4 = work_dir / f"scene_{idx+1:02d}.mp4"
    q = beat["q"].strip()
    fb = beat.get("fb", q).strip()

    if any(k in q.lower() for k in ("space", "planet", "orbit", "nasa", "rocket", "sun", "solar", "galaxy")):
        try:
            if nasa.fetch_video(q, raw_mp4) and _transcode_video_safe(raw_mp4, norm_mp4, dur):
                return norm_mp4
        except Exception:
            pass

    if _search_pexels_unused(q, used_ids, raw_mp4, norm_mp4, dur, used_lock):
        return norm_mp4
    if _search_pixabay_unused(q, used_ids, raw_mp4, norm_mp4, dur, used_lock):
        return norm_mp4
    if fb != q:
        if _search_pexels_unused(fb, used_ids, raw_mp4, norm_mp4, dur, used_lock):
            return norm_mp4
        if _search_pixabay_unused(fb, used_ids, raw_mp4, norm_mp4, dur, used_lock):
            return norm_mp4

    # Fallback: real stock photo + dynamic Ken Burns (never static or black!)
    photo = work_dir / f"photo_{idx+1:02d}.jpg"
    try:
        if ai_master.fetch_stock_photo(q, photo) or ai_master.fetch_stock_photo(fb, photo):
            if ai_master.create_ken_burns_clip(photo, norm_mp4, duration=dur, motion_style=idx):
                return norm_mp4
    except Exception:
        pass

    # Secondary fallback: AI visual + Ken Burns
    try:
        vp = f"Cinematic vertical 9:16 documentary shot of {q}, realistic lighting, sharp detail, 8k"
        if ai_master.generate_ken_burns_scene(vp, norm_mp4, duration=dur, motion_style=idx, work_dir=work_dir, query=q, fallback_query=fb):
            if norm_mp4.exists() and norm_mp4.stat().st_size > 20_000:
                return norm_mp4
    except Exception:
        pass

    Messenger.warning(f"  🛡️ Activando fondo animado de emergencia para escena {idx+1}")
    return _create_emergency_motion_clip(norm_mp4, dur, idx)


def _fmt_ass(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        s += 1
        cs = 0
    return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"


def _align_script_to_whisper(tokens: list[str], w_words: list[tuple[float, float]], cursor: float, dur: float) -> list[dict]:
    if not tokens:
        return []
    if w_words and len(tokens) == len(w_words):
        return [
            {"word": tok, "start": cursor + max(0.0, ws), "end": cursor + min(dur - 0.03, max(ws + 0.08, we))}
            for tok, (ws, we) in zip(tokens, w_words)
        ]
    # Speech span from Whisper (or full beat minus end pad) distributed by word weight
    span_start = max(0.0, w_words[0][0]) if w_words else 0.0
    span_end = min(dur - 0.04, w_words[-1][1]) if w_words else max(0.25, dur - 0.14)
    if span_end <= span_start + 0.15:
        span_start, span_end = 0.0, max(0.25, dur - 0.14)
    weights = [max(2, len(t)) for t in tokens]
    total_w = sum(weights)
    t_cur = span_start
    out: list[dict] = []
    for tok, wt in zip(tokens, weights):
        seg = (span_end - span_start) * (wt / total_w)
        out.append({"word": tok, "start": cursor + t_cur, "end": cursor + t_cur + seg})
        t_cur += seg
    return out


def make_viral_pop_subtitles(audio_wav: Path, out_ass: Path, beats: Optional[list[dict]] = None, beat_durs: Optional[list[float]] = None, work_dir: Optional[Path] = None):
    """Generates giant 1-2 word pop-in subtitles per beat with exact Spanish script spelling + Whisper voice timing."""
    words: list[dict] = []
    try:
        import torch
        import whisper

        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = whisper.load_model("base", device=device)

        if beats and beat_durs and work_dir:
            cursor = 0.0
            for idx, (b, d) in enumerate(zip(beats, beat_durs)):
                tokens = [t.strip(".,;:!?¿¡").upper() for t in b.get("narration", "").split() if t.strip(".,;:!?¿¡")]
                b_wav = work_dir / f"beat_{idx+1:02d}_clean.wav"
                w_times: list[tuple[float, float]] = []
                if b_wav.exists():
                    res = model.transcribe(str(b_wav), word_timestamps=True, language="es", condition_on_previous_text=False)
                    for seg in res.get("segments", []):
                        for w in seg.get("words", []):
                            ws, we = float(w["start"]), float(w["end"])
                            if w.get("word", "").strip() and ws < d - 0.05 and (we - ws) >= 0.02:
                                w_times.append((ws, we))
                words.extend(_align_script_to_whisper(tokens, w_times, cursor, d))
                cursor += d
        else:
            res = model.transcribe(str(audio_wav), word_timestamps=True, language="es", condition_on_previous_text=False)
            for seg in res.get("segments", []):
                for w in seg.get("words", []):
                    txt = w["word"].strip().strip(".,;:!?¿¡").upper()
                    if txt:
                        words.append({"word": txt, "start": float(w["start"]), "end": float(w["end"])})
    except Exception as e:
        Messenger.warning(f"  ⚠️ Whisper fallback a tiempos por golpe visual ({e})")

    if not words and beats and beat_durs:
        cursor = 0.0
        for b, d in zip(beats, beat_durs):
            tokens = [t.strip(".,;:!?¿¡").upper() for t in b.get("narration", "").split() if t.strip(".,;:!?¿¡")]
            words.extend(_align_script_to_whisper(tokens, [], cursor, d))
            cursor += d

    # Group into 1-2 ultra-punchy words (single big word if length >= 5 or natural pause)
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        # Bold white, heavy black outline (9), 3D drop shadow (4), bottom-center focal zone MarginV=520
        "Style: Pop,Montserrat,96,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,9,4,2,70,70,520,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    i = 0
    while i < len(words):
        cur = words[i]
        nxt = words[i + 1] if i + 1 < len(words) else None
        # Pair short 1-4 char words with next word if gap is small
        if nxt and len(cur["word"]) <= 4 and len(nxt["word"]) <= 7 and (nxt["start"] - cur["end"]) < 0.14:
            pair_words = [cur, nxt]
            i += 2
        else:
            pair_words = [cur]
            i += 1

        seg_start = pair_words[0]["start"]
        next_start = words[i]["start"] if i < len(words) else pair_words[-1]["end"] + 0.35
        seg_end = min(next_start, max(pair_words[-1]["end"] + 0.12, seg_start + 0.25))

        if len(pair_words) == 1:
            txt = f"{{\\fscx108\\fscy108\\t(0,80,\\fscx100\\fscy100)}}{pair_words[0]['word']}"
            lines.append(f"Dialogue: 0,{_fmt_ass(seg_start)},{_fmt_ass(seg_end)},Pop,,0,0,0,,{txt}")
        else:
            # Active word 1 -> active word 2 highlight in warm gold (#FFD43B -> BGR &H003BD4FF)
            mid = pair_words[1]["start"]
            if mid <= seg_start:
                mid = (seg_start + seg_end) * 0.5
            w1, w2 = pair_words[0]["word"], pair_words[1]["word"]
            t1 = f"{{\\c&H003BD4FF&}}{w1}{{\\c&H00FFFFFF&}} {w2}"
            t2 = f"{w1} {{\\c&H003BD4FF&}}{w2}{{\\c&H00FFFFFF&}}"
            lines.append(f"Dialogue: 0,{_fmt_ass(seg_start)},{_fmt_ass(mid)},Pop,,0,0,0,,{t1}")
            lines.append(f"Dialogue: 0,{_fmt_ass(mid)},{_fmt_ass(seg_end)},Pop,,0,0,0,,{t2}")

    out_ass.write_text("\n".join(lines) + "\n", encoding="utf-8")
    Messenger.info(f"  ⚡ Subtítulos Pop-In generados ({len(words)} palabras)")


def make_subtle_watermark_badge(out_png: Path, label: str = "CURIOSIDADES DEL MUNDO"):
    """Small translucent badge top-left (never blocks the hook or video)."""
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(str(FONT_PATH), 22)
    bbox = draw.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([(48, 58), (88 + tw, 102)], radius=20, fill=(10, 15, 25, 165), outline=(255, 255, 255, 90), width=2)
    draw.text((68, 68), label, font=font, fill=(255, 255, 255, 230))
    img.save(out_png)


def produce_micro_doc(ep: dict, force: bool = False) -> Path:
    t0 = time.time()
    out_mp4 = OUT_DIR / f"{ep['id']}.mp4"
    work_dir = SCRATCH_DIR / ep["id"]
    if force and work_dir.exists():
        shutil.rmtree(work_dir, ignore_errors=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    Messenger.info(f"\n🎬 [MICRO-DOC V2] Produciendo: {ep['id']} — {ep['title']}")

    # 1. Voice synthesis per beat (exact visual sync!)
    voice_wav, beat_durs, total_dur = synthesize_beats_voice(ep["beats"], work_dir)
    Messenger.success(f"🎙️ Voz dinámica lista: {total_dur:.2f}s ({len(ep['beats'])} golpes visuales)")

    # 2. Custom copyright-free soundbed + transition whooshes
    bed_wav = work_dir / "soundbed.wav"
    build_doc_soundbed(total_dur, beat_durs, bed_wav)

    # 3. Subtitles + unique real stock video scenes
    ass_path = work_dir / "subtitles.ass"
    make_viral_pop_subtitles(voice_wav, ass_path, beats=ep["beats"], beat_durs=beat_durs, work_dir=work_dir)

    used_ids: set[str] = set()
    used_lock = threading.Lock()
    ai_master = AIImageMaster()
    nasa = NASATool()
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [
            pool.submit(fetch_and_master_scene, i, beat, dur, work_dir, used_ids, ai_master, nasa, used_lock)
            for i, (beat, dur) in enumerate(zip(ep["beats"], beat_durs))
        ]
        clips = [f.result() for f in futures]

    concat_txt = work_dir / "video_concat.txt"
    concat_txt.write_text("\n".join(f"file '{c.resolve().as_posix()}'" for c in clips) + "\n", encoding="utf-8")

    badge_png = work_dir / "badge.png"
    make_subtle_watermark_badge(badge_png)

    try:
        rel_fonts = FONTS_DIR.relative_to(BASE_DIR).as_posix()
        rel_ass = ass_path.relative_to(BASE_DIR).as_posix()
    except Exception:
        rel_fonts = FONTS_DIR.as_posix().replace(":", "\\:")
        rel_ass = ass_path.as_posix().replace(":", "\\:")

    filter_complex = (
        f"[0:v][1:v]overlay=0:0:shortest=1[v_b];"
        f"[v_b]ass='{rel_ass}':fontsdir='{rel_fonts}'[v_out];"
        f"[2:a]volume=1.0[va];"
        f"[3:a]volume=0.28[ba];"
        f"[va][ba]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.92[a_out]"
    )

    is_ci = os.getenv("GITHUB_ACTIONS") == "true" or os.getenv("CI") == "true"
    v_codec = ["-c:v", "libx264", "-preset", "veryfast" if is_ci else "fast", "-crf", "19"]

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-loop", "1", "-framerate", "30", "-i", str(badge_png),
        "-i", str(voice_wav),
        "-i", str(bed_wav),
        "-filter_complex", filter_complex,
        "-map", "[v_out]", "-map", "[a_out]",
        "-t", f"{total_dur:.3f}", "-shortest",
        *v_codec, "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        str(out_mp4),
    ], check=True, cwd=str(BASE_DIR), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    sz = out_mp4.stat().st_size / (1024 * 1024)
    Messenger.success(f"🎉 MICRO-DOC V2 LISTO: {out_mp4.name} ({sz:.1f} MB, {total_dur:.2f}s) en {time.time()-t0:.1f}s")
    return out_mp4


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Viral Micro-Documentary Engine V2 (100% Free & Cloud Automated)")
    parser.add_argument("--single", action="store_true", help="Generate & optionally upload 1 fresh micro-documentary")
    parser.add_argument("--upload", action="store_true", help="Publish to Facebook Reels")
    parser.add_argument("--episode-id", type=str, default="", help="Force specific episode ID from catalog")
    parser.add_argument("--force", action="store_true", help="Force re-render")
    args = parser.parse_args()

    # 1. Check priority pre-rendered override (for FilmCraft/manual queued reels)
    if args.single and not args.episode_id and QUEUE_FILE.exists():
        try:
            q_data = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
            pre_item = q_data.get("pre_rendered_video")
            if isinstance(pre_item, dict) and pre_item.get("file_path"):
                pre_path = BASE_DIR / pre_item["file_path"]
                if pre_path.exists():
                    pre_title = pre_item.get("title", "").strip()
                    pre_desc = pre_item.get("description", "").strip()
                    Messenger.info(f"🎯 [QUEUE PRIORITY] Video pre-renderizado encontrado: {pre_path.name}")
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
        # 1st priority: unused curated episode in micro_doc_catalog.json
        for ep in catalog:
            if counts.get(_norm_title(ep["title"]), 0) == 0:
                target_ep = ep
                break

    if not target_ep:
        # 2nd priority: generate 100% original topic via Gemini
        Messenger.info("✨ Catálogo base cubierto. Generando nuevo guión Micro-Documental con Gemini...")
        fresh = generate_micro_doc_episode(catalog, set(counts.keys()))
        if fresh:
            catalog.append(fresh)
            CATALOG_FILE.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")
            target_ep = fresh
            Messenger.success(f"🆕 Nuevo guión generado: {fresh['id']} — {fresh['title']}")

    if not target_ep and catalog:
        # 3rd priority: least-recently-posted fallback
        target_ep = min(
            enumerate(catalog),
            key=lambda pair: (counts.get(_norm_title(pair[1]["title"]), 0), last_idx.get(_norm_title(pair[1]["title"]), -1), pair[0]),
        )[1]

    if not target_ep:
        Messenger.error("❌ No se pudo seleccionar ni generar ningún episodio.")
        sys.exit(1)

    master_mp4 = produce_micro_doc(target_ep, force=args.force)

    if args.upload and master_mp4.exists():
        fb = FacebookTool(page_id=os.getenv("FACEBOOK_PAGE_ID", ""), access_token=os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", ""))
        res_id = fb.upload_reel(file_path=master_mp4, title=target_ep["title"], description=target_ep.get("description", ""))
        Messenger.success(f"🎉 Reel V2 publicado en Facebook! Video ID: {res_id}")
        today = datetime.date.today().isoformat()
        with open(HISTORY_FILE, "a", encoding="utf-8") as hf:
            hf.write(f"{today},video,{target_ep['title'].replace(',', ' - ')}\n")


if __name__ == "__main__":
    main()
