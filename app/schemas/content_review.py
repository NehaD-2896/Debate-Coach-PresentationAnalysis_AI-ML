from pydantic import BaseModel, Field


class SlideFeedback(BaseModel):
    slide_number: int
    takeaway: str = ""
    supporting_detail: str = ""
    feedback: str
    presentation_alignment: str = ""


class ContentReviewSchema(BaseModel):
    structure_score: int = Field(ge=0, le=100)
    clarity_score: int = Field(ge=0, le=100)
    claim_support_score: int = Field(ge=0, le=100)
    flow_score: int = Field(ge=0, le=100)
    slide_feedback: list[SlideFeedback] = Field(default_factory=list)
    overall_content_feedback: str
    strengths: list[str] = Field(default_factory=list)
    improvement_actions: list[str] = Field(default_factory=list)
