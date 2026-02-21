import ast
from Rules.SQL_injection_rule import SQLInjectionRule
from Rules.eval_rule import EvalRule
from Rules.command_rule import CommandInjectionRule

RULES = [SQLInjectionRule, EvalRule, CommandInjectionRule]


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.rules = [rule() for rule in RULES]

    def visit(self, node):
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
    analyzer.visit(tree)
    return analyzer.results()