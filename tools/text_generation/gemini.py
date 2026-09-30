from typing import Any, Type, TypeVar

from pydantic import BaseModel

from tools.common.gemini_base import GeminiBase, GeminiQuotaExhaustedError
from tools.common.messenger import Messenger

T = TypeVar("T", bound=BaseModel)


from google.genai import types

class GeminiTextGenerator(GeminiBase):
    text_model: str = "gemini-2.5-flash"
    fallback_models: list[str] = [
        "gemini-2.5-flash",
        "gemini-3-flash-preview",
        "gemini-3.1-flash-lite",
        "gemini-3.5-flash",
    ]

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def generate_text(self, prompt: str, schema: Type[T]) -> T:
        """
        Generates content with Gemini and parses it into a Pydantic model.
        Automatically cascades to fallback models if the primary model hits its daily quota (429)
        or high-demand saturation (503).
        """
        if not prompt:
             Messenger.error("❌ ERROR: PROMPT VACÍO")
        else:
             Messenger.info(f"DEBUG PROMPT LEN: {len(prompt)}")

        models_to_try = [self.text_model] + [m for m in self.fallback_models if m != self.text_model]
        last_error = None

        for model_name in models_to_try:
            try:
                response = self._execute_with_retry(
                    "models.generate_content",
                    model=model_name,
                    contents=[prompt],
                    config={
                        'response_mime_type': 'application/json',
                        'response_schema': schema,
                        'safety_settings': [
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                                threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                            ),
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                                threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                            ),
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                                threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                            ),
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                                threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                            ),
                        ]
                    }
                )
                self._extract_usage(response, model_name)

                if not response.text:
                    raise RuntimeError(f"❌ No hay respuesta de Gemini ({model_name})")

                return schema.model_validate_json(response.text)
            except (GeminiQuotaExhaustedError, Exception) as e:
                last_error = e
                Messenger.warning(f"⚠️ Modelo '{model_name}' falló o agotó cuota ({type(e).__name__}). Intentando modelo alternativo...")
                continue

        raise RuntimeError(f"❌ Todos los modelos de Gemini fallaron. Último error: {last_error}")

    def generate(self, prompt: str) -> str:
        """
        Generates raw text with Gemini with model fallback cascade.
        """
        models_to_try = [self.text_model] + [m for m in self.fallback_models if m != self.text_model]
        last_error = None

        for model_name in models_to_try:
            try:
                response = self._execute_with_retry(
                    "models.generate_content",
                    model=model_name,
                    contents=[prompt],
                    config={
                        'safety_settings': [
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                                threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                            ),
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                                threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                            ),
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                                threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                            ),
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                                threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                            ),
                        ]
                    }
                )
                self._extract_usage(response, model_name)

                if not response.text:
                    raise RuntimeError(f"No hay respuesta de Gemini ({model_name})")

                return response.text.strip()
            except (GeminiQuotaExhaustedError, Exception) as e:
                last_error = e
                Messenger.warning(f"⚠️ Modelo '{model_name}' falló ({type(e).__name__}). Intentando modelo alternativo...")
                continue

        raise RuntimeError(f"❌ Todos los modelos de Gemini fallaron. Último error: {last_error}")

    def translate_srt(self, srt_content: str, target_language: str = "English") -> str:
        """
        Translates an SRT subtitle file to the target language while strictly preserving timestamps and SRT format.
        """
        prompt = f"""
You are a professional subtitle translator. Translate the following SRT file to {target_language}.
CRITICAL RULES:
1. Preserve the exact SRT format (subtitle number, timestamps).
2. DO NOT change or modify the timestamps (e.g. 00:00:01,000 --> 00:00:04,000).
3. Translate ONLY the subtitle text.
4. Keep the translation concise so it fits the timing on screen.
5. Do NOT add any markdown formatting, headers, or conversational text. Output ONLY the raw SRT format.

SRT CONTENT:
{srt_content}
"""
        models_to_try = [self.text_model] + [m for m in self.fallback_models if m != self.text_model]
        last_error = None

        for model_name in models_to_try:
            try:
                response = self._execute_with_retry(
                    "models.generate_content",
                    model=model_name,
                    contents=[prompt],
                    config={
                        'safety_settings': [
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                                threshold=types.HarmBlockThreshold.BLOCK_NONE,
                            ),
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                                threshold=types.HarmBlockThreshold.BLOCK_NONE,
                            ),
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                                threshold=types.HarmBlockThreshold.BLOCK_NONE,
                            ),
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                                threshold=types.HarmBlockThreshold.BLOCK_NONE,
                            ),
                        ]
                    }
                )
                self._extract_usage(response, model_name)
                
                if not response.text:
                    raise RuntimeError(f"❌ No hay respuesta de Gemini en la traducción ({model_name}).")
                    
                translated_srt = response.text.strip()
                # Remove markdown code blocks if gemini added them accidentally
                if translated_srt.startswith("```srt"):
                    translated_srt = translated_srt[6:]
                if translated_srt.startswith("```"):
                    translated_srt = translated_srt[3:]
                if translated_srt.endswith("```"):
                    translated_srt = translated_srt[:-3]
                    
                return translated_srt.strip()
            except (GeminiQuotaExhaustedError, Exception) as e:
                last_error = e
                Messenger.warning(f"⚠️ Modelo '{model_name}' falló en traducción ({type(e).__name__}). Intentando modelo alternativo...")
                continue

        raise RuntimeError(f"❌ Todos los modelos de Gemini fallaron en traducción. Último error: {last_error}")

