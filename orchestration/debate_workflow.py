from typing import Any, Dict, Sequence


class DebateWorkflow:
    """Sequential integration of the project's existing AI components."""

    def __init__(self, modules: Sequence[Any]):
        if len(modules) != 4:
            raise ValueError("DebateWorkflow requires exactly 4 modules.")
        self.modules = list(modules)

    @staticmethod
    def _call(module: Any, argument: str, context: Dict[str, Any]) -> Any:
        for method_name in ("run", "analyze", "generate", "coach"):
            method = getattr(module, method_name, None)
            if callable(method):
                return method(argument, **context)

        if callable(module):
            return module(argument, **context)

        raise TypeError(
            f"Module {module!r} must expose run/analyze/generate/coach "
            "or be callable."
        )

    def run(self, argument: str) -> Dict[str, Any]:
        if not argument or not argument.strip():
            raise ValueError("argument must not be empty")

        context: Dict[str, Any] = {}
        results: Dict[str, Any] = {}

        for index, module in enumerate(self.modules, start=1):
            output = self._call(module, argument, context)
            key = getattr(module, "output_key", f"module_{index}")
            results[key] = output
            context[key] = output

        return {
            "input": argument,
            "modules": results,
        }


def build_real_workflow(
    argument_agent,
    fallacy_agent,
    ai_engine,
    persona="The Contrarian",
):
    """Build a workflow from the project's real components."""
    from .adapters import (
        ArgumentAnalysisAdapter,
        FallacyDetectionAdapter,
        RebuttalAdapter,
        CoachingScoringAdapter,
    )

    return DebateWorkflow([
        ArgumentAnalysisAdapter(argument_agent),
        FallacyDetectionAdapter(fallacy_agent),
        RebuttalAdapter(ai_engine, persona),
        CoachingScoringAdapter(ai_engine),
    ])
