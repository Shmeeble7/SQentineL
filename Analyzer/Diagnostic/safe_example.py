import sqlite3

# =========================================================
# This is meant to be used purely for testing the analyzer.
# Please do not be a dingus and actually use it.
# ==========================================================

conn = sqlite3.connect("test.db")
cursor = conn.cursor()


# parameterized query
username = input("Username: ")
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))


# multiple parameters
email = input("Email: ")
password = input("Password: ")
cursor.execute(
    "SELECT * FROM users WHERE email = ? AND password = ?",
    (email, password)
)


# insert
name = input("Name: ")
age = input("Age: ")
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))


# LIKE
search = input("Search: ")
cursor.execute("SELECT * FROM products WHERE name LIKE ?", ("%" + search + "%",))


# integer conversion
user_id = int(input("ID: "))
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))


# whitelist ORDER BY
order = input("Sort (name/date): ")
if order not in ["name", "date"]:
    order = "name"

query = f"SELECT * FROM logs ORDER BY {order}"
cursor.execute(query)


# constant query
cursor.execute("SELECT COUNT(*) FROM users")


# prepared statement
def get_user():
    return input("User: ")

u = get_user()
cursor.execute("SELECT * FROM users WHERE username = ?", (u,))