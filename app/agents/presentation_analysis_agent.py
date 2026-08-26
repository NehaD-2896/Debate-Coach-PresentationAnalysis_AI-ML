from .base_agent import BaseAgent
from app.schemas.presentation_full import PresentationAnalysisResponse
from app.schemas.delivery import DeliveryAssessmentSchema
from app.schemas.content_review import ContentReviewSchema
from app.services.presentation_audio import compute_presentation_metrics
from app.services.heuristics import heuristic_delivery, heuristic_content
from app.services.advanced_reviewer import advanced_review
from app.llm_client import LLMClient


class PresentationAnalysisAgent(BaseAgent):
    name = "Presentation Analysis Agent"

    async def run(self, transcript: str, filename: str, slides: list[dict], duration_seconds: float | None = None) -> PresentationAnalysisResponse:
        metrics = compute_presentation_metrics(transcript, duration_seconds)
        llm = LLMClient()
        review = await advanced_review(slides, transcript, metrics.filler_word_count)

        if review is None:
            delivery = heuristic_delivery(transcript, metrics.filler_word_count)
            content = heuristic_content(slides)
            mode = "deterministic-fallback"
            provider = None
            model = None
        else:
            delivery = DeliveryAssessmentSchema(
                grammar_issues=review.grammar_issues,
                confidence_score=review.confidence_score,
                clarity_score=review.clarity_score,
                engagement_score=review.engagement_score,
                overall_feedback=review.delivery_feedback,
            )
            content = ContentReviewSchema(
                structure_score=review.structure_score,
                clarity_score=review.content_clarity_score,
                claim_support_score=review.claim_support_score,
                flow_score=review.flow_score,
                slide_feedback=review.slide_feedback,
                overall_content_feedback=review.overall_content_feedback,
                strengths=review.content_strengths,
                improvement_actions=review.content_improvements,
            )
            mode = "advanced-llm"
            provider = llm.primary_provider
            model = llm.primary_model

        return PresentationAnalysisResponse(
            transcript=transcript,
            filename=filename,
            slide_count=len(slides),
            presentation_metrics=metrics,
            delivery_metrics=delivery,
            content_review=content,
            analysis_mode=mode,
            llm_provider=provider,
            llm_model=model,
        )
