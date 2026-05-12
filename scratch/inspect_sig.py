from google import genai
import os
import time

client = genai.Client(
    vertexai=True,
    project="automatizacion-475715",
    location="us-central1"
)

# Trigger a very small operation if possible, or just check the return type
print("Checking operation type and methods...")
# Since I can't easily trigger a fake operation without quota, I'll assume 
# it's a standard operation object.

# BUT wait! I'll try to use the model ID to get a dummy operation name if possible.
# Actually, I'll just check if 'client.models.generate_videos' has a 'wait' parameter.
import inspect
print(f"generate_videos signature: {inspect.signature(client.models.generate_videos)}")
