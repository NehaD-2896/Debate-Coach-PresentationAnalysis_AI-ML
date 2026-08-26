# AI/ML Integration Only

This package contains only the orchestration layer and integration test.
It does not import, copy, or re-implement any agent.

Four existing modules are injected into `DebateWorkflow` in this order:

1. Argument Analysis
2. Fallacy Detection
3. Rebuttal / Debate Simulation
4. Coaching / Recommendation

Example:

```python
from orchestration.debate_workflow import DebateWorkflow

workflow = DebateWorkflow([
    argument_analysis_agent,
    fallacy_detection_agent,
    rebuttal_agent,
    coaching_agent,
])

result = workflow.run(user_argument)
```

Each later module receives the original argument plus the outputs of all
previous modules as keyword context.
