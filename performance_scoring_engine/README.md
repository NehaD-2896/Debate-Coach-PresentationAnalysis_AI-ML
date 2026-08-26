# Milestone 5 — Performance Scoring Engine

A production-oriented, integration-ready performance scoring service for the Debate Coach platform.

## What makes this real

This engine **does not generate random/default performance numbers**. It calculates the score from actual outputs supplied by upstream engines:

- Argument Analysis Engine
- Fallacy Detection Engine
- Debate Evaluation / rebuttal evaluation
- Counterargument Engine (context only; generated counterarguments are not treated as learner performance)
- Presentation Analysis Engine

The deterministic score follows the reference project's official rubric:

| Criterion | Weight |
|---|---:|
| Argument Quality | 30% |
| Evidence Usage | 20% |
| Logical Consistency | 20% |
| Rebuttal Effectiveness | 15% |
| Communication Skills | 15% |

The service normalizes 0–10 evaluator values to 0–100 when necessary and never turns unavailable modules into zero. If only part of the rubric is available, it reports `data_completeness` and normalizes over the evidence that actually exists.

## Groq integration

Groq is used for the **qualitative coaching layer**, not to invent the numeric score. After deterministic scoring, the service can synchronously send the real session evidence and calculated results to Groq and return structured coaching:

- summary
- strengths
- improvement areas
- next steps
- evidence used

The implementation uses Groq Structured Outputs with `openai/gpt-oss-20b` by default. Set `GROQ_API_KEY` in `.env` to enable it.

If Groq is unavailable or not configured, the API still returns the deterministic score and explicitly marks the feedback provider as `deterministic`.

## API

### Health

`GET /health`

Returns engine status and whether Groq is configured.

### Score a real session

`POST /api/v1/performance/score`

Send the actual upstream JSON objects in their native shapes. See `examples/session.json`.

The response includes:

- `overall_performance_score`
- `debate_performance_score`
- `presentation_score`
- `critical_thinking_score`
- `communication_effectiveness_score`
- weighted component breakdown
- `data_completeness`
- strengths and improvement areas
- notes describing missing evidence
- structured Groq coaching when configured

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# put your GROQ_API_KEY in .env
python -m uvicorn app.main:app --reload --port 8011
```

Open:

`http://127.0.0.1:8011/docs`

## Verify Groq separately

After putting `GROQ_API_KEY` in `.env`, run:

```powershell
python scripts/check_groq.py
```

This makes a real live Groq request. It is separate from the deterministic scoring tests.

## Test

```powershell
python -m pytest -q
```

## Example curl

```powershell
curl -X POST "http://127.0.0.1:8011/api/v1/performance/score" `
  -H "accept: application/json" `
  -H "Content-Type: application/json" `
  --data-binary "@examples/session.json"
```

## Integration flow

```text
Browser / Debate Coach UI
        |
        v
Debate + Presentation session
        |
        +--> Argument Analysis Engine
        +--> Fallacy Detection Engine
        +--> Debate Evaluation / Rebuttal Engine
        +--> Presentation Analysis Engine
        |
        v
Performance Scoring Engine
        |
        +--> deterministic official rubric score
        |
        +--> Groq structured coaching (optional, real API call)
        |
        v
Combined performance result
```

The numeric score remains reproducible and auditable. Groq adds natural-language coaching grounded in the same evidence.
