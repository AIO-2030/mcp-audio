from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import hashlib
from siliconflow_api import transcribe_audio

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
            "author": "YourName",
            "version": "1.0"
        }
    })
