import requests
import os

AUDIO_URL = os.getenv("AUDIO_URL")
API_KEY = os.getenv("API_KEY")

def transcribe_audio(file_path):
    with open(file_path, 'rb') as f:
        files = {
            'file': f,
        }
        data = {
            'model': 'FunAudioLLM/SenseVoiceSmall'
        }
        headers = {
            'Authorization': f'Bearer {API_KEY}'
        }

        response = requests.post(AUDIO_URL, headers=headers, files=files, data=data)
        response.raise_for_status()
        return response.json()
