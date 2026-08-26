from orchestration.debate_workflow import build_real_workflow


class FakeRealArgumentAgent:
    def run(self, text):
        return {
            "claim": text,
            "evidence": ["study"],
            "strength_label": "strong",
            "strength_score": 80,
            "clarity_score": 90,
            "logical_consistency_score": 88,
        }


class FakeRealFallacyAgent:
    def run(self, text):
        return {"fallacies_found": []}


class FakeRealAIEngine:
    def generate_simulation_response(self, text, persona):
        return {
            "opponent_rebuttal": "Challenge the main premise.",
            "fallacies_detected": [],
            "rebuttal_strength_percent": 75,
            "coaching_tip": "Address the strongest counterargument.",
        }

    def calculate_weighted_score(
        self, arg_quality, evidence, logic, rebuttal, comms
    ):
        return round(
            0.30 * arg_quality
            + 0.20 * evidence
            + 0.20 * logic
            + 0.15 * rebuttal
            + 0.15 * comms,
            1,
        )


def test_real_components_are_wired_end_to_end():
    workflow = build_real_workflow(
        FakeRealArgumentAgent(),
        FakeRealFallacyAgent(),
        FakeRealAIEngine(),
    )

    result = workflow.run(
        "AI should support teachers rather than replace them."
    )

    modules = result["modules"]
    assert list(modules) == [
        "argument_analysis",
        "fallacy_detection",
        "rebuttal",
        "coaching",
    ]
    assert modules["argument_analysis"]["strength_score"] == 80
    assert modules["fallacy_detection"]["fallacies_found"] == []
    assert modules["rebuttal"]["rebuttal_strength_percent"] == 75
    assert modules["coaching"]["overall_score"] > 0
