import ast
from Analyzer.Reporting.issue import Issue
from Analyzer.Reporting.templates import TEMPLATES
class BaseRule:
    id = "BASE"
    description = "Base rule"
    severity = "INFO"

    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.issues = []

    def report(self, node, template_key, evidence=None):
        template = TEMPLATES[template_key]

        severity, confidence = self.score(template_key, evidence)

        issue = Issue(
            line=node.lineno,
            rule_id=self.id,
            severity=severity,
            confidence=confidence,
            title=template["title"],
            explanation=template["explanation"],
            danger=template["danger"],
            fix=template["fix"],
            example_payload=template.get("example_payload"),
            example_fix=template.get("example_fix"),
        )

        self.issues.append(issue)

    def score(self, template_key, evidence):
        if template_key == "SQLI_TAINT":
            return "HIGH", "HIGH"

        if template_key == "SQLI_FSTRING":
            return "HIGH", "MEDIUM"

        if template_key == "SQLI_CONCAT":
            return "MEDIUM", "MEDIUM"

        return "LOW", "LOW"

    def visit_Call(self, node): pass
    def visit_Assign(self, node): pass
    def visit_BinOp(self, node): pass
    def visit_JoinedStr(self, node): pass