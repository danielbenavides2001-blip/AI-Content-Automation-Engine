from google import genai
import inspect

client = genai.Client(
    vertexai=True,
    project="automatizacion-475715",
    location="us-central1"
)

print(f"Signature of _get_videos_operation: {inspect.signature(client.operations._get_videos_operation)}")
