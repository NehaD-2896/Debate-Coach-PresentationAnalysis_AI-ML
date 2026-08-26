from __future__ import annotations
import json
from typing import Any
from .config import get_settings


SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "performance_coaching",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "strengths": {"type": "array", "items": {"type": "string"}},
                "improvement_areas": {"type": "array", "items": {"type": "string"}},
                "next_steps": {"type": "array", "items": {"type": "string"}},
                "evidence": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["summary", "strengths", "improvement_areas", "next_steps", "evidence"],
            "additionalProperties": False,
        },
    },
}


def _compact(payload: Any, limit: int = 14000) -> str:
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return text[:limit]


def generate_feedback(result: dict[str, Any], req: Any) -> dict[str, Any] | None:
    settings = get_settings()
    if not settings.groq_api_key:
        return None

    from groq import Groq
    client = Groq(api_key=settings.groq_api_key)
    source = {
        "topic": req.topic,
        "stance": req.stance,
        "transcript": req.transcript,
        "score_result": {
            "overall_performance_score": result.get("overall_performance_score"),
            "debate_components": result.get("debate_components"),
            "presentation_score": result.get("presentation_score"),
            "critical_thinking_score": result.get("critical_thinking_score"),
            "communication_effectiveness_score": result.get("communication_effectiveness_score"),
            "data_completeness": result.get("data_completeness"),
            "notes": result.get("notes"),
        },
        "upstream_outputs": {
            "argument_analysis": req.argument_analysis,
            "fallacy_analysis": req.fallacy_analysis,
            "debate_evaluation": req.debate_evaluation,
            "presentation_analysis": req.presentation_analysis,
        },
    }
    system = (
        "You are the final performance coach in an AI Debate Coach platform. "
        "Use ONLY the supplied learner evidence and calculated scores. Never invent a score, quote, event, or weakness. "
        "Do not recalculate or override the deterministic rubric. Explain what the evidence means and give actionable coaching. "
        "If evidence is missing, explicitly say it is unavailable. Keep the response concise and specific."
    )
    user = "Return structured coaching for this exact scored session:\n" + _compact(source)
    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        response_format=SCHEMA,
        temperature=0.2,
        max_completion_tokens=1200,
    )
    content = response.choices[0].message.content or "{}"
    return {"provider": "groq", "model": settings.groq_model, **json.loads(content)}
