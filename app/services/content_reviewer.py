from app.llm_client import LLMClient
from app.schemas.content_review import ContentReviewSchema
from .heuristics import heuristic_content

SYSTEM = """You are a presentation content reviewer. Judge only the actual extracted slide/page text: structure, clarity, claim support and flow. Do not evaluate speaking style. Do not invent visual content that was not extracted. Give slide feedback only for substantive slides."""


async def review_content(slides: list[dict]) -> ContentReviewSchema:
    fallback = heuristic_content(slides)
    if not any(s.get("text", "").strip() for s in slides):
        return fallback
    text = "\n\n".join(f"--- Slide/Page {s['slide_number']} ---\n{s.get('text') or '(no extractable text)'}" for s in slides)
    result = await LLMClient().structured(SYSTEM, text, ContentReviewSchema)
    return result or fallback
