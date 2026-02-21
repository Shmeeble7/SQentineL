from Analyzer.Rules.base import BaseRule
import ast


class CommandInjectionRule(BaseRule):

    id = "CMDI"
    description = "Command Injection"

    def _is_shell_true(self, node):
        for kw in node.keywords:
            if kw.arg == "shell" and isinstance(kw.value, ast.Constant):
                return kw.value.value is True
        return False

    def _is_tainted(self, node):
        return self.analyzer.expr_is_tainted(node)

    def _list_contains_shell(self, node):

        if not isinstance(node, (ast.List, ast.Tuple)):
            return False

        if len(node.elts) < 2:
            return False

        first = node.elts[0]
        second = node.elts[1]

        if not isinstance(first, ast.Constant):
            return False

        if first.value not in ("sh", "bash"):
            return False

        if not isinstance(second, ast.Constant) or second.value != "-c":
            return False

        if len(node.elts) >= 3:
            return self._is_tainted(node.elts[2])

        return False

    def command_arg_is_tainted(self, node):

        if not node.args:
            return False

        arg = node.args[0]

        # string command
        if isinstance(arg, (ast.Constant, ast.BinOp, ast.JoinedStr, ast.Call, ast.Name)):
            return self._is_tainted(arg)

        # list execution
        if isinstance(arg, (ast.List, ast.Tuple)):
            if self._list_contains_shell(arg):
                return True

        return False

    def visit_Call(self, node):

        if not isinstance(node.func, ast.Attribute):
            return

        attr = node.func.attr

        # ---- os.system / popen ----
        if isinstance(node.func.value, ast.Name):
            if node.func.value.id == "os":
                if attr in ("system", "popen"):
                    if self.command_arg_is_tainted(node):
                        self.report(node, "CMDI_OS")
                    return

        # ---- subprocess ----
        if isinstance(node.func.value, ast.Name):
            module = node.func.value.id

            if hasattr(self.analyzer, "import_aliases") and \
                    module in self.analyzer.import_aliases:
                if self.analyzer.import_aliases[module] == "subprocess":

                    if attr in ("run", "call", "Popen"):

                        if self._is_shell_true(node) and self.command_arg_is_tainted(node):
                            self.report(node, "CMDI_SUBPROCESS")