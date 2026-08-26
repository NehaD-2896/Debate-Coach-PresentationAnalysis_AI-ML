from typing import Any, Dict

from .state import DebateState
from fallacy_detection.detector import FallacyDetector
from debate_simulation.simulator import DebateSimulator
from recommendation_engine.coach import DebateCoach

class DebateWorkflow:
    """Four-module AI/ML integration pipeline.

    The existing argument_analysis/analyzer.py is injected by the caller so
    this integration does not overwrite the team's existing Module 1.
    """

    def __init__(
        self,
        argument_analyzer: Any,
        fallacy_detector: Any | None = None,
        simulator: Any | None = None,
        coach: Any | None = None,
    ):
        self.argument_analyzer = argument_analyzer
        self.fallacy_detector = fallacy_detector or FallacyDetector()
        self.simulator = simulator or DebateSimulator()
        self.coach = coach or DebateCoach()

    @staticmethod
    def _run_argument_analyzer(analyzer: Any, argument: str) -> Dict[str, Any]:
        if hasattr(analyzer, "analyze"):
            result = analyzer.analyze(argument)
        elif callable(analyzer):
            result = analyzer(argument)
        else:
            raise TypeError("argument_analyzer must expose analyze() or be callable")

        return result if isinstance(result, dict) else {"result": result}

    def run(self, argument: str) -> Dict[str, Any]:
        if not argument or not argument.strip():
            raise ValueError("argument must not be empty")

        state = DebateState(argument=argument)

        # Module 1: existing repository argument_analysis module.
        state.argument_analysis = self._run_argument_analyzer(
            self.argument_analyzer, argument
        )

        # Module 2: fallacy detection.
        state.fallacy_audit = self.fallacy_detector.analyze(
            argument,
            argument_analysis=state.argument_analysis,
        )

        # Module 3: debate simulation / rebuttal.
        state.simulation = self.simulator.generate(
            argument,
            argument_analysis=state.argument_analysis,
            fallacy_audit=state.fallacy_audit,
        )

        # Module 4: recommendation / debate coaching.
        state.coaching = self.coach.coach(
            argument,
            argument_analysis=state.argument_analysis,
            fallacy_audit=state.fallacy_audit,
            simulation=state.simulation,
        )

        return {
            "argument_analysis": state.argument_analysis,
            "fallacy_audit": state.fallacy_audit,
            "simulation": state.simulation,
            "coaching": state.coaching,
        }
