import os
import time
import requests
import subprocess
from pathlib import Path
from typing import Optional
from tools.common.messenger import Messenger

VOICEBOX_BASE_URL = os.getenv("VOICEBOX_URL", "http://127.0.0.1:17493")
DEFAULT_PROFILE_ID = "8f037919-95d5-4ee1-9dd5-59c5082f8f53"  # El Porqué de Todo (Voz Cinematográfica)

class VoiceboxClient:
    """
    Client for local Voicebox neural voice synthesis with automatic chunking,
    polling, and cloud fallback (Edge-TTS).
    """

    def __init__(self, profile_id: str = DEFAULT_PROFILE_ID):
        self.profile_id = profile_id
        self.base_url = VOICEBOX_BASE_URL.rstrip("/")

    def is_available(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/health", timeout=1.5)
            return r.status_code == 200 and r.json().get("status") == "healthy"
        except Exception:
            return False

    def synthesize_sentence(self, text: str, out_wav: Path) -> bool:
        """Synthesizes a single chunk via Voicebox API."""
        try:
            url = f"{self.base_url}/generate"
            payload = {
                "profile_id": self.profile_id,
                "text": text.strip(),
                "language": "es"
            }
            res = requests.post(url, json=payload, timeout=15)
            if res.status_code != 200:
                Messenger.warning(f"Voicebox generate error {res.status_code}: {res.text}")
                return False

            gen_id = res.json().get("id")
            if not gen_id:
                return False

            # Poll status with responsive 0.4s interval for fast CUDA response
            for _ in range(250):
                time.sleep(0.4)
                st_res = requests.get(f"{self.base_url}/history/{gen_id}", timeout=5)
                if st_res.status_code == 200:
                    data = st_res.json()
                    status = data.get("status")
                    if status == "completed":
                        audio_res = requests.get(f"{self.base_url}/audio/{gen_id}", timeout=15)
                        if audio_res.status_code == 200 and len(audio_res.content) > 1000:
                            out_wav.parent.mkdir(parents=True, exist_ok=True)
                            out_wav.write_bytes(audio_res.content)
                            return True
                    elif status == "failed":
                        Messenger.warning(f"Voicebox task {gen_id} failed: {data.get('error')}")
                        return False
            return False
        except Exception as e:
            Messenger.warning(f"Voicebox synthesis exception: {e}")
            return False

    def synthesize_full_narration(self, text: str, out_path: Path) -> float:
        """
        Synthesizes long narration text by chunking, synthesizing each chunk,
        and concatenating them into out_path (wav or mp3).
        Falls back to Edge-TTS if Voicebox is unavailable.
        """
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if self.is_available():
            Messenger.info(f"🎙️ [Voicebox Local] Sintetizando con 'El Porqué de Todo (Voz Cinematográfica)'...")
            import re
            raw_sentences = [s.strip() for s in re.split(r'(?<=[.?!])\s+', text) if s.strip()]
            
            # Agrupar en bloques de 2-3 frases (~30 a 45 palabras) para máxima naturalidad y velocidad
            chunks = []
            curr = []
            curr_words = 0
            for s in raw_sentences:
                w_count = len(s.split())
                if curr and curr_words + w_count > 38:
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

            all_succeeded = True
            for idx, c_text in enumerate(chunks):
                c_wav = scratch_dir / f"chunk_{idx:03d}.wav"
                Messenger.info(f"  🎙️ [Voicebox {idx+1}/{len(chunks)}]: {c_text[:45]}...")
                ok = self.synthesize_sentence(c_text, c_wav)
                if ok and c_wav.exists() and c_wav.stat().st_size > 5000:
                    chunk_wavs.append(c_wav)
                else:
                    Messenger.warning(f"  ⚠️ Chunk {idx+1} falló en Voicebox.")
                    all_succeeded = False
                    break

            if all_succeeded and chunk_wavs:
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
                Messenger.success(f"✅ Master audio Voicebox generado con éxito ({dur:.2f}s)")
                return dur

        # Fallback to Edge-TTS (Cloud or when Voicebox is offline)
        Messenger.warning("⚠️ Voicebox no disponible o falló. Activando fallback neuronal (es-CO-GonzaloNeural)...")
        import asyncio
        import edge_tts
        async def _run_edge():
            comm = edge_tts.Communicate(text, "es-CO-GonzaloNeural", rate="+3%")
            await comm.save(str(out_path))
        asyncio.run(_run_edge())

        dur = self._get_duration(out_path)
        Messenger.success(f"✅ Fallback audio generado ({dur:.2f}s)")
        return dur

    def _get_duration(self, path: Path) -> float:
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
        res = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return float(res.stdout.strip())
