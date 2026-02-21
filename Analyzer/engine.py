import ast
from Analyzer.Rules.SQL_injection_rule import SQLInjectionRule
from Analyzer.Rules.eval_rule import EvalRule
from Analyzer.Rules.command_rule import CommandInjectionRule

RULES = [SQLInjectionRule, EvalRule, CommandInjectionRule]


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.rules = [rule(self) for rule in RULES]
        self.tainted = set()

    def expr_is_tainted(self, node):

        if isinstance(node, ast.Name):
            return node.id in self.tainted

        # string concatenation
        if isinstance(node, ast.BinOp):
            return self.expr_is_tainted(node.left) or self.expr_is_tainted(node.right)

        # function calls
        if isinstance(node, ast.Call):
            if getattr(node.func, "id", None) == "input":
                return True

            # propagation: func(tainted)
            for arg in node.args:
                if self.expr_is_tainted(arg):
                    return True

            # methods like .strip() .lower() .replace()
            if isinstance(node.func, ast.Attribute):
                return self.expr_is_tainted(node.func.value)

        # f-strings
        if isinstance(node, ast.JoinedStr):
            for value in node.values:
                if isinstance(value, ast.FormattedValue):
                    if self.expr_is_tainted(value.value):
                        return True

        return False

    def visit(self, node):

        if isinstance(node, ast.Assign):
            value_tainted = self.expr_is_tainted(node.value)

            for target in node.targets:
                if isinstance(target, ast.Name):
                    if value_tainted:
                        self.tainted.add(target.id)
                    elif target.id in self.tainted:
                        self.tainted.remove(target.id)

        for rule in self.rules:
            method = getattr(rule, f"visit_{type(node).__name__}", None)
            if method:
                method(node)

        self.generic_visit(node)

    def results(self):
        issues = []
        for rule in self.rules:
            issues.extend(rule.issues)
        return issues


def analyze(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [{
            "line": e.lineno,
            "rule": "SYNTAX",
            "severity": "ERROR",
            "message": str(e),
            "suggestion": "Fix syntax"
        }]

    analyzer = Analyzer()
    analyzer.source_lines = code.splitlines()
    analyzer.visit(tree)
    return analyzer.results()