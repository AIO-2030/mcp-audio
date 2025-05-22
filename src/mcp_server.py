from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import hashlib
from siliconflow_api import transcribe_audio
import base64
import uuid

load_dotenv()

app = Flask(__name__)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route('/api/v1/mcp/voice_model', methods=['POST'])
def handle_audio_upload():
    if 'audio' not in request.files:
        return jsonify({"error": "Missing audio file"}), 400

    file = request.files['audio']
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(file_path)

    audio_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

    try:
        result = transcribe_audio(file_path)
        return jsonify({
            "transcript": result.get("text", ""),
            "confidence": result.get("confidence", 0.9),
            "audio_hash": audio_hash
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/mcp/help', methods=['GET'])
def help_info():
    return jsonify({
        "description": "MCP plugin for SiliconFlow voice transcription",
        "capability_tags": ["voice_recognition", "text_extraction"],
        "methods": [
            {
                "name": "identify_voice",
                "description": "Identify voice from audio file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "audio": {
                            "type": "file",
                            "description": "Audio file"
                        }
                    },
                    "required": ["audio"]
                }
            }
        ],
        "source": {
            "author": "AIO-2030",
            "version": "1.0"
        }
    })


@app.route('/api/v1/mcp/tools.call', methods=['POST'])
def handle_tools_call():
    data = request.get_json()

    method = data.get("params", {}).get("method", "")
    if method != "identify_voice":
        return jsonify({"error": "Unsupported method"}), 400

    inputs = data.get("params", {}).get("inputs", [])
    if not inputs or inputs[0]["type"] != "audio":
        return jsonify({"error": "Missing or invalid audio input"}), 400

    try:
        audio_bytes = base64.b64decode(inputs[0]["value"])
    except Exception:
        return jsonify({"error": "Invalid base64 data"}), 400

    filename = f"{uuid.uuid4().hex}.wav"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(audio_bytes)

    try:
        result = transcribe_audio(file_path)
        audio_hash = hashlib.md5(audio_bytes).hexdigest()
        return jsonify({
            "transcript": result.get("text", ""),
            "confidence": result.get("confidence", 0.9),
            "audio_hash": audio_hash
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("MCP-Audio server starting on http://localhost:8080")
    app.run(host="0.0.0.0", port=8080, debug=True)
