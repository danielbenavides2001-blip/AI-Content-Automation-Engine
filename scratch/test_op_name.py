from google import genai
import os

client = genai.Client(
    vertexai=True,
    project="automatizacion-475715",
    location="us-central1"
)

# We can't trigger an op, but we can try to find one if it exists
# or we can manually construct what we think it is and see what the SDK does.
print("Testing operation name building...")
from google.genai import types
# Mock an operation
op = types.GenerateVideosOperation(name="projects/123/locations/us-central1/operations/456")
print(f"Mocked Op Name: {op.name}")
# Try to 'get' it via private method to see the URL it generates?
# (We can't see the URL easily without a debugger, but we can guess).
