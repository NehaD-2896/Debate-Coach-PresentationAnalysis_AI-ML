from __future__ import annotations
from typing import Any
from .schemas import PerformanceScoreRequest

RUBRIC = (
    ("Argument Quality", 0.30),
    ("Evidence Usage", 0.20),
    ("Logical Consistency", 0.20),
    ("Rebuttal Effectiveness", 0.15),
    ("Communication Skills", 0.15),
)


def clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, float(value)))


def number(data: dict[str, Any] | None, *keys: str) -> float | None:
    if not isinstance(data, dict):
        return None
    for key in keys:
        value = data.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return clamp(value)
    return None


def number_any(data: dict[str, Any] | None, *paths: tuple[str, ...]) -> float | None:
    for path in paths:
        cur: Any = data
        for key in path:
            if not isinstance(cur, dict):
                cur = None
                break
            cur = cur.get(key)
        if isinstance(cur, (int, float)) and not isinstance(cur, bool):
            return clamp(cur)
    return None


def scale_0_10(value: float | None) -> float | None:
    return None if value is None else clamp(value * 10)


def component(name: str, score: float, weight: float, source: str) -> dict[str, Any]:
    score = round(clamp(score), 2)
    return {
        "name": name,
        "score": score,
        "weight": weight,
        "contribution": round(score * weight, 2),
        "source": source,
        "available": True,
    }


def argument_quality(req: PerformanceScoreRequest) -> tuple[float | None, str]:
    a, d = req.argument_analysis, req.debate_evaluation
    # Reference mapping: (clarity + relevance) / 2.
    clarity = number(a, "clarity_score")
    relevance = number(a, "relevance_score")
    if clarity is not None and relevance is not None:
        return (clarity + relevance) / 2, "argument_analysis.clarity_score+relevance_score"
    values = [v for v in (clarity, relevance, number(a, "strength_score", "argument_strength_score")) if v is not None]
    if values:
        return sum(values) / len(values), "argument_analysis.available_argument_signals"
    logic = number(d, "logic")
    return (scale_0_10(logic), "debate_evaluation.logic") if logic is not None and logic <= 10 else (None, "missing")


def evidence(req: PerformanceScoreRequest) -> tuple[float | None, str]:
    v = number(req.argument_analysis, "evidence_strength_score", "evidence_score")
    if v is not None:
        return v, "argument_analysis.evidence_strength_score"
    v = number(req.debate_evaluation, "evidence")
    return (scale_0_10(v), "debate_evaluation.evidence") if v is not None and v <= 10 else ((v, "debate_evaluation.evidence") if v is not None else (None, "missing"))


def logic(req: PerformanceScoreRequest) -> tuple[float | None, str]:
    v = number(req.argument_analysis, "logical_consistency_score", "logic_score")
    if v is not None:
        return v, "argument_analysis.logical_consistency_score"
    v = number(req.debate_evaluation, "logic")
    return (scale_0_10(v), "debate_evaluation.logic") if v is not None and v <= 10 else ((v, "debate_evaluation.logic") if v is not None else (None, "missing"))


def rebuttal(req: PerformanceScoreRequest) -> tuple[float | None, str]:
    # A generated counterargument is NOT evidence of learner rebuttal skill.
    v = number(req.debate_evaluation, "rebuttal_quality", "rebuttal_effectiveness_score")
    if v is not None:
        return (scale_0_10(v), "debate_evaluation.rebuttal_quality") if v <= 10 else (v, "debate_evaluation.rebuttal_quality")
    # Reference Milestone-3 UI used persuasiveness as the rebuttal proxy when no evaluator score exists.
    v = number(req.argument_analysis, "persuasiveness_score")
    if v is not None:
        return v, "argument_analysis.persuasiveness_score_proxy"
    return None, "missing"


def communication(req: PerformanceScoreRequest) -> tuple[float | None, str]:
    d = req.presentation_analysis or {}
    delivery = d.get("delivery_metrics") or d.get("delivery") or {}
    values = [number(delivery, "clarity_score"), number(delivery, "confidence_score"), number(delivery, "engagement_score")]
    values = [v for v in values if v is not None]
    if values:
        return sum(values) / len(values), "presentation_analysis.delivery_metrics"
    return None, "missing"


