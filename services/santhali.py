import os
import requests
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


def translate_hindi_to_santhali(text: str) -> str:

    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing in .env")

    prompt = f"""
Translate the following Hindi educational text into Santhali.

Hindi text:
{text}

Requirements:
- Translate the meaning accurately.
- Keep it suitable for primary school students.
- Do not explain the text.
- Do not summarize it.
- Return ONLY the Santhali translation.
"""

    response = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a careful Hindi to Santhali "
                        "educational translation assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,
            "max_completion_tokens": 500
        },
        timeout=60
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Santhali translation error "
            f"{response.status_code}: {response.text}"
        )

    data = response.json()

    content = data["choices"][0]["message"]["content"].strip()

    if content.startswith("```"):
        content = (
            content
            .replace("```text", "")
            .replace("```", "")
            .strip()
        )

    return content