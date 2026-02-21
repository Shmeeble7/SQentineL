from Analyzer.Rules.base import BaseRule
import ast


class SQLInjectionRule(BaseRule):

    id = "SQLI"
    description = "SQL Injection"
    severity = "HIGH"

    def visit_Call(self, node):
        if getattr(node.func, "attr", "") != "execute":
            return

        if not node.args:
            return

        query = node.args[0]

        # If no tainted data reaches execute, stop immediately
        if not self.analyzer.expr_is_tainted(query):
            return

        # --- Classification only happens AFTER taint confirmed ---

        # direct f-string
        if isinstance(query, ast.JoinedStr):
            self.report(node, "SQLI_FSTRING", evidence="fstring contains tainted data")
            return

        # string concatenation
        if isinstance(query, ast.BinOp):
            self.report(node, "SQLI_CONCAT", evidence="string concatenation with tainted data")
            return

        # variable passed
        if isinstance(query, ast.Name):
            self.report(node, "SQLI_TAINT", evidence="tainted variable reaches execute")
            return

        # fallback (covers function returns, builders, complex expressions)
        self.report(node, "SQLI_RETURN", evidence="returned tainted value")


