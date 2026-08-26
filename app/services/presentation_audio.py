import math
import re
from collections import Counter
from typing import Optional
from app.schemas.presentation import PresentationMetricsSchema

FILLER_WORDS = ("um", "uh", "uhh", "like", "you know", "actually", "basically", "literally")


def compute_presentation_metrics(transcript: str, duration_sec: Optional[float] = None) -> PresentationMetricsSchema:
    lowered = transcript.lower()
    counts = {
        word: len(re.findall(rf"\b{re.escape(word)}\b", lowered))
        for word in FILLER_WORDS
    }
    counts = {k: v for k, v in counts.items() if v}
    filler_count = sum(counts.values())
    words = transcript.split()
    word_count = len(words)

    if not duration_sec or duration_sec <= 0:
        return PresentationMetricsSchema(
            words_per_minute=None,
            pace_status="N/A (no duration)",
            filler_word_count=filler_count,
            filler_words=counts,
            duration_seconds=duration_sec,
            word_count=word_count,
        )

    wpm = math.ceil(word_count / (duration_sec / 60.0)) if word_count else 0
    if wpm > 160:
        pace = "Too Fast"
    elif wpm < 110:
        pace = "Too Slow"
    else:
        pace = "Optimal"
    return PresentationMetricsSchema(
        words_per_minute=wpm,
        pace_status=pace,
        filler_word_count=filler_count,
        filler_words=counts,
        duration_seconds=duration_sec,
        word_count=word_count,
    )
