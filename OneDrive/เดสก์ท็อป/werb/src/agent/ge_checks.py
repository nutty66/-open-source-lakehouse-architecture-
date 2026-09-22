import csv
from typing import Dict, Any, List, Tuple

def sample_rows(path: str, max_rows: int = 10) -> List[Dict[str, str]]:
    rows = []
    with open(path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, r in enumerate(reader):
            if i >= max_rows:
                break
            rows.append(r)
    return rows


def check_required_columns(rows: List[Dict[str, str]], expected: Dict[str, Any]) -> Tuple[bool, str]:
    expected_cols = expected.get('columns', [])
    if not rows:
        return False, 'No sample rows'
    present = set(rows[0].keys())
    missing = [c for c in expected_cols if c not in present]
    if missing:
        return False, f'Missing required columns: {missing}'
    return True, 'Required columns present'


def check_types(rows: List[Dict[str, str]], expected: Dict[str, Any]) -> Tuple[bool, str]:
    # expected may include optional `types` map
    types = expected.get('types', {})
    if not types:
        return True, 'No type expectations'
    for r in rows:
        for col, t in types.items():
            v = r.get(col, '')
            if v == '' or v is None:
                continue
            if t == 'number':
                try:
                    float(v)
                except Exception:
                    return False, f'Column {col} expected number but got {v}'
            # extend with other types if needed
    return True, 'Types OK'


def run_all_checks(sample_csv: str, expected: Dict[str, Any]) -> Tuple[bool, List[str]]:
    rows = sample_rows(sample_csv, max_rows=20)
    ok, msg = check_required_columns(rows, expected)
    results = [msg]
    if not ok:
        return False, results
    ok2, msg2 = check_types(rows, expected)
    results.append(msg2)
    return ok2, results
