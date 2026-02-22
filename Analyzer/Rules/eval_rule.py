from Analyzer.Rules.base import BaseRule
import ast


class EvalRule(BaseRule):

    id = "EVAL"
    description = "Arbitrary Code Execution"
    severity = "CRITICAL"

    SINKS = {"eval", "exec", "compile"}

    def visit_Call(self, node):

        # Only direct name calls (eval(), exec(), compile())
        if not isinstance(node.func, ast.Name):
            return

        if node.func.id not in self.SINKS:
            return

        if not node.args:
            return

        payload = node.args[0]

        # Only continue if tainted data reaches sink
        if not self.analyzer.expr_is_tainted(payload):
            return

        # f-string injection
        if isinstance(payload, ast.JoinedStr):
            self.report(node, "EVAL_FSTRING",
                        evidence="fstring with tainted data passed to dynamic execution")
            return

        # string concatenation
        if isinstance(payload, ast.BinOp):
            self.report(node, "EVAL_CONCAT",
                        evidence="string concatenation with tainted data")
            return

        # direct variable
        if isinstance(payload, ast.Name):
            self.report(node, "EVAL_TAINT",
                        evidence="tainted variable passed to dynamic execution")
            return

        # tainted return from function
        if isinstance(payload, ast.Call):
            self.report(node, "EVAL_RETURN",
                        evidence="tainted return value passed to dynamic execution")
            return

        # fallback
        self.report(node, "EVAL_GENERIC",
                    evidence="tainted data reaches dynamic execution")