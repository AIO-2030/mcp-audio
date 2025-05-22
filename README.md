# MCP-Audio Plugin

`mcp-audio` is an AIO-2030 compliant MCP plugin that performs voice-to-text transcription using the Audio speech recognition API.

It exposes the `identify_voice` method via both `multipart/form-data` and `base64` formats, supports the AIO `tools.call` protocol, and returns JSON-RPC structured outputs.

---

## Features

- Fully AIO-compliant MCP plugin (`/tools.call`, `/help`)
- Converts `.wav`/`.mp3` audio files to transcripts using SiliconFlow
- API key managed securely via `.env` file
- Docker-compatible and minimal dependencies
- Registration-ready for AIO endpoint registry

---

##  Setup (Local)

### 1. Clone and Install

```bash
git clone git@github.com:AIO-2030/mcp-audio.git
cd mcp-audio
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Add .env file
```bash
cp .env.example .env
```

Set your audio URL and API key:

```
AUDIO_URL=https--xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Run the MCP server

```bash
python src/mcp_server.py
```

### 4. Docker

#### 4.1 Build and Run
```bash
docker build -t mcp-audio .
docker run --env-file .env -p 8080:8080 mcp-audio
```

## API Overview

### POST /api/v1/mcp/voice_model

Upload audio file directly. Response:

```json
{
  "transcript": "hello world",
  "confidence": 0.91,
  "audio_hash": "a1b2c3..."
}
```

### POST /api/v1/mcp/tools.call (AIO Protocol)

JSON-RPC format with base64-encoded audio. Response:

```json
{
  "method": "tools.call",
  "params": {
    "method": "identify_voice",
    "inputs": [
      {
        "type": "audio",
        "value": "<base64-audio>"
      }
    ]
  }
}
```

### GET /api/v1/mcp/help
Auto-serves contents of mcp_audio_registration.json. Used by Queen AI for MCP discovery and service indexing.

## Testing Tools

### Base64 Voice Test
```bash
python test/test_audio_base64.py
```

### Health Check
```bash
python health_check.py
```

## MCP Registration (to AIO Endpoint Canister)
```bash
./register_mcp.sh
```
Requires jq, dfx, and a running endpoint_registry canister.
