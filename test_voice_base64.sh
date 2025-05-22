#!/bin/bash

AUDIO_FILE="test/m____ejj.wav"
OUTPUT_JSON="tools_call_payload.json"
API_URL="http://localhost:8080/api/v1/mcp/tools.call"

if [ ! -f "$AUDIO_FILE" ]; then
  echo "Audio file '$AUDIO_FILE' not found!"
  exit 1
fi

BASE64_AUDIO=$(base64 "$AUDIO_FILE" | tr -d '\n')

cat > "$OUTPUT_JSON" <<EOF
{
  "method": "tools.call",
  "params": {
    "method": "identify_voice",
    "inputs": [
      {
        "type": "audio",
        "value": "$BASE64_AUDIO"
      }
    ]
  }
}
EOF

curl -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d @"$OUTPUT_JSON"

rm "$OUTPUT_JSON"
