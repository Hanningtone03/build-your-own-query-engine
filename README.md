![CI](https://github.com/Hanningtone03/build-your-own-query-engine/actions/workflows/ci.yml/badge.svg)

# Build Your Own Query Engine

A query engine in Python; run SQL-like queries directly over CSV and JSON files.

## How it works

A SQL string goes through a lexer, parser, and planner into an execution plan. The executor runs each step — scan, filter, project, sort, group, limit; over the file data. No database needed.

## Project structure

```
src/
├── cli.py
├── lexer.py
├── parser.py
├── planner.py
├── executor.py
└── scanner.py
```

## Running locally

```bash
python -m src.cli "SELECT * FROM data/file.csv"
```

## Supported SQL

| Feature | Example |
|---------|---------|
| Select all | `SELECT * FROM data/employees.csv` |
| Filter | `SELECT * FROM data/employees.csv WHERE department = 'Engineering'` |
| Sort | `SELECT * FROM data/employees.csv ORDER BY salary DESC` |
| Limit | `SELECT * FROM data/employees.csv LIMIT 3` |
| Group | `SELECT COUNT(id) FROM data/employees.csv GROUP BY department` |
| Distinct | `SELECT DISTINCT department FROM data/employees.csv` |

## Tech

- Python 3
- `csv`, `json`, `re` modules
- No external dependencies
