import csv
from typing import List, Tuple

def read_csv_header(path: str) -> List[str]:
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            return [c.strip() for c in row]
    return []

def detect_schema_drift(csv_path: str, expected_columns: List[str]) -> Tuple[List[str], List[str]]:
    header = read_csv_header(csv_path)
    new_cols = [c for c in header if c not in expected_columns]
    missing_cols = [c for c in expected_columns if c not in header]
    return new_cols, missing_cols
