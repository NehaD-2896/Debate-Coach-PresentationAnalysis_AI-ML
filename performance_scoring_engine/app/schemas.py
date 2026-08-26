from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel, Field, ConfigDict


class ScoreComponent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    score: float = Field(ge=0, le=100)
    weight: float = Field(ge=0, le=1)
    contribution: float = Field(ge=0, le=100)
    source: str
    available: bool = True


class Feedback(BaseModel):
    model_config = ConfigDict(extra="forbid")
    provider: Literal["groq", "deterministic"]
    model: str | None = None
    summary: str
    strengths: list[str] = Field(default_factory=list)
    improvement_areas: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)


class PerformanceScoreRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    # Native outputs from upstream teammate engines.
    argument_analysis: dict[str, Any] | None = None
    fallacy_analysis: dict[str, Any] | None = None
    counterargument_analysis: dict[str, Any] | None = None
    debate_evaluation: dict[str, Any] | None = None
    debate_transcript: list[dict[str, Any]] | None = None
    presentation_analysis: dict[str, Any] | None = None

    # Optional raw learner transcript for Groq coaching synthesis.
    transcript: str | None = None
    topic: str | None = None
    stance: str | None = None
    session_id: str | None = None


class PerformanceScoreResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    session_id: str | None = None
    overall_performance_score: float | None = None
    debate_performance_score: float | None = None
    presentation_score: float | None = None
    critical_thinking_score: float | None = None
    communication_effectiveness_score: float | None = None
    debate_components: list[ScoreComponent] = Field(default_factory=list)
    presentation_components: list[ScoreComponent] = Field(default_factory=list)
    data_completeness: float = Field(ge=0, le=1)
    strengths: list[str] = Field(default_factory=list)
    improvement_areas: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    feedback: Feedback | None = None
    score_scale: str = "0-100"
    scoring_version: str = "2.0"
