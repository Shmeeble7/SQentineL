import ast
class BaseRule:
    id = "BASE"
    description = "Base rule"
    severity = "INFO"

    def __init__(self):
        self.issues = []

    def report(self, node, message, suggestion=""):
        self.issues.append({
            "rule": self.id,
            "severity": self.severity,
            "line": getattr(node, "lineno", "?"),
            "message": message,
            "suggestion": suggestion
        })

    # Each rule can implement any of these
    def visit_Call(self, node): pass
    def visit_Assign(self, node): pass
    def visit_BinOp(self, node): pass
    def visit_JoinedStr(self, node): pass