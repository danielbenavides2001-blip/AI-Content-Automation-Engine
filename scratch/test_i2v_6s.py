from google import genai
from google.genai import types
import os
import time
import json
import google.auth
import google.auth.transport.requests
import requests
from pathlib import Path

client = genai.Client(
    vertexai=True,
    project="automatizacion-475715",
    location="us-central1"
)

img_path = "flows/image_content_generator/out_short/ideas/idea_000001/images/scene_01.png"
prompt = "Slow cinematic movement."

print(f"Triggering I2V test with duration 6s...")

operation = client.models.generate_videos(
    model="veo-3.1-fast-generate-001",
    prompt=prompt,
    image=types.Image(
        image_bytes=Path(img_path).read_bytes(),
        mime_type="image/png"
    ),
    config=types.GenerateVideosConfig(
        number_of_videos=1,
        fps=24,
        duration_seconds=6.0,
        aspect_ratio="9:16"
    )
)

op_name = operation.name
resource_name = op_name.rpartition('/operations/')[0]
url = f"https://us-central1-aiplatform.googleapis.com/v1beta1/{resource_name}:fetchPredictOperation"

creds, _ = google.auth.default()
auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)

while True:
    resp = requests.post(url, headers={"Authorization": f"Bearer {creds.token}"}, json={"operationName": op_name})
    data = resp.json()
    done = data.get("done", False)
    print(f"Polling... Done: {done}")
    if done:
        print("RESULT:")
        print(json.dumps(data, indent=2))
        break
    time.sleep(15)
