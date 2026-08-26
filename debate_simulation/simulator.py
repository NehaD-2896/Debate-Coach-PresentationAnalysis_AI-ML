from typing import Any, Dict, List

class DebateSimulator:
    """Module 3: generates a structured counterargument/rebuttal stage."""

    name = "Debate Simulation"

    def generate(
        self,
        argument: str,
        argument_analysis: Dict[str, Any] | None = None,
        fallacy_audit: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        if not argument or not argument.strip():
            raise ValueError("argument must not be empty")

        return {
            "counterarguments": [
                "Challenge the strongest assumption in the argument.",
                "Ask for evidence supporting the main claim.",
                "Present the strongest reasonable opposing position."
            ],
            "rebuttal_strategy": (
                "Address the strongest counterargument first, support the claim "
                "with evidence, and close with a concise conclusion."
            ),
        }
