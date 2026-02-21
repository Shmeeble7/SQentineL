import os
import subprocess

# ==============================================================
# Once again, this is only for testing. Do not run this unless
# are a certified goober head
# ==============================================================


# Direct concatenation into os.system
filename = input("File to read: ")
os.system("cat " + filename)


# f-string into shell=True subprocess
host = input("Host to ping: ")
subprocess.run(f"ping -c 1 {host}", shell=True)


# Variable propagation
user = input("Directory: ")
cmd = "ls " + user
subprocess.Popen(cmd, shell=True)


# Passed through helper function
def show_file(name):
    os.system("cat " + name)

data = input("Another file: ")
show_file(data)


# popen usage
target = input("Check process: ")
os.popen("ps aux | grep " + target)


# call() with shell=True
query = input("Search logs: ")
subprocess.call(f"grep {query} /var/log/syslog", shell=True)