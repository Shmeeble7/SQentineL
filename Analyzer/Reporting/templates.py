TEMPLATES = {

    "SQLI_TAINT": {
        "title": "User input reaches SQL query",
        "explanation":
            "Data from the user flows directly into a database query.",

        "danger":
            "An attacker can modify the query logic and access or delete data.",

        "fix":
            "Use parameterized queries instead of string building.",

        "example_payload": "' OR 1=1 --",
        "example_fix":
            'cursor.execute("SELECT * FROM users WHERE name = ?", (username,))'
    },


    "SQLI_CONCAT": {
        "title": "SQL query built using string concatenation",
        "explanation":
            "Building SQL queries with + allows untrusted data to alter the query.",

        "danger":
            "Attackers may inject conditions or bypass authentication.",

        "fix":
            "Replace concatenation with query parameters.",

        "example_payload": "' OR '1'='1",
        "example_fix": 'cursor.execute("SELECT * FROM users WHERE name = ?", (username,))'
    },


    "SQLI_FSTRING": {
        "title": "SQL query built using f-string",
        "explanation": "Python f-strings insert variables directly into SQL text.",
        "danger": "If the variable contains SQL, it becomes part of the command.",
        "fix": "Use placeholders (?) and pass variables separately.",
        "example_payload": "'; DROP TABLE users; --",
        "example_fix": 'cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))'
    },

    "CMDI_OS": {
        "title": "User input executed as system command",
        "explanation": "User-controlled data is passed directly into a system shell command.",
        "danger": "An attacker can execute arbitrary commands on the server.",
        "fix": "Avoid os.system/popen. Use subprocess.run with argument list.",
        "example_payload": "filename=; rm -rf /",
        "example_fix": "subprocess.run(['cat', filename])"
    },

    "CMDI_SUBPROCESS": {
        "title": "Shell command constructed from user input",
        "explanation": "The program builds a shell command using user input while shell=True is enabled.",
        "danger": "Attackers can inject additional shell commands.",
        "fix": "Remove shell=True and pass arguments as a list.",
        "example_payload": "host=8.8.8.8; cat /etc/passwd",
        "example_fix": "subprocess.run(['ping','-c','1',host])"
    },

    "SQLI_RETURN": {
        "title": "User input returned from function reaches SQL query",
        "explanation": "Tainted data returned from a function is used in a SQL query.",
        "danger": "Attackers can inject arbitrary SQL by controlling returned values.",
        "fix": "Validate or parameterize returned data before database execution.",
        "severity": "HIGH",
        "confidence": "HIGH",
    },

    "IMPROPER_INPUT":  {
        "title": "Improper input",
        "explanation": "The text you entered was not a valid form of input",
        "danger": "You can't learn anything :(",
        "fix": "SQentineL can only handle python code currently",
        "severity": "LOW",
        "confidence": "HIGH",
    },

    "SYNTAX_ERROR":  {
        "title": "Improper syntax",
        "explanation": "Your input contains a syntax error",
        "danger": "SQentineL cannot analyze that code",
        "fix": "Fix your program syntax before passing in the code",
        "severity": "LOW",
        "confidence": "HIGH",
    },

    "EVAL_TAINT": {
        "title": "User input executed as Python code",
        "explanation":
            "User-controlled data is passed directly into a dynamic execution function such as eval or exec.",

        "danger":
            "This is reliably exploitable remote code execution.",

        "fix":
            "Avoid using eval/exec on user input. Use safer alternatives like literal parsing or explicit logic.",

        "severity": "Critical",
        "confidence": "High",

        "example_payload": "__import__('os').system('whoami')",
        "example_fix":
            "Use ast.literal_eval() for safe expression parsing."
    },


    "EVAL_CONCAT": {
        "title": "Dynamic code built using string concatenation",
        "explanation":
            "Python code is constructed using + with untrusted data before being executed.",

        "danger":
            "Attackers can inject arbitrary Python statements into the constructed code.",

        "fix":
            "Do not build executable code using string concatenation. Refactor to avoid dynamic execution.",

        "severity": "HIGH",
        "confidence": "MEDIUM",

        "example_payload": "1); __import__('os').system('ls') #",
        "example_fix":
            "Replace dynamic execution with direct function calls or safe parsing."
    },


    "EVAL_FSTRING": {
        "title": "Dynamic code built using f-string",
        "explanation":
            "Python f-strings insert variables directly into executable code text.",

        "danger":
            "If the variable contains malicious Python, it becomes part of the executed code.",

        "fix":
            "Avoid f-strings for executable code. Use controlled logic instead of dynamic execution.",

        "severity": "HIGH",
        "confidence": "MEDIUM",

        "example_payload": "__import__('os').system('cat /etc/passwd')",
        "example_fix":
            "Remove eval/exec and handle user input safely without execution."
    },


    "EVAL_RETURN": {
        "title": "Tainted return value executed as Python code",
        "explanation":
            "User input flows through a function and is later executed dynamically.",

        "danger":
            "Even indirect user input can lead to full remote code execution.",

        "fix":
            "Validate or sanitize returned values before use, and avoid dynamic execution functions.",

        "severity": "HIGH",
        "confidence": "HIGH",

        "example_payload": "__import__('subprocess').getoutput('whoami')",
        "example_fix":
            "Ensure functions return validated data and remove eval/exec usage."
    },


    "EVAL_GENERIC": {
        "title": "Tainted data reaches dynamic execution",
        "explanation":
            "Untrusted data is used in a dynamic execution context.",

        "danger":
            "This can result in arbitrary code execution and full system compromise.",

        "fix":
            "Remove dynamic execution of untrusted input and redesign the logic safely.",

        "severity": "MEDIUM",
        "confidence": "LOW",


    },
}
