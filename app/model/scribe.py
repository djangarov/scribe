from pydantic import BaseModel


class OCRResult(BaseModel):
    text: str
    average_confidence: float
    word_count: int
