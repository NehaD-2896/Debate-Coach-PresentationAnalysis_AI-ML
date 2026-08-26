from typing import Any, Dict

class DebateCoach:
    """Module 4: converts the pipeline outputs into coaching feedback."""

    name = "Debate Coach"

    def coach(
        self,
        argument: str,
        argument_analysis: Dict[str, Any] | None = None,
        fallacy_audit: Dict[str, Any] | None = None,
        simulation: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        analysis = argument_analysis or {}

        scores = [
            analysis.get("strength_score"),
            analysis.get("clarity_score"),
            analysis.get("relevance_score"),
            analysis.get("persuasiveness_score"),
        ]
        numeric = [float(x) for x in scores if isinstance(x, (int, float))]
        overall = round(sum(numeric) / len(numeric), 1) if numeric else 75.0

        return {
            "overall_score": overall,
            "strengths": [
                "The argument has a clear position.",
                "The response can be strengthened with specific evidence."
            ],
            "improvements": [
                "Address the strongest opposing argument.",
                "Use concrete evidence or examples.",
                "Finish with a concise conclusion."
            ],
            "coaching": (
                "Challenge the premise directly while keeping the response tied "
                "to evidence and the strongest counterargument."
            ),
        }
