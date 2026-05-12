import google.auth
import google.auth.transport.requests
import requests
import os

creds, project = google.auth.default()
auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)

location = "us-central1"
project_id = "automatizacion-475715"
# We use the ID from the previous error log
op_id = "6518d17f-d1b2-42c5-b743-cf237b1691b4"

paths = [
    f"projects/{project_id}/locations/{location}/operations/{op_id}",
    f"projects/{project_id}/locations/{location}/publishers/google/models/veo-3.1-fast-generate-001/operations/{op_id}"
]

for path in paths:
    url = f"https://{location}-aiplatform.googleapis.com/v1beta1/{path}"
    print(f"Testing URL: {url}")
    resp = requests.get(url, headers={"Authorization": f"Bearer {creds.token}"})
    print(f"Response: {resp.status_code}")
    if resp.status_code == 200:
        print("✅ SUCCESS!")
        # print(resp.json())
    else:
        print(f"❌ FAILED: {resp.text[:200]}")
