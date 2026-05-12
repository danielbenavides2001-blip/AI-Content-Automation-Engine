from google import genai
import os

client = genai.Client(
    vertexai=True,
    project="automatizacion-475715",
    location="us-central1"
)

# We'll try to find the operation by just its name if it's an absolute path
# If operation.name starts with 'projects/', we can try to use it directly.
print("Exploring operations...")
# Since we don't have a real op name right now, we can't test much.
# BUT I'll try to see if 'client.operations.get' accepts a full path.
