import asyncio
from app.agents.presentation_analysis_agent import PresentationAnalysisAgent


def test_agent_without_llm_keys():
    result = asyncio.run(PresentationAnalysisAgent().run(
        "Good morning everyone. Today we discuss artificial intelligence.",
        "demo.pptx",
        [{"slide_number": 1, "text": "Artificial Intelligence"}],
        10,
    ))
    assert result.slide_count == 1
    assert 0 <= result.delivery_metrics.confidence_score <= 100
    assert result.presentation_metrics.words_per_minute is not None
