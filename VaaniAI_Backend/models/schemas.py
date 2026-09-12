from typing import Optional
from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str
    source_language: str = "auto"
    target_language: str = "Hindi"
    language: Optional[str] = "hi"

class ProcessResponse(BaseModel):
    answer: str
    translation: str
    simple_explanation: str
    example: str
