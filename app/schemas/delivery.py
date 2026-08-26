from pydantic import BaseModel, Field


class GrammarIssue(BaseModel):
    original_text: str
    corrected_text: str
    explanation: str


class DeliveryAssessmentSchema(BaseModel):
    grammar_issues: list[GrammarIssue] = Field(default_factory=list)
    confidence_score: int = Field(ge=0, le=100)
    clarity_score: int = Field(ge=0, le=100)
    engagement_score: int = Field(ge=0, le=100)
    overall_feedback: str
