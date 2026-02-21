from base import BaseRule
import ast


class SQLInjectionRule(BaseRule):
    id = "SQLI"
    description = "SQL Injection"
    severity = "HIGH"

    def visit_JoinedStr(self, node):
        self.report(
            node,
            "SQL query built using f-string interpolation",
            "Use parameterized query"
        )

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "execute" and len(node.args) == 1:
                self.report(
                    node,
                    "Query executed without parameters",
                    "Use execute(query, params)"
                )