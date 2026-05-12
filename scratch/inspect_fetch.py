import google.auth
import google.auth.transport.requests
import requests
import json

creds, project = google.auth.default()
auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)

location = "us-central1"
# We use the ID from the previous successful (but "empty") run
op_name = "projects/automatizacion-475715/locations/us-central1/publishers/google/models/veo-3.1-fast-generate-001/operations/beae2abf-83b8-4348-a140-b4725628b600"
resource_name = op_name.rpartition('/operations/')[0]

url = f"https://{location}-aiplatform.googleapis.com/v1beta1/{resource_name}:fetchPredictOperation"
headers = {
    "Authorization": f"Bearer {creds.token}",
    "Content-Type": "application/json"
}
data = {"operationName": op_name}

resp = requests.post(url, headers=headers, json=data)
print(f"Status: {resp.status_code}")
print(json.dumps(resp.json(), indent=2))
