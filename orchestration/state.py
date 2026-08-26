from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class DebateState:
    argument: str
    outputs: Dict[str, Any] = field(default_factory=dict)
