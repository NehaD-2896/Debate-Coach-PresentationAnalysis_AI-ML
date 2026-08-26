from orchestration.debate_workflow import DebateWorkflow

class FakeArgumentAnalyzer:
    def analyze(self, argument):
        return {
            "claim": argument,
            "strength_score": 80,
            "clarity_score": 90,
            "relevance_score": 85,
            "persuasiveness_score": 82,
        }

def test_four_module_integration():
    result = DebateWorkflow(FakeArgumentAnalyzer()).run(
        "AI should support teachers rather than replace them."
    )

    assert set(result) == {
        "argument_analysis",
        "fallacy_audit",
        "simulation",
        "coaching",
    }
    assert result["argument_analysis"]["strength_score"] == 80
    assert "fallacies" in result["fallacy_audit"]
    assert "counterarguments" in result["simulation"]
    assert "overall_score" in result["coaching"]
