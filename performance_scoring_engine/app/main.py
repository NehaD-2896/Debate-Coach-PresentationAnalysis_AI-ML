from fastapi import FastAPI, HTTPException
from .config import get_settings
from .groq_feedback import generate_feedback
from .schemas import PerformanceScoreRequest, PerformanceScoreResponse
from .scoring import score_request

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "engine": "performance_scoring_engine",
        "version": settings.app_version,
        "groq_configured": bool(settings.groq_api_key),
        "scoring": "deterministic-reference-rubric",
    }


@app.post("/api/v1/performance/score", response_model=PerformanceScoreResponse)
def score_performance(body: PerformanceScoreRequest):
    result = score_request(body)
    try:
        ai_feedback = generate_feedback(result, body)
        if ai_feedback:
            result["feedback"] = ai_feedback
        else:
            result["feedback"] = {
                "provider": "deterministic",
                "model": None,
                "summary": "Deterministic scoring completed. Configure GROQ_API_KEY to add AI coaching synthesis.",
                "strengths": result["strengths"],
                "improvement_areas": result["improvement_areas"],
                "next_steps": result["improvement_areas"][:3],
                "evidence": result["notes"],
            }
    except Exception as exc:
        # Scoring remains usable even if the external LLM is unavailable.
        result["notes"].append(f"Groq coaching unavailable: {type(exc).__name__}.")
        result["feedback"] = {
            "provider": "deterministic",
            "model": None,
            "summary": "Deterministic scoring completed; AI coaching was unavailable for this request.",
            "strengths": result["strengths"],
            "improvement_areas": result["improvement_areas"],
            "next_steps": result["improvement_areas"][:3],
            "evidence": result["notes"],
        }
    return result
