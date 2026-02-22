import os
import ast
import shlex
import sqlite3
import subprocess


def get_user():
    return input("Enter value: ")

def get_number():
    return input("Enter number: ")


# EVAL INJECTION TESTS
def eval_vulnerable_direct():
    user = get_user()
    eval(user)  # Should trigger


def eval_vulnerable_concat():
    user = get_user()
    code = "print(" + user + ")"
    eval(code)  # Should trigger


def eval_sanitized_literal_eval():
    user = get_user()
    safe = ast.literal_eval(user)
    print(safe)  # Should not trigger


def eval_vulnerable_return_flow():
    user = get_user()
    processed = passthrough(user)
    eval(processed)  # should trigger


def eval_sanitized_after_literal():
    user = get_user()
    safe = ast.literal_eval(user)
    result = passthrough(safe)
    eval(result)  # Should not trigger


# SQL INJECTION TESTS

def sql_vulnerable_concat():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    username = get_user()
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    cursor.execute(query)  # should trigger


def sql_vulnerable_fstring():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    username = get_user()
    query = f"SELECT * FROM users WHERE name = '{username}'"
    cursor.execute(query)  # should trigger


def sql_safe_parameterized():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    username = get_user()
    cursor.execute(
        "SELECT * FROM users WHERE name = ?",
        (username,)
    )  # should not trigger


def sql_numeric_cast_sanitized():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    user_id = int(get_number())
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)  # Should not trigger if numeric cast removes taint


# COMMAND INJECTION TESTS

def cmd_vulnerable_os_system():
    filename = get_user()
    os.system("cat " + filename)  # should trigger


def cmd_vulnerable_subprocess_shell():
    host = get_user()
    subprocess.run("ping " + host, shell=True)  # should trigger


def cmd_safe_argument_list():
    filename = get_user()
    subprocess.run(["cat", filename])  # should not trigger


def cmd_safe_shlex_quote():
    filename = get_user()
    safe = shlex.quote(filename)
    os.system("cat " + safe)  # Should not trigger if sanitizer detected


# MIXED FLOW TESTS

def passthrough(value):
    return value


def double_passthrough():
    user = get_user()
    step1 = passthrough(user)
    step2 = passthrough(step1)
    eval(step2)  # should trigger


def sanitized_then_concatenated():
    user = get_user()
    safe = ast.literal_eval(user)
    code = "print(" + str(safe) + ")"
    eval(code)  # Should not trigger


# FALSE POSITIVE CHECKS

def hardcoded_eval():
    eval("print('hello')")


def hardcoded_sql():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")  # Should not trigger


def safe_string_manipulation():
    name = "admin"
    print("Hello " + name)  # Should not trigger


# EDGE CASES
def partial_sanitization():
    user = get_user()
    cleaned = user.strip()
    eval(cleaned)  # strip is NOT sanitizer


def reassignment_overwrite():
    user = get_user()
    user = "safe_value"
    eval(user)  # taint overwritten
