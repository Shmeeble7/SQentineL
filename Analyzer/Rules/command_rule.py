from base import BaseRule
import ast


class CommandInjectionRule(BaseRule):
    id = "CMDI"
    description = "Command Injection"
    severity = "CRITICAL"

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ["system", "popen"]:
                self.report(
                    node,
                    "Possible command injection",
                    "Use subprocess with argument list and no shell=True"
                )
