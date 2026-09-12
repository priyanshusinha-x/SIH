import os
import json
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


SYSTEM_PROMPT = """
You are VaaniAI, a multilingual educational assistant.

You must carefully separate TRANSLATION from EXPLANATION.

Return ONLY valid JSON with exactly these keys:
{
  "answer": "...",
  "translation": "...",
  "simple_explanation": "...",
  "example": "..."
}

Rules:

1. "answer":
   Answer the user's question correctly.

2. "translation":
   DIRECTLY TRANSLATE THE USER'S ORIGINAL INPUT TEXT into the requested target language.
   Do NOT explain, summarize, expand, or change the meaning.
   Preserve the meaning and intent of the original sentence.
   If the original input is a question, keep it as a question.
   The translation should be a natural and accurate translation.

3. "simple_explanation":
   Give a very simple, child-friendly explanation of the concept in the target language.

4. "example":
   Give one simple practical example in the target language.

Use simple language suitable for students.
Do not add unnecessary information to the translation.
"""


def grok_process(
    text: str,
    source_language: str = "auto",
    target_language: str = "Hindi"
) -> dict:

    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing in .env")

    user_prompt = f"""
Original user input:
{text}

Source language:
{source_language}

Target language:
{target_language}

IMPORTANT:

First understand the ORIGINAL USER INPUT.

The "translation" field MUST be a direct translation of:
"{text}"

Do NOT turn the translation into a definition or explanation.

For example:

Original:
"What is gravity?"

Hindi translation:
"गुरुत्वाकर्षण क्या है?"

The explanation can explain what gravity is, but the translation itself must remain a direct translation of the original question.
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
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "temperature": 0.2,
            "max_completion_tokens": 800
        },
        timeout=60
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Groq API error {response.status_code}: {response.text}"
        )

    data = response.json()

    content = data["choices"][0]["message"]["content"].strip()

    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(content)

        return {
            "answer": result.get("answer", ""),
            "translation": result.get("translation", ""),
            "simple_explanation": result.get("simple_explanation", ""),
            "example": result.get("example", "")
        }

    except json.JSONDecodeError:

        return {
            "answer": content,
            "translation": content,
            "simple_explanation": content,
            "example": ""
        }