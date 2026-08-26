from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class DebateState:
    argument: str
    argument_analysis: Dict[str, Any] = field(default_factory=dict)
    fallacy_audit: Dict[str, Any] = field(default_factory=dict)
    simulation: Dict[str, Any] = field(default_factory=dict)
    coaching: Dict[str, Any] = field(default_factory=dict)
