import google.auth
import google.auth.transport.requests
import requests

creds, project = google.auth.default()
auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)

location = "us-central1"
op_name = "projects/automatizacion-475715/locations/us-central1/publishers/google/models/veo-3.1-fast-generate-001/operations/1796fdff-9f91-458e-b46e-573ee97c6d44"

versions = ["v1", "v1beta1"]

for v in versions:
    url = f"https://{location}-aiplatform.googleapis.com/{v}/{op_name}"
    print(f"Testing URL ({v}): {url}")
    resp = requests.get(url, headers={"Authorization": f"Bearer {creds.token}"})
    print(f"Response: {resp.status_code}")
    if resp.status_code == 200:
        print("✅ SUCCESS!")
        print(resp.json().get("done"))
    else:
        print(f"❌ FAILED: {resp.text[:100]}")
