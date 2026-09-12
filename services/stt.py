import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
STT_URL = "https://api.groq.com/openai/v1/audio/transcriptions"

def transcribe_audio(
    audio_bytes: bytes,
    filename: str,
    content_type: str
) -> dict:

    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing in .env")

    response = requests.post(
        STT_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}"
        },
        files={
            "file": (
                filename,
                audio_bytes,
                content_type
            )
        },
        data={
            "model": "whisper-large-v3-turbo",
            "response_format": "json"
        },
        timeout=120
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Groq STT error {response.status_code}: {response.text}"
        )

    data = response.json()

    return {
        "text": data.get("text", ""),
        "language": data.get("language"),
        "duration": data.get("duration")
    }