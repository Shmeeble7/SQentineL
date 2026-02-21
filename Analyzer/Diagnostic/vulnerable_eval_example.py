# Direct eval
user_input = input("Enter code: ")
eval(user_input)


# f-string injection
x = input("Enter value: ")
code = f"print({x})"
eval(code)


# Concatenation injection
y = input("Enter expression: ")
cmd = "print(" + y + ")"
exec(cmd)


# Indirect via function return
def build_code(data):
    return data

z = input("Enter payload: ")
dangerous = build_code(z)
eval(dangerous)


# Compile usage
a = input("Enter code to compile: ")
compiled = compile(a, "<string>", "exec")
exec(compiled)