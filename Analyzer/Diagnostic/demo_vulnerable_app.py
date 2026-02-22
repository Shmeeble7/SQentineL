import os
import sqlite3
import subprocess
import ast

# Fake database setup
def get_user_by_name(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # SQL Injection (concatenation)
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    cursor.execute(query)

    return cursor.fetchall()


def get_user_by_email(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # SQL Injection (f-string)
    query = f"SELECT * FROM users WHERE email = '{email}'"
    cursor.execute(query)

    return cursor.fetchall()


def safe_lookup(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchall()

# Command Execution Features
def ping_host(host):
    # Command Injection (os.system)
    os.system("ping " + host)


def list_directory(path):
    # Command Injection (subprocess + shell=True)
    subprocess.run(f"dir {path}", shell=True)


def safe_list_directory(path):
    subprocess.run(["dir", path])


# Dynamic Code Execution
def run_user_expression(expr):
    # Direct eval of user input
    return eval(expr)


def build_and_execute(value):
    # Eval with f-string
    code = f"print({value})"
    eval(code)


def concat_exec(value):
    # Exec with concatenation
    command = "print(" + value + ")"
    exec(command)


def indirect_eval(data):
    # Tainted return flow
    return data


def execute_indirect(payload):
    code = indirect_eval(payload)
    eval(code)


def safe_literal_parse(data):
    return ast.literal_eval(data)


# Simulated App Flow
def main():

    username = input("Username: ")
    email = input("Email: ")
    host = input("Host to ping: ")
    path = input("Directory to list: ")
    expression = input("Math expression to run: ")

    print("\n--- Database Queries ---")
    get_user_by_name(username)
    get_user_by_email(email)
    safe_lookup(1)

    print("\n--- System Commands ---")
    ping_host(host)
    list_directory(path)
    safe_list_directory(path)

    print("\n--- Dynamic Execution ---")
    run_user_expression(expression)
    build_and_execute(expression)
    concat_exec(expression)
    execute_indirect(expression)
    safe_literal_parse("[1, 2, 3]")


if __name__ == "__main__":
    main()