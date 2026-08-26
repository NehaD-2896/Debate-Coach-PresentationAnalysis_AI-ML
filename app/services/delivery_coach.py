from app.llm_client import LLMClient
from app.schemas.delivery import DeliveryAssessmentSchema
from .heuristics import heuristic_delivery

SYSTEM = """You are a supportive presentation delivery coach. Judge HOW the speaker communicates, not the truth of the argument. Return structured scores from 0-100 for confidence, clarity and audience engagement. Identify only real grammar issues. Be constructive. Use the supplied filler count as evidence, but do not invent audio characteristics that are not present in the transcript."""


async def analyze_delivery(text: str, filler_count: int = 0) -> DeliveryAssessmentSchema:
    fallback = heuristic_delivery(text, filler_count)
    result = await LLMClient().structured(SYSTEM, f"Filler word count: {filler_count}\n\nTranscript:\n{text}", DeliveryAssessmentSchema)
    return result or fallback
