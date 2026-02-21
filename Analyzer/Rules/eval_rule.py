from Analyzer.Rules.base import BaseRule
import ast


class EvalRule(BaseRule):
    def __init__(self, analyzer):
        super().__init__(analyzer)

    id = "EVAL"
    description = "Arbitrary Code Execution"
    severity = "CRITICAL"

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in ["eval", "exec"]:
                self.report(
                    node,
                    "Use of eval/exec with possible user input",
                    "Avoid dynamic code execution"
                )