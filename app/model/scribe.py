from pydantic import BaseModel


class Result(BaseModel):
    text: str
    average_confidence: float
    word_count: int
