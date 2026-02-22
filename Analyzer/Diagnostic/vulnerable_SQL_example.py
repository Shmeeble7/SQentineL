import sqlite3

# =========================================================
# This is meant to be used purely for testing the analyzer.
# Please do not be a dingus and actually use it.
# ==========================================================

conn = sqlite3.connect("test.db")
cursor = conn.cursor()


# string concatenation
username = input("Username: ")
query = "SELECT * FROM users WHERE username = '" + username + "'"
cursor.execute(query)


# f-string injection
password = input("Password: ")
cursor.execute(f"SELECT * FROM users WHERE password = '{password}'")


# percent formatting
user_id = input("ID: ")
cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)


# .format injection
email = input("Email: ")
sql = "SELECT * FROM users WHERE email = '{}'".format(email)
cursor.execute(sql)


# taint through variable assignment
search = input("Search: ")
base = "SELECT * FROM products WHERE name LIKE '%"
query = base + search + "%'"
cursor.execute(query)


# taint through function return
def get_user_input():
    return input("Category: ")


category = get_user_input()
cursor.execute("SELECT * FROM items WHERE category = '" + category + "'")


# multi-step taint
raw = input("Raw: ")
processed = raw.strip()
final_query = "SELECT * FROM data WHERE value = '" + processed + "'"
cursor.execute(final_query)


# execute many misuse
values = input("Values: ")
cursor.execute("INSERT INTO test VALUES (" + values + ")")


# DELETE injection
item = input("Item: ")
cursor.execute("DELETE FROM inventory WHERE name = '" + item + "'")


# ORDER BY injection
order = input("Order by: ")
cursor.execute("SELECT * FROM logs ORDER BY " + order)