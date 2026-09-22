import json
import os
from datetime import datetime

def ensure_dirs():
    os.makedirs('prs', exist_ok=True)
    os.makedirs('staging', exist_ok=True)

def create_pr_suggestion(expected_schema_path, new_cols, csv_sample_path) -> str:
    ensure_dirs()
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    branch = f'agent-schema-fix/{ts}'
    pr_path = os.path.join('prs', f'pr_{ts}.md')
    with open(expected_schema_path, encoding='utf-8') as f:
        expected = json.load(f)

    content = {
        'branch': branch,
        'change': 'add_nullable_columns',
        'new_columns': new_cols,
        'rationale': 'Detected new columns in incoming CSV; propose adding as nullable to staging and mapping',
    }

    with open(pr_path, 'w', encoding='utf-8') as f:
        f.write('# PR Suggestion\n')
        f.write('Branch: ' + branch + '\n\n')
        f.write('Proposed change JSON:\n')
        json.dump(content, f, indent=2, ensure_ascii=False)
        f.write('\n\n')
        f.write('Sample file: ' + csv_sample_path + '\n')

    return pr_path

def apply_staging_change(expected_schema_path, new_cols):
    ensure_dirs()
    with open(expected_schema_path, encoding='utf-8') as f:
        expected = json.load(f)
    # backup existing staging file if present
    staging_file = os.path.join('staging', 'expected_schema.json')
    backup_path = None
    if os.path.exists(staging_file):
        ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        backup_path = os.path.join('staging', f'expected_schema_backup_{ts}.json')
        with open(staging_file, 'r', encoding='utf-8') as sf, open(backup_path, 'w', encoding='utf-8') as bf:
            bf.write(sf.read())

    # apply non-destructive additions
    for c in new_cols:
        if c not in expected['columns']:
            expected['columns'].append(c)
    with open(staging_file, 'w', encoding='utf-8') as f:
        json.dump(expected, f, indent=2, ensure_ascii=False)
    return staging_file, backup_path


def rollback_staging(backup_path):
    staging_file = os.path.join('staging', 'expected_schema.json')
    if backup_path and os.path.exists(backup_path):
        with open(backup_path, 'r', encoding='utf-8') as bf, open(staging_file, 'w', encoding='utf-8') as sf:
            sf.write(bf.read())
        return True
    return False
