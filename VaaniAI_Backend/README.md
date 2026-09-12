# VaaniAI Backend

FastAPI backend for the SIH VaaniAI project using xAI/Grok.

## Features

- Text question → Grok
- Voice/audio → xAI Speech-to-Text
- Child-friendly explanation
- Translation/adaptation to target language
- Text-to-Speech using xAI Voice API
- CORS for frontend integration

## 1. Create environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

## 2. Install packages

```powershell
pip install -r requirements.txt
```

## 3. Configure API key

Copy:

```text
.env.example
```

to:

```text
.env
```

Then put your xAI key in:

```text
XAI_API_KEY=your_real_key
```

Never put the API key inside frontend JavaScript.

## 4. Start backend

```powershell
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Swagger API testing:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

### GET /
Health/basic status.

### GET /health
Backend health check.

### POST /api/process
Send JSON:

```json
{
  "text": "What is photosynthesis?",
  "source_language": "English",
  "target_language": "Hindi"
}
```

### POST /api/voice
Upload an audio file and provide:

```text
target_language=Hindi
```

The backend:
audio → xAI STT → Grok → JSON answer

### POST /api/tts
Send:

```json
{
  "text": "पौधे सूर्य की रोशनी से अपना भोजन बनाते हैं।",
  "language": "hi"
}
```

It returns audio.

## Important

The xAI API uses Bearer authentication and the API base is `https://api.x.ai`.
Keep XAI_API_KEY only on the backend.
