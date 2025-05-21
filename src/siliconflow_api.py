import requests
import os
from dotenv import load_dotenv

load_dotenv()

SILICONFLOW_URL = "https://api.siliconflow.cn/v1/audio/transcriptions"
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

        response = requests.post(SILICONFLOW_URL, headers=headers, files=files, data=data)
        response.raise_for_status()
        return response.json()
