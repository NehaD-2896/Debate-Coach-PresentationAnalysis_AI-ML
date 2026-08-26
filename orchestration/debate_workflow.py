from typing import Any, Dict, Sequence

class DebateWorkflow:
    """Pure integration/orchestration layer.

    No agent/module is imported here. The team's existing four modules are
    injected into the workflow, so this file can live independently of
    their package names and locations.
    """

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
            f"Module {module!r} must expose run/analyze/generate/coach or be callable."
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

        return {"input": argument, "modules": results}
