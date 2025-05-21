#!/bin/bash

base64_data=$(base64 -w 0 test/m____ejj.wav)

curl -X POST http://localhost:9090/api/v1/mcp/tools.call \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools.call",
    "params": {
      "method": "identify_voice",
      "inputs": [
        {
          "type": "audio",
          "value": "'"$base64_data"'"
        }
      ]
    }
  }'
