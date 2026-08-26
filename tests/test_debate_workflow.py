from orchestration.debate_workflow import DebateWorkflow

class ArgumentAnalysisAgent:
    output_key = "argument_analysis"
    def run(self, argument, **context):
        return {"claim": argument, "strength_score": 82}

class FallacyDetectionAgent:
    output_key = "fallacy_detection"
    def run(self, argument, **context):
        assert "argument_analysis" in context
        return {"fallacies_found": []}

class RebuttalAgent:
    output_key = "rebuttal"
    def run(self, argument, **context):
        assert "fallacy_detection" in context
        return {"counterargument": "Provide evidence for the claim."}

class CoachAgent:
    output_key = "coaching"
    def run(self, argument, **context):
        assert "rebuttal" in context
        return {"score": 82, "feedback": "Address the strongest counterargument."}

def test_four_module_chain():
    workflow = DebateWorkflow([
        ArgumentAnalysisAgent(),
        FallacyDetectionAgent(),
        RebuttalAgent(),
        CoachAgent(),
    ])

    result = workflow.run(
        "AI should support teachers rather than replace them."
    )

    assert list(result["modules"]) == [
        "argument_analysis",
        "fallacy_detection",
        "rebuttal",
        "coaching",
    ]
    assert result["modules"]["argument_analysis"]["strength_score"] == 82
    assert result["modules"]["fallacy_detection"]["fallacies_found"] == []
    assert "counterargument" in result["modules"]["rebuttal"]
    assert result["modules"]["coaching"]["score"] == 82
