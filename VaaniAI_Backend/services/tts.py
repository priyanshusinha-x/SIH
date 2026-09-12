import io
import edge_tts


VOICE_MAP = {
    "english": "en-IN-NeerjaNeural",
    "en": "en-IN-NeerjaNeural",

    "hindi": "hi-IN-SwaraNeural",
    "hi": "hi-IN-SwaraNeural",

    "bengali": "bn-IN-TanishaaNeural",
    "bn": "bn-IN-TanishaaNeural",

    "marathi": "mr-IN-AarohiNeural",
    "mr": "mr-IN-AarohiNeural",

    "gujarati": "gu-IN-DhwaniNeural",
    "gu": "gu-IN-DhwaniNeural",

    "tamil": "ta-IN-PallaviNeural",
    "ta": "ta-IN-PallaviNeural",

    "telugu": "te-IN-ShrutiNeural",
    "te": "te-IN-ShrutiNeural",

    "kannada": "kn-IN-SapnaNeural",
    "kn": "kn-IN-SapnaNeural",
}


async def text_to_speech(text: str, language: str = "hi"):

    language = (language or "hi").lower().strip()
    voice = VOICE_MAP.get(language, "hi-IN-SwaraNeural")

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice
    )

    audio = io.BytesIO()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio.write(chunk["data"])

    audio_bytes = audio.getvalue()

    if not audio_bytes:
        raise RuntimeError("TTS generated empty audio")

    return audio_bytes, "audio/mpeg"