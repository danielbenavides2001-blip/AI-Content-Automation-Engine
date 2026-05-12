from google import genai
import os

client = genai.Client(
    vertexai=True,
    project="automatizacion-475715",
    location="us-central1"
)

print(f"Models methods: {[m for m in dir(client.models) if 'operation' in m.lower() or 'video' in m.lower()]}")
