import os
import subprocess

# ==============================================================
# Once again, this is only for testing. Do not run this unless
# are a certified goober head
# ==============================================================

# Constant command
os.system("uptime")


# Proper subprocess argument list
filename = input("File to read: ")
subprocess.run(["cat", filename])


# Proper argument list with variable
directory = input("Directory: ")
subprocess.Popen(["ls", directory])


# shell=True but no user input
subprocess.run("ls -la", shell=True)


# Sanitized input example
user = input("Username: ")
if user.isalnum():
    subprocess.run(["id", user])


# Safe helper function
def show_file(name):
    subprocess.run(["cat", name])


data = input("Another file: ")
show_file(data)
