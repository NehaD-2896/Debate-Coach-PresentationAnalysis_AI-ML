from typing import Optional
from pydantic import BaseModel, Field


class PresentationMetricsSchema(BaseModel):
    words_per_minute: Optional[int] = Field(default=None, ge=0)
    pace_status: str
    filler_word_count: int = Field(default=0, ge=0)
    filler_words: dict[str, int] = Field(default_factory=dict)
    duration_seconds: Optional[float] = None
    word_count: int = Field(default=0, ge=0)
