from google import genai
import os
import time

client = genai.Client(
    vertexai=True,
    project="automatizacion-475715",
    location="us-central1"
)

print("Starting test video (will be interrupted)...")
# We use a very simple prompt to trigger something
# BUT wait! I'll just check if 'operation.done' is a property or a method.
from google.genai import types
op = types.GenerateVideosOperation(name="test")
print(f"Is 'done' a property? {isinstance(getattr(types.GenerateVideosOperation, 'done', None), property)}")
