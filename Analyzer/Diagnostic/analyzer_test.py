import sys
from Analyzer.engine import analyze

def print_results(results):
    for issue in results:
        print(f"\nLine {issue.line} — {issue.title}")
        if issue.code_snippet:
            print("Code:", issue.code_snippet.strip())

        print(f"Severity: {issue.severity} | Confidence: {issue.confidence}")

        print("Why:", issue.explanation)
        print("Risk:", issue.danger)
        print("Fix:", issue.fix)

        if issue.example_payload:
            print("Example attack:", issue.example_payload)

        if issue.example_fix:
            print("Safer code:", issue.example_fix)



def run_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    results = analyze(code)
    print_results(results)


def interactive_mode():
    print("Paste Python code. Type END on a new line to analyze.\n")

    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    code = "\n".join(lines)
    results = analyze(code)
    print_results(results)


if __name__ == "__main__":
    # Usage:
    # python test_scanner.py file example.py
    # python test_scanner.py paste

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python test_scanner.py file <filename>")
        print("  python test_scanner.py paste")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "file":
        run_from_file(sys.argv[2])

    elif mode == "paste":
        interactive_mode()

    else:
        print("Unknown mode")