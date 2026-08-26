import re
from app.schemas.delivery import DeliveryAssessmentSchema
from app.schemas.content_review import ContentReviewSchema, SlideFeedback


def heuristic_delivery(text: str, filler_count: int) -> DeliveryAssessmentSchema:
    words = text.split()
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    avg_sentence = len(words) / max(len(sentences), 1)
    hedges = len(re.findall(r"\b(maybe|perhaps|might|could|i think|i believe|possibly)\b", text.lower()))
    confidence = max(45, min(95, 82 - hedges * 5 - min(filler_count, 10) * 2))
    clarity = max(45, min(95, 84 - max(0, avg_sentence - 24) * 1.5))
    engagement = max(45, min(92, 58 + min(len(re.findall(r"\?", text)) * 5, 15) + min(len(re.findall(r"\b(you|we|imagine|why|how)\b", text.lower())) * 2, 15)))
    return DeliveryAssessmentSchema(
        confidence_score=round(confidence), clarity_score=round(clarity), engagement_score=round(engagement), grammar_issues=[],
        overall_feedback="Deterministic fallback: add an LLM provider key for advanced transcript-specific coaching."
    )


def heuristic_content(slides: list[dict]) -> ContentReviewSchema:
    substantive = [s for s in slides if s.get("text", "").strip()]
    if not substantive:
        return ContentReviewSchema(structure_score=0, clarity_score=0, claim_support_score=0, flow_score=0,
                                    overall_content_feedback="No extractable slide text was available, so content quality cannot be reliably assessed.")
    avg_len = sum(len(s["text"].split()) for s in substantive) / len(substantive)
    structure = 72 if len(substantive) >= 3 else 58
    clarity = min(90, round(55 + min(avg_len, 30)))
    support = min(88, round(48 + min(avg_len / 2, 35)))
    flow = 68 if len(substantive) > 1 else 55
    feedback = [SlideFeedback(slide_number=s["slide_number"], takeaway="", supporting_detail="",
                              feedback="LLM slide-specific review unavailable; configure GROQ_API_KEY for advanced feedback.") for s in substantive]
    return ContentReviewSchema(structure_score=structure, clarity_score=clarity, claim_support_score=support, flow_score=flow,
                                slide_feedback=feedback,
                                overall_content_feedback="The deck was parsed successfully. Configure GROQ_API_KEY to enable evidence-grounded slide-by-slide coaching.")
