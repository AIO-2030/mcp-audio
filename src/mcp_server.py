import json

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
    try:
        with open(os.path.join(os.path.dirname(__file__), "../mcp_audio_registration.json")) as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": "Failed to load help content", "details": str(e)}), 50


@app.route('/api/v1/mcp/tools.call', methods=['POST'])
def handle_tools_call():
    try:
        data = request.get_json()

        if not data or "params" not in data:
            return jsonify({"error": "Missing 'params' in request"}), 400

        method = data["params"].get("method", "")
        if method != "identify_voice":
            return jsonify({"error": "Unsupported method"}), 400

        inputs = data["params"].get("inputs")
        if not isinstance(inputs, list) or not inputs:
            return jsonify({"error": "Missing or invalid 'inputs' list"}), 400

        first_input = inputs[0]
        if not isinstance(first_input, dict) or first_input.get("type") != "audio":
            return jsonify({"error": "First input must be of type 'audio'"}), 400

        base64_data = first_input.get("value")
        if not base64_data:
            return jsonify({"error": "Missing 'value' in audio input"}), 400

        # Decode and save
        audio_bytes = base64.b64decode(base64_data)
        filename = f"{uuid.uuid4().hex}.wav"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(audio_bytes)

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
