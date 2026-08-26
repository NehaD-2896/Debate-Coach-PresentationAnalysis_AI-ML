from pydantic import BaseModel, Field
from .delivery import GrammarIssue
from .content_review import SlideFeedback


class AIReviewSchema(BaseModel):
    confidence_score: int = Field(ge=0, le=100)
    clarity_score: int = Field(ge=0, le=100)
    engagement_score: int = Field(ge=0, le=100)
    grammar_issues: list[GrammarIssue] = Field(default_factory=list)
    delivery_feedback: str
    delivery_strengths: list[str] = Field(default_factory=list)
    delivery_improvements: list[str] = Field(default_factory=list)

    structure_score: int = Field(ge=0, le=100)
    content_clarity_score: int = Field(ge=0, le=100)
    claim_support_score: int = Field(ge=0, le=100)
    flow_score: int = Field(ge=0, le=100)
    overall_content_feedback: str
    content_strengths: list[str] = Field(default_factory=list)
    content_improvements: list[str] = Field(default_factory=list)
    slide_feedback: list[SlideFeedback] = Field(default_factory=list)
