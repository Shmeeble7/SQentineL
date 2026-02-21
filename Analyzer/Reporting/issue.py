from dataclasses import dataclass
from typing import Optional


@dataclass
class Issue:
    line: int
    rule_id: str
    severity: str
    confidence: str

    title: str
    explanation: str
    danger: str
    fix: str

    example_payload: Optional[str] = None
    example_fix: Optional[str] = None