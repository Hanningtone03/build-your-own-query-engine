import csv
import json
import os

def scan(source):
    if not os.path.exists(source):
        raise FileNotFoundError(f"File not found: {source}")

    if source.endswith(".csv"):
        with open(source, "r") as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]

    if source.endswith(".json"):
        with open(source, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return [data]

    raise ValueError(f"Unsupported file type: {source}")