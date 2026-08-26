from app.schemas.ai_review import AIReviewSchema


def test_advanced_review_schema_supports_slide_grounding():
    obj = AIReviewSchema(
        confidence_score=80, clarity_score=81, engagement_score=79,
        delivery_feedback="Good delivery.",
        structure_score=82, content_clarity_score=84, claim_support_score=77, flow_score=80,
        overall_content_feedback="The deck has a clear sequence.",
        slide_feedback=[{
            "slide_number": 1,
            "takeaway": "The system solves noisy light-curve detection.",
            "supporting_detail": "The slide names BLS/TLS and false-positive filtering.",
            "feedback": "State the takeaway before the tool names.",
            "presentation_alignment": "The transcript explains the same problem.",
        }],
    )
    assert obj.slide_feedback[0].slide_number == 1
