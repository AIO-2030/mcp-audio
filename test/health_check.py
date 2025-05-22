import requests
import json
import base64

HELP_URL = "http://localhost:8080/api/v1/mcp/help"
TOOLS_CALL_URL = "http://localhost:8080/api/v1/mcp/tools.call"

def check_help():
    print("🔍 Checking /api/v1/mcp/help ...")
    try:
        r = requests.get(HELP_URL)
        r.raise_for_status()
        data = r.json()
        assert "methods" in data
        print("/api/v1/mcp/help OK:", json.dumps(data["methods"], indent=2))
    except Exception as e:
        print("/api/v1/mcp/help FAILED:", str(e))


def check_tools_call_stub():
    print("Checking /tools.call minimal response ...")
    try:
        payload = {
            "method": "tools.call",
            "params": {
                "method": "identify_voice",
                "inputs": [
                    {
                        "type": "audio",
                        "value": base64.b64encode(b"fake").decode()
                    }
                ]
            }
        }
        r = requests.post(TOOLS_CALL_URL, json=payload)
        if r.status_code == 200:
            print(" /api/v1/mcp/tools.call OK:", r.json())
        else:
            print(f"/api/v1/mcp/tools.call responded with status {r.status_code}")
            print(r.text)
    except Exception as e:
        print("/api/v1/mcp/tools.call FAILED:", str(e))


if __name__ == "__main__":
    print("MCP Audio Plugin Health Check\n")
    check_help()
    check_tools_call_stub()
