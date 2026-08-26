from pydantic import BaseModel, Field
from .presentation import PresentationMetricsSchema
from .delivery import DeliveryAssessmentSchema
from .content_review import ContentReviewSchema


class PresentationAnalysisResponse(BaseModel):
    transcript: str
    filename: str
    slide_count: int
    presentation_metrics: PresentationMetricsSchema
    delivery_metrics: DeliveryAssessmentSchema
    content_review: ContentReviewSchema
    analysis_mode: str = "advanced-llm"
    llm_provider: str | None = None
    llm_model: str | None = None
