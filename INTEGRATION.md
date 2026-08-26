# Integration Contract

## Presentation Analysis -> Performance Scoring

The Presentation Analysis Engine returns a JSON object with these key sections:

```json
{
  "transcript": "...",
  "filename": "presentation.pptx",
  "slide_count": 10,
  "presentation_metrics": {
    "words_per_minute": 126,
    "pace_status": "Optimal",
    "filler_word_count": 4
  },
  "delivery_metrics": {
    "confidence_score": 84,
    "clarity_score": 88,
    "engagement_score": 79,
    "grammar_issues": [],
    "overall_feedback": "..."
  },
  "content_review": {
    "structure_score": 82,
    "clarity_score": 86,
    "claim_support_score": 74,
    "flow_score": 81,
    "slide_feedback": [],
    "overall_content_feedback": "..."
  }
}
```

The Performance Scoring Engine can consume these values as the communication/presentation side of the overall evaluation. Do not recompute speech metrics in the scoring layer.

## Why the browser recorder is included
The supplied reference frontend demonstrates the intended user workflow: a learner uploads slides, records through `navigator.mediaDevices.getUserMedia()` and `MediaRecorder`, automatically calculates duration, and posts the resulting audio with the presentation to the analysis endpoint. This module follows that pattern while keeping the backend independently integrable.
