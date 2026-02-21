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
    },


    "SQLI_FSTRING": {
        "title": "SQL query built using f-string",
        "explanation":
            "Python f-strings insert variables directly into SQL text.",

        "danger":
            "If the variable contains SQL, it becomes part of the command.",

        "fix":
            "Use placeholders (?) and pass variables separately."
    }
}