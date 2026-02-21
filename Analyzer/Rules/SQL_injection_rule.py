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

        # variable passed
        if isinstance(query, ast.Name):
            if query.id in self.analyzer.tainted:
                self.report(node, "SQLI_TAINT", evidence="tainted variable reaches execute")

        # direct f-string
        if isinstance(query, ast.JoinedStr):
            if self.analyzer.expr_is_tainted(query):
                self.report(node, "SQLI_FSTRING", evidence="fstring contains tainted data")

        # string concatenation
        if isinstance(query, ast.BinOp):
            if self.analyzer.expr_is_tainted(query):
                self.report(node, "SQLI_CONCAT", evidence="string concatenation with tainted data")

