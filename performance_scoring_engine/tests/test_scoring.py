from app.schemas import PerformanceScoreRequest
from app.scoring import score_request


def test_reference_rubric_matches_milestone_3_mapping():
    req = PerformanceScoreRequest(
        argument_analysis={
            "clarity_score": 80,
            "relevance_score": 90,
            "evidence_strength_score": 70,
            "logical_consistency_score": 85,
            "persuasiveness_score": 75,
        },
        presentation_analysis={
            "delivery_metrics": {"clarity_score": 80, "confidence_score": 90, "engagement_score": 70}
        },
    )
    result = score_request(req)
    expected = .30 * 85 + .20 * 70 + .20 * 85 + .15 * 75 + .15 * 80
    assert round(result["overall_performance_score"], 2) == round(expected, 2)


def test_missing_data_is_not_zeroed():
    req = PerformanceScoreRequest(argument_analysis={"clarity_score": 80, "relevance_score": 80})
    result = score_request(req)
    assert result["overall_performance_score"] == 80
    assert result["data_completeness"] == 0.30
    assert "Evidence Usage" in " ".join(result["notes"])


def test_debate_evaluator_ten_point_values_are_normalized():
    req = PerformanceScoreRequest(
        debate_evaluation={"logic": 8, "evidence": 7, "rebuttal_quality": 9},
        presentation_analysis={"delivery_metrics": {"clarity_score": 80, "confidence_score": 80, "engagement_score": 80}},
    )
    result = score_request(req)
    names = {x["name"]: x["score"] for x in result["debate_components"]}
    assert names["Logical Consistency"] == 80
    assert names["Evidence Usage"] == 70
    assert names["Rebuttal Effectiveness"] == 90


def test_counterargument_generation_is_not_learner_rebuttal():
    req = PerformanceScoreRequest(
        argument_analysis={"clarity_score": 80, "relevance_score": 80},
        counterargument_analysis={"rebuttals": [{"text": "generated rebuttal"}]},
    )
    result = score_request(req)
    assert "Rebuttal Effectiveness" in " ".join(result["notes"])
    assert all(x["name"] != "Rebuttal Effectiveness" for x in result["debate_components"])
