import ast
from Analyzer.Rules.SQL_injection_rule import SQLInjectionRule
from Analyzer.Rules.eval_rule import EvalRule
from Analyzer.Rules.command_rule import CommandInjectionRule
from Analyzer.Reporting import templates as tmp
from Analyzer.Reporting.issue import Issue
RULES = [SQLInjectionRule, EvalRule, CommandInjectionRule]


def make_issue(rule_id, line, snippet=""):
    t = tmp.TEMPLATES[rule_id]

    return Issue(
        line=line,
        rule_id=rule_id,
        code_snippet=snippet,
        severity=t.get("severity", "LOW"),
        confidence=t.get("confidence", "HIGH"),
        title=t["title"],
        explanation=t["explanation"],
        danger=t["danger"],
        fix=t["fix"],
        example_payload=t.get("example_payload"),
        example_fix=t.get("example_fix"),
    )

class FunctionCollector(ast.NodeVisitor):
    def __init__(self):
        self.functions = {}
        self.current_function = None

    def visit_FunctionDef(self, node):
        # register function
        self.functions[node.name] = node

        # track which function we are inside
        previous = self.current_function
        self.current_function = node

        # visit body
        self.generic_visit(node)

        # restore previous function context
        self.current_function = previous

    def visit_Return(self, node):
        # attach parent function reference
        node._parent_function = self.current_function
        self.generic_visit(node)




class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.rules = [rule(self) for rule in RULES]
        self.tainted = set()
        self.functions = {}
        self.current_function = None
        self.tainted_returns = set()
        self.learning_returns = False
        self.import_aliases = {}
        self.reported_findings = set()

    def contains_source(self, node):
        if isinstance(node, ast.Call):
            if getattr(node.func, "id", None) == "input":
                return True

        for child in ast.iter_child_nodes(node):
            if self.contains_source(child):
                return True

        return False

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


    # Handle return statements
    def visit_Return(self, node):
        if self.learning_returns and node.value and self.expr_is_tainted(node.value):
            if self.current_function:
                self.tainted_returns.add(self.current_function)

        self.generic_visit(node)

    # Handle import statements, obviously this is not every possible alias but it's all we need for now
    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == "subprocess":
                self.import_aliases[alias.asname or alias.name] = "subprocess"
            if alias.name == "os":
                self.import_aliases[alias.asname or alias.name] = "os"

        self.generic_visit(node)

    # Handle from import statements, obviously this is not every possible alias but it's all we need for now
    def visit_ImportFrom(self, node):
        if node.module == "subprocess":
            for alias in node.names:
                self.import_aliases[alias.asname or alias.name] = "subprocess"

        if node.module == "os":
            for alias in node.names:
                self.import_aliases[alias.asname or alias.name] = "os"

        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        previous = self.current_function
        self.current_function = node.name

        self.generic_visit(node)

        self.current_function = previous

    #Handle Assignments
    def visit_Assign(self, node):
        value_tainted = self.expr_is_tainted(node.value)

        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
            if node.value.func.id in self.tainted_returns:
                value_tainted = True

        for target in node.targets:
            if isinstance(target, ast.Name):
                if value_tainted:
                    self.tainted.add(target.id)
                else:
                    self.tainted.discard(target.id)

    # Handle function calls
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id

            if func_name in self.functions:
                func_def = self.functions[func_name]

                original_taint = self.tainted.copy()

                for arg, param in zip(node.args, func_def.args.args):
                    if self.expr_is_tainted(arg):
                        self.tainted.add(param.arg)

                for stmt in func_def.body:
                    self.visit(stmt)

                self.tainted = original_taint
                return

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, None)
        if visitor:
            visitor(node)

        # rule execution
        if not self.learning_returns:
            for rule in self.rules:
                rule_method = getattr(rule, f"visit_{type(node).__name__}", None)
                if rule_method:
                    rule_method(node)
        super().generic_visit(node)

    def results(self):
        issues = []
        for rule in self.rules:
            issues.extend(rule.issues)
        return issues


def analyze(code: str):
    # Filter out non-code inputs/non-python inputs
    if code.count("\n") < 1 and not any(x in code for x in ["(", "=", "def ", "import "]):
        return [make_issue("IMPROPER_INPUT", 0, code)]

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [make_issue("SYNTAX_ERROR", e.lineno, code)]

    collector = FunctionCollector()
    collector.visit(tree)

    analyzer = Analyzer()
    analyzer.functions = collector.functions

    changed = True
    while changed:
        before = set(analyzer.tainted_returns)

        analyzer.learning_returns = True

        for func in collector.functions.values():

            original_taint = analyzer.tainted.copy()
            for param in func.args.args:
                analyzer.tainted.add(param.arg)

            analyzer.visit(func)

            analyzer.tainted = original_taint

        analyzer.learning_returns = False
        changed = before != analyzer.tainted_returns

    # print("TAINTED RETURNS LEARNED:", analyzer.tainted_returns)

    analyzer.source_lines = code.splitlines()
    analyzer.visit(tree)

    return analyzer.results()

