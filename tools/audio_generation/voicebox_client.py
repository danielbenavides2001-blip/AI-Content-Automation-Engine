import os
import time
import requests
import subprocess
from pathlib import Path
from typing import Optional
from tools.common.messenger import Messenger

VOICEBOX_BASE_URL = os.getenv("VOICEBOX_URL", "http://127.0.0.1:17493")
DEFAULT_PROFILE_ID = "e294f4c2-3dc3-42af-bfa5-51a6492a28b9"  # XpressTV (Curiosidades Virales)

class VoiceboxClient:
    """
    Client for local Voicebox neural voice synthesis with automatic chunking,
    robust queue polling, and retry mechanisms on CUDA.
    Zero fallback to cloud TTS ensures 100% voice authenticity.
    """

    def __init__(self, profile_id: str = DEFAULT_PROFILE_ID):
        self.profile_id = profile_id
        self.base_url = VOICEBOX_BASE_URL.rstrip("/")

    def is_available(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/health", timeout=3.0)
            return r.status_code == 200 and r.json().get("status") == "healthy"
        except Exception:
            return False

    def synthesize_sentence(self, text: str, out_wav: Path, max_retries: int = 5) -> bool:
        """Synthesizes a single chunk via Voicebox API with persistent queue waiting and retries."""
        url = f"{self.base_url}/generate"
        payload = {
            "profile_id": self.profile_id,
            "text": text.strip(),
            "language": "es"
        }

        for attempt in range(max_retries):
            try:
                res = requests.post(url, json=payload, timeout=60)
                if res.status_code != 200:
                    Messenger.warning(f"Voicebox generate HTTP {res.status_code} (intento {attempt+1}/{max_retries}): {res.text}")
                    time.sleep(2.0)
                    continue

                gen_id = res.json().get("id")
                if not gen_id:
                    time.sleep(1.0)
                    continue

                # Poll status for up to 600s (10 min) allowing parallel queues to finish
                for _ in range(1200):
                    time.sleep(0.5)
                    try:
                        st_res = requests.get(f"{self.base_url}/history/{gen_id}", timeout=10)
                        if st_res.status_code == 200:
                            data = st_res.json()
                            status = data.get("status")
                            if status == "completed":
                                audio_res = requests.get(f"{self.base_url}/audio/{gen_id}", timeout=20)
                                if audio_res.status_code == 200 and len(audio_res.content) > 1000:
                                    out_wav.parent.mkdir(parents=True, exist_ok=True)
                                    out_wav.write_bytes(audio_res.content)
                                    return True
                            elif status == "failed":
                                Messenger.warning(f"Voicebox tarea {gen_id} falló: {data.get('error')}. Reintentando...")
                                break
                    except Exception:
                        time.sleep(1.0)
            except Exception as e:
                Messenger.warning(f"Voicebox intento {attempt+1}/{max_retries} excepción: {e}")
                time.sleep(2.0)

        return False

    def synthesize_full_narration(self, text: str, out_path: Path) -> float:
        """
        Synthesizes long narration text by chunking, synthesizing each chunk with Voicebox,
        and concatenating them into out_path (wav or mp3).
        Strictly requires Voicebox to maintain 100% authentic XpressTV cloned voice.
        """
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.is_available():
            # Wait up to 15 seconds for Voicebox server to respond
            for _ in range(5):
                time.sleep(3.0)
                if self.is_available():
                    break
            if not self.is_available():
                raise RuntimeError("Voicebox Local Server no está disponible en http://127.0.0.1:17493. No se permite fallback.")

        Messenger.info(f"🎙️ [Voicebox Local CUDA] Sintetizando narración con voz clonada XpressTV...")
        import re
        raw_sentences = [s.strip() for s in re.split(r'(?<=[.?!])\s+', text) if s.strip()]
        
        # Agrupar en bloques de 25-35 palabras para máxima fluidez y evitar sobrecarga de GPU
        chunks = []
        curr = []
        curr_words = 0
        for s in raw_sentences:
            w_count = len(s.split())
            if curr and curr_words + w_count > 30:
                chunks.append(" ".join(curr))
                curr = [s]
                curr_words = w_count
            else:
                curr.append(s)
                curr_words += w_count
        if curr:
            chunks.append(" ".join(curr))

        chunk_wavs = []
        scratch_dir = out_path.parent / f"vb_chunks_{int(time.time())}"
        scratch_dir.mkdir(parents=True, exist_ok=True)

        for idx, c_text in enumerate(chunks):
            c_wav = scratch_dir / f"chunk_{idx:03d}.wav"
            Messenger.info(f"  🎙️ [Voicebox {idx+1}/{len(chunks)}]: {c_text[:45]}...")
            ok = self.synthesize_sentence(c_text, c_wav)
            if ok and c_wav.exists() and c_wav.stat().st_size > 5000:
                chunk_wavs.append(c_wav)
            else:
                raise RuntimeError(f"Falla crítica: Voicebox no pudo generar el Chunk {idx+1}/{len(chunks)}. Abortando para no usar fallback.")

        # Concatenate all wav chunks using ffmpeg concat filter
        concat_list = scratch_dir / "concat.txt"
        with open(concat_list, "w", encoding="utf-8") as f:
            for cw in chunk_wavs:
                f.write(f"file '{cw.resolve().as_posix()}'\n")

        temp_master = scratch_dir / "master.wav"
        cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(temp_master)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Export to destination path (wav or mp3)
        if out_path.suffix.lower() == ".mp3":
            cmd_mp3 = ["ffmpeg", "-y", "-i", str(temp_master), "-c:a", "libmp3lame", "-b:a", "192k", str(out_path)]
            subprocess.run(cmd_mp3, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            import shutil
            shutil.copy(temp_master, out_path)

        # Cleanup scratch chunks
        for cw in chunk_wavs:
            try: cw.unlink()
            except Exception: pass
        try: concat_list.unlink()
        except Exception: pass
        try: temp_master.unlink()
        except Exception: pass
        try: scratch_dir.rmdir()
        except Exception: pass

        dur = self._get_duration(out_path)
        Messenger.success(f"✅ Master audio Voicebox (XpressTV CUDA) generado con éxito ({dur:.2f}s)")
        return dur

    def _get_duration(self, path: Path) -> float:
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
        res = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return float(res.stdout.strip())
