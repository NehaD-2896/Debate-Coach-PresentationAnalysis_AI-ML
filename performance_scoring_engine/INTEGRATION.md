# Integration Contract

## Upstream payloads

The engine accepts these fields without forcing teammates to rewrite their existing response shapes:

- `argument_analysis`
- `fallacy_analysis`
- `counterargument_analysis`
- `debate_evaluation`
- `debate_transcript`
- `presentation_analysis`
- `transcript`
- `topic`
- `stance`
- `session_id`

## Reference mapping

Argument Quality:

`(argument_analysis.clarity_score + argument_analysis.relevance_score) / 2`

Evidence Usage:

`argument_analysis.evidence_strength_score`

Logical Consistency:

`argument_analysis.logical_consistency_score`

Rebuttal Effectiveness:

1. `debate_evaluation.rebuttal_quality` when present (0–10 or 0–100)
2. otherwise `argument_analysis.persuasiveness_score` as the same proxy used by the reference UI
3. otherwise unavailable

Communication Skills:

`average(presentation_analysis.delivery_metrics.clarity_score, confidence_score, engagement_score)`

## Why generated counterarguments are excluded

The counterargument service produces AI-generated rebuttals. Those are not the learner's performance. Counting them as learner skill would inflate the score and break evaluation integrity.

## Data integrity

- No random values.
- No synthetic zeros for missing modules.
- Missing evidence is reported.
- Numeric scoring is deterministic.
- AI feedback is generated only from supplied evidence.
- Groq failures do not destroy the deterministic score.
