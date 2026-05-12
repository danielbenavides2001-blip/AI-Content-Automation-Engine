from google import genai
import os

client = genai.Client(
    vertexai=True,
    project="automatizacion-475715",
    location="us-central1"
)

# We won't trigger a real video (expensive), we just check the client structure
print(f"Client type: {type(client)}")
print(f"Models type: {type(client.models)}")
print(f"Operations type: {type(client.operations)}")
print(f"Operations methods: {dir(client.operations)}")
