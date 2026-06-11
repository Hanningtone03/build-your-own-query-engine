# Build Your Own Query Engine

A query engine built from scratch in Python; execute SQL-like queries directly over CSV and JSON files.

## How it works

Query engines like DuckDB and Apache Drill execute queries over raw files without loading them into a database first. This project implements that pipeline from scratch:

- Tokenizes and parses SQL-like query strings
- Scans CSV and JSON files into row collections
- Builds a query execution plan from the parsed AST
- Executes filtering, projection, sorting, grouping and aggregation
- Prints results as a formatted table

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
| Aggregates | `SELECT COUNT(id) FROM data/employees.csv GROUP BY department` |
| Distinct | `SELECT DISTINCT department FROM data/employees.csv` |
| Aliases | `SELECT name AS employee FROM data/employees.csv` |

## Tech

- Python 3
- `csv`, `json`, `re` modules
- No external dependencies
