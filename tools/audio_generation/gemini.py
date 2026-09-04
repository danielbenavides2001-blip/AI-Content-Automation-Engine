import random
import time
import wave
from pathlib import Path
from typing import Any

from google.genai import types

from tools.common.gemini_base import GeminiBase
from tools.common.messenger import Messenger


class GeminiAudioGenerator(GeminiBase):
    tts_model: str = "gemini-2.5-flash-preview-tts"
    voice_name: str = "Fenrir"
    _last_call_time: float = 0.0

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        # La modalidad de audio preview solo existe en claves de Gemini Developer API, no en Vertex AI
        self._clients_info = [c for c in self._clients_info if not c["is_vertex"]]
        if not self._clients_info:
            raise RuntimeError("❌ Se requiere al menos una GEMINI_API_KEY para Gemini Audio TTS")

    def _rotate_to_next_client(self) -> bool:
        if not self._clients_info:
            return False
        self._client_index = (self._client_index + 1) % len(self._clients_info)
        Messenger.info(f"🔄 Rotando clave de audio a cliente #{self._client_index + 1}/{len(self._clients_info)}")
        return True

    def text_to_speech(
        self,
        text: str,
        audio_path: Path,
    ) -> None:
        """
        Generates audio using Gemini TTS and saves it to disk.
        Applies adaptive rate-limiting only when calls are too frequent.
        """
        now = time.time()
        min_gap = 2.0
        if now - self._last_call_time < min_gap:
            actual_delay = min_gap - (now - self._last_call_time) + random.uniform(0.5, 1.5)
            Messenger.info(f"Rate-limiting TTS: waiting {actual_delay:.1f}s")
            time.sleep(actual_delay)
        self._last_call_time = time.time()

        audio_path.parent.mkdir(parents=True, exist_ok=True)

        response = self._execute_with_retry(
            "models.generate_content",
            model=self.tts_model,
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=self.voice_name,
                        )
                    )
                ),
            ),
        )
        self._extract_usage(response, self.tts_model)

        pcm_chunks: list[bytes] = []
        if response.parts:
            for part in response.parts:
                if part.text:
                    Messenger.info(f"Gemini thoughts: {part.text}")
                elif part.inline_data and part.inline_data.data:
                    pcm_chunks.append(part.inline_data.data)

        if not pcm_chunks:
            raise RuntimeError("❌ No se encontró audio en la respuesta de Gemini")

        combined_pcm = b"".join(pcm_chunks)
        self._write_wav(audio_path, combined_pcm)
        Messenger.audio(f"Audio generado: {audio_path}")

    def _write_wav(
        self,
        filename: Path,
        pcm_data: bytes,
        *,
        sample_rate: int = 24000,
        channels: int = 1,
        sample_width: int = 2,
    ) -> None:
        """
        Writes raw PCM data to a WAV file.
        """
        with wave.open(str(filename), "wb") as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(sample_width)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(pcm_data)
