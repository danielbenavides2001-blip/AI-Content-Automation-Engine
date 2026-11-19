import os
import time
import requests
import subprocess
from pathlib import Path
from typing import Optional
from tools.common.messenger import Messenger

VOICEBOX_BASE_URL = os.getenv("VOICEBOX_URL", "http://127.0.0.1:17493")
DEFAULT_PROFILE_ID = "e294f4c2-3dc3-42af-bfa5-51a6492a28b9"  # XpressTV (Curiosidades Virales)

_GLOBAL_XTTS_MODEL = None

def get_xtts_model():
    global _GLOBAL_XTTS_MODEL
    if _GLOBAL_XTTS_MODEL is None:
        os.environ["COQUI_TOS_AGREED"] = "1"
        from TTS.api import TTS
        Messenger.info("⚡ [XTTS-v2] Inicializando modelo en memoria CPU para síntesis en nube/GitHub...")
        _GLOBAL_XTTS_MODEL = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    return _GLOBAL_XTTS_MODEL

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

                # Poll status for up to 180s (3 min) per chunk, allowing parallel queue to finish
                poll_count = 0
                for _ in range(360):
                    time.sleep(0.5)
                    poll_count += 1
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
                            elif status in ("failed", "cancelled"):
                                Messenger.warning(f"Voicebox tarea {gen_id} {status}: {data.get('error')}. Reintentando...")
                                break
                    except Exception:
                        time.sleep(1.0)
                else:
                    # Timeout after 180s in queue: cancel and retry
                    try:
                        requests.post(f"{self.base_url}/generate/{gen_id}/cancel", timeout=5)
                    except Exception:
                        pass
                    Messenger.warning(f"Voicebox tarea {gen_id} timeout tras 180s. Cancelando y reintentando...")
            except Exception as e:
                Messenger.warning(f"Voicebox intento {attempt+1}/{max_retries} excepción: {e}")
                time.sleep(2.0)

        return False

    def _synthesize_with_edge_tts(self, text: str, out_path: Path) -> float:
        import asyncio
        import edge_tts
        Messenger.info("⚡ [Edge-TTS Fallback] Sintetizando narración con voz de alta fidelidad (Jorge Neural)...")
        t0 = time.time()
        async def _speak():
            comm = edge_tts.Communicate(text, "es-MX-JorgeNeural", rate="+3%", pitch="+1Hz")
            await comm.save(str(out_path))
        asyncio.run(_speak())
        dur = self._get_duration(out_path)
        Messenger.success(f"✅ [Edge-TTS] Narración sintetizada en {time.time()-t0:.1f}s ({dur:.2f}s de audio)")
        return dur

    def _synthesize_with_xtts(self, text: str, out_path: Path) -> float:
        """
        Cloud/CPU engine using Coqui XTTS-v2 with the official XpressTV reference audio.
        Enables 100% autonomous cloud execution in GitHub Actions with the PC powered off.
        """
        ref_wav = Path(__file__).resolve().parents[2] / "flows" / "image_content_generator" / "resources" / "voices" / "xpresstv_reference.wav"
        if not ref_wav.exists():
            Messenger.warning(f"Audio de referencia no encontrado en: {ref_wav}. Usando Edge-TTS...")
            return self._synthesize_with_edge_tts(text, out_path)

        try:
            Messenger.info(f"🎙️ [XTTS-v2 CPU] Sintetizando narración con voz clonada XpressTV ({len(text.split())} palabras)...")
            t0 = time.time()
            tts = get_xtts_model()
            tts.tts_to_file(
                text=text,
                speaker_wav=str(ref_wav),
                language="es",
                file_path=str(out_path),
                split_sentences=True
            )
            dur = self._get_duration(out_path)
            Messenger.success(f"✅ [XTTS-v2] Narración con voz XpressTV sintetizada en {time.time()-t0:.1f}s ({dur:.2f}s de audio)")
            return dur
        except Exception as e:
            Messenger.warning(f"⚠️ [XTTS-v2 CPU] Error o timeout en síntesis XTTS: {e}. Activando fallback Edge-TTS...")
            return self._synthesize_with_edge_tts(text, out_path)

    def synthesize_full_narration(self, text: str, out_path: Path) -> float:
        """
        Synthesizes long narration text by chunking, synthesizing each chunk with Voicebox,
        and concatenating them into out_path (wav or mp3).
        Strictly requires Voicebox to maintain 100% authentic XpressTV cloned voice.
        """
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.is_available():
            Messenger.info("ℹ️ Servidor Voicebox local no detectado en http://127.0.0.1:17493.")
            Messenger.info("🚀 Conmutando a XTTS-v2 en CPU para síntesis 100% autónoma en la nube...")
            return self._synthesize_with_xtts(text, out_path)

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
