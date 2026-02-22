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
        self.seen = set()

    def is_tainted(self, node):
        return self.analyzer.expr_is_tainted(node)

    def report(self, node, template_key, evidence=None):
        template = TEMPLATES[template_key]

        severity, confidence = self.score(template_key, evidence)
        source = self.analyzer.source_lines[node.lineno - 1]

        signature = (node.lineno, template_key, self.id)
        # prevent duplicate reports
        if signature in self.seen:
            return

        self.seen.add(signature)

        issue = Issue(
            line=node.lineno,
            rule_id=self.id,
            code_snippet=source,
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

        if template_key == "SQLI_RETURN":
            return "HIGH", "HIGH"

        if template_key == "CMDI_OS":
            return "CRITICAL", "HIGH"

        if template_key == "CMDI_SUBPROCESS":
            return "CRITICAL", "MEDIUM"

        if template_key == "EVAL_TAINT":
            return "CRITICAL", "HIGH"

        if template_key == "EVAL_CONCAT":
            return "HIGH", "MEDIUM"

        if template_key == "EVAL_FSTRING":
            return "HIGH", "MEDIUM"

        if template_key == "EVAL_FSTRING":
            return "HIGH", "HIGH"

        if template_key == "EVAL_GENERIC":
            return "MEDIUM", "LOW"

        return "UNCLASSIFIED", "UNCLASSIFIED"

    def visit_Call(self, node): pass
    def visit_Assign(self, node): pass
    def visit_BinOp(self, node): pass
    def visit_JoinedStr(self, node): pass