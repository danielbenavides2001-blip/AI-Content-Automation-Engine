from google import genai
import os

client = genai.Client(
    vertexai=True,
    project="automatizacion-475715",
    location="us-central1"
)

print("Listing models...")
for model in client.models.list():
    if "veo" in model.name.lower() or "video" in model.name.lower():
        print(f"- {model.name} (Capabilities: {model.supported_actions})")
