import base64
import json
import requests

AUDIO_FILE = "test/m____ejj.wav"
API_URL = "http://localhost:8080/api/v1/mcp/tools.call"


with open(AUDIO_FILE, 'rb') as f:
    audio_bytes = f.read()
    base64_audio = base64.b64encode(audio_bytes).decode("utf-8")

print(f"[DEBUG] Encoded base64 length: {len(base64_audio)}")
payload = {
    "method": "tools.call",
    "params": {
        "method": "identify_voice",
        "inputs": [{
            "type": "audio",
            "value": base64_audio
        }]
    }
}

headers = {"Content-Type": "application/json"}
response = requests.post(API_URL, data=json.dumps(payload), headers=headers)

print("Server Response:")
print(response.status_code)
print(response.text)