def presentation_score(req: PerformanceScoreRequest) -> float | None:
    p = req.presentation_analysis
    if not isinstance(p, dict):
        return None
    explicit = number(p, "presentation_score")
    if explicit is not None:
        return explicit
    delivery = p.get("delivery_metrics") or p.get("delivery") or {}
    content = p.get("content_review") or {}
    metrics = p.get("presentation_metrics") or {}
    values = [
        number(delivery, "confidence_score"), number(delivery, "clarity_score"), number(delivery, "engagement_score"),
        number(content, "structure_score"), number(content, "clarity_score"), number(content, "claim_support_score"), number(content, "flow_score"),
    ]
    values = [v for v in values if v is not None]
    if values:
        return sum(values) / len(values)
    wpm = number(metrics, "words_per_minute")
    return None if wpm is None else None


def critical_thinking(req: PerformanceScoreRequest) -> float | None:
    logic_score, _ = logic(req)
    if logic_score is None:
        return None
    penalty = 0.0
    f = req.fallacy_analysis
    if isinstance(f, dict):
        if isinstance(f.get("fallacies_found"), list):
            penalty = min(25.0, 5.0 * len(f["fallacies_found"]))
        elif f.get("fallacy_detected") is True:
            confidence = number(f, "confidence", "confidence_score") or 60
            penalty = min(25.0, 0.25 * confidence)
    return clamp(logic_score - penalty)


def score_request(req: PerformanceScoreRequest) -> dict[str, Any]:
    resolvers = [
        ("Argument Quality", 0.30, argument_quality),
        ("Evidence Usage", 0.20, evidence),
        ("Logical Consistency", 0.20, logic),
        ("Rebuttal Effectiveness", 0.15, rebuttal),
        ("Communication Skills", 0.15, communication),
    ]
    components: list[dict[str, Any]] = []
    missing: list[str] = []
    for name, weight, resolver in resolvers:
        value, source = resolver(req)
        if value is None:
            missing.append(name)
        else:
            components.append(component(name, value, weight, source))

    available_weight = sum(c["weight"] for c in components)
    overall = None
    if components and available_weight > 0:
        overall = sum(c["score"] * c["weight"] for c in components) / available_weight

    presentation = presentation_score(req)
    critical = critical_thinking(req)
    comm, _ = communication(req)

    strengths = [f"{c['name']} ({c['score']:.0f}/100)" for c in components if c["score"] >= 80]
    improvements = [f"Improve {c['name']} ({c['score']:.0f}/100)" for c in components if c["score"] < 60]
    notes = [
        "Scores are derived from supplied upstream engine outputs; no random/default performance values are generated.",
        "The official reference rubric is 30% Argument Quality, 20% Evidence Usage, 20% Logical Consistency, 15% Rebuttal Effectiveness, 15% Communication Skills.",
    ]
    if missing:
        notes.append("Unavailable rubric inputs: " + ", ".join(missing) + ".")
    if available_weight < 1:
        notes.append(f"Available rubric weight: {available_weight:.0%}; overall score is normalized across available evidence only.")
    if req.counterargument_analysis is not None and rebuttal(req)[1] != "counterargument_analysis":
        notes.append("Generated counterarguments are not counted as learner rebuttal performance.")

    completeness = available_weight
    return {
        "session_id": req.session_id,
        "overall_performance_score": round(overall, 2) if overall is not None else None,
        "debate_performance_score": round(overall, 2) if overall is not None else None,
        "presentation_score": round(presentation, 2) if presentation is not None else None,
        "critical_thinking_score": round(critical, 2) if critical is not None else None,
        "communication_effectiveness_score": round(comm, 2) if comm is not None else None,
        "debate_components": components,
        "presentation_components": presentation_components(req.presentation_analysis),
        "data_completeness": round(completeness, 3),
        "strengths": strengths[:5],
        "improvement_areas": improvements[:5],
        "notes": notes,
        "feedback": None,
        "score_scale": "0-100",
        "scoring_version": "2.0",
    }


def presentation_components(presentation: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(presentation, dict):
        return []
    delivery = presentation.get("delivery_metrics") or presentation.get("delivery") or {}
    content = presentation.get("content_review") or {}
    fields = [
        ("Confidence", number(delivery, "confidence_score"), "presentation_analysis.delivery_metrics"),
        ("Clarity", number(delivery, "clarity_score"), "presentation_analysis.delivery_metrics"),
        ("Engagement", number(delivery, "engagement_score"), "presentation_analysis.delivery_metrics"),
        ("Structure", number(content, "structure_score"), "presentation_analysis.content_review"),
        ("Content Clarity", number(content, "clarity_score"), "presentation_analysis.content_review"),
        ("Claim Support", number(content, "claim_support_score"), "presentation_analysis.content_review"),
        ("Flow", number(content, "flow_score"), "presentation_analysis.content_review"),
    ]
    present = [(n, v, s) for n, v, s in fields if v is not None]
    weight = 1 / len(present) if present else 1
    return [component(n, v, weight, s) for n, v, s in present]
