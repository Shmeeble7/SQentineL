# Safe constant eval
eval("print(123)")

# Safe literal_eval usage
import ast
data = "[1, 2, 3]"
ast.literal_eval(data)

# Safe compile with constant
code = compile("print('hello')", "<string>", "exec")
exec(code)

# Sanitized user input example
value = "42"
eval(value)