from dataclasses import dataclass
from typing import Optional


@dataclass
class Issue:
    line: int
    rule_id: str
    code_snippet: str
    severity: str
    confidence: str

    title: str
    explanation: str
    danger: str
    fix: str

    example_payload: Optional[str] = None
    example_fix: Optional[str] = None


def to_dict(self):
    return {
        "line": self.line,
        "rule_id": self.rule_id,
        "severity": self.severity,
        "confidence": self.confidence,
        "title": self.title,
        "explanation": self.explanation,
        "danger": self.danger,
        "fix": self.fix,
        "example_payload": self.example_payload,
        "example_fix": self.example_fix,
        "code_snippet": self.code_snippet,
    }