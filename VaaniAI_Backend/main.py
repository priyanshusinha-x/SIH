import os
from dotenv import load_dotenv

# Load .env first
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from services.grok import grok_process
from services.santhali import translate_hindi_to_santhali
from services.stt import transcribe_audio
from services.tts import text_to_speech
from services.santhali import translate_hindi_to_santhali
from models.schemas import TextRequest, ProcessResponse

app = FastAPI(
    title="VaaniAI Backend",
    description="SIH backend for multilingual voice learning using xAI Grok",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "VaaniAI backend is running", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/process", response_model=ProcessResponse)
async def process_text(request: TextRequest):
    try:
        # For Santhali, use Groq for educational explanation
# and IndicTrans2 for the actual Santhali translation.
if request.target_language.lower() == "santhali":

    result = grok_process(
        text=request.text,
        source_language=request.source_language,
        target_language="Hindi"
    )

    result["translation"] = translate_hindi_to_santhali(request.text)

else:

    result = grok_process(
        text=request.text,
        source_language=request.source_language,
        target_language=request.target_language
    )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/api/voice")
async def process_voice(
    file: UploadFile = File(...),
    target_language: str = "Hindi"
):
    try:
        audio = await file.read()

        if not audio:
            raise HTTPException(status_code=400, detail="Empty audio file")

        transcript = transcribe_audio(
            audio_bytes=audio,
            filename=file.filename or "audio.webm",
            content_type=file.content_type or "audio/webm"
        )

        result = grok_process(
            text=transcript["text"],
            source_language=transcript.get("language", "auto"),
            target_language=target_language
        )

        return {
            "transcript": transcript["text"],
            "detected_language": transcript.get("language"),
            "duration": transcript.get("duration"),
            **result
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tts")
async def generate_tts(request: TextRequest):
    try:
        audio_bytes, content_type = await text_to_speech(
            text=request.text,
            language=request.language or "hi"
        )

        from fastapi.responses import Response

        return Response(
            content=audio_bytes,
            media_type=content_type,
            headers={
                "Content-Disposition": "inline; filename=vaani_response.mp3"
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )