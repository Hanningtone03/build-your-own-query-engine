import sys
import json
from .parser import parse
from .planner import plan
from .executor import execute

def print_table(rows):
    if not rows:
        print("No results.")
        return
    headers = list(rows[0].keys())
    widths = {h: max(len(h), max(len(str(r.get(h, ""))) for r in rows)) for h in headers}
    header_line = " | ".join(h.ljust(widths[h]) for h in headers)
    print(header_line)
    print("-" * len(header_line))
    for row in rows:
        print(" | ".join(str(row.get(h, "")).ljust(widths[h]) for h in headers))

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.cli \"SELECT * FROM data/file.csv\"")
        return
    query = " ".join(sys.argv[1:])
    try:
        ast = parse(query)
        steps = plan(ast)
        results = execute(steps)
        print_table(results)
        print(f"\n{len(results)} row(s)")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()