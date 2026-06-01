import os
import httpx
from typing import Any, Callable, Optional

from dotenv import load_dotenv
from google.genai import Client, errors
from pydantic import PrivateAttr
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from tools.common.base_model import BaseModelTool
from tools.common.messenger import Messenger

load_dotenv()


class GeminiUsage(BaseModelTool):
    model: str
    prompt_tokens: Optional[int] = None
    thoughts_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class GeminiBase(BaseModelTool):
    _client: Client = PrivateAttr()
    _location: str = PrivateAttr()
    _ai_studio_client: Optional[Client] = PrivateAttr(default=None)
    _vertex_client: Optional[Client] = PrivateAttr(default=None)

    @property
    def client(self) -> Client:
        return self._client

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        
        project_id = os.getenv("GCP_PROJECT_ID")
        location = os.getenv("GCP_LOCATION", "us-central1")
        self._location = location
        api_key = os.getenv("GEMINI_API_KEY")

        if api_key:
            self._ai_studio_client = Client(api_key=api_key)
        if project_id:
            self._vertex_client = Client(
                vertexai=True,
                project=project_id,
                location=location
            )

        if self._ai_studio_client:
            Messenger.info("🔧 Primary Client: Google AI Studio (API Key) initialized...")
            self._client = self._ai_studio_client
            if self._vertex_client:
                Messenger.info("✨ Backup Client: Vertex AI (Enterprise) initialized as hot standby...")
        elif self._vertex_client:
            Messenger.info(f"✨ Primary Client: Vertex AI (Enterprise) initialized in project: {project_id}...")
            self._client = self._vertex_client
        else:
            raise RuntimeError("❌ GEMINI_API_KEY or GCP_PROJECT_ID is required")

    @retry(
        wait=wait_exponential(multiplier=2, min=5, max=60),
        stop=stop_after_attempt(7),
        retry=retry_if_exception_type((errors.APIError, httpx.RequestError, httpx.RemoteProtocolError, httpx.HTTPError)),
        before_sleep=lambda retry_state: Messenger.warning(
            f"⏳ [Intento {retry_state.attempt_number}/7] Gemini saturado o con error de red: {retry_state.outcome.exception()}. "
            f"Reintentando en {retry_state.next_action.sleep}s..."
        ),
        reraise=True,
    )
    def _execute_with_retry(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """
        Executes a Gemini API call with a robust retry and automatic fallback to Vertex AI on saturation/503.
        """
        def call_api():
            if self._client != self._ai_studio_client and self._ai_studio_client is not None:
                # We are using the Vertex fallback client. Dynamically resolve the models method.
                return self._client.models.generate_content(*args, **kwargs)
            return func(*args, **kwargs)

        try:
            return call_api()
        except (errors.ServerError, errors.ClientError) as e:
            if self._vertex_client and self._client == self._ai_studio_client:
                Messenger.warning(
                    f"⚠️ [HOT FALLBACK] AI Studio está saturado (Error: {e}). "
                    f"Cambiando en caliente al cliente empresarial de Vertex AI..."
                )
                self._client = self._vertex_client
                # Execute immediately on Vertex AI
                return self._client.models.generate_content(*args, **kwargs)
            raise e

    def _extract_usage(self, response: Any, model_name: str) -> GeminiUsage:
        usage_meta = getattr(response, "usage_metadata", None)
        usage = GeminiUsage(model=model_name)

        if usage_meta:
            usage.prompt_tokens = getattr(usage_meta, "prompt_token_count", None)
            usage.thoughts_tokens = getattr(usage_meta, "thoughts_token_count", None)
            usage.output_tokens = getattr(usage_meta, "candidates_token_count", None)
            usage.total_tokens = getattr(usage_meta, "total_token_count", None)

        if usage.total_tokens is not None:
            Messenger.usage(
                model=usage.model,
                prompt=usage.prompt_tokens or 0,
                thoughts=usage.thoughts_tokens or 0,
                output=usage.output_tokens or 0,
                total=usage.total_tokens
            )
        return usage
