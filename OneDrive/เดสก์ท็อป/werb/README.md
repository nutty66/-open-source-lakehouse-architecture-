Self-Healing Agent POC

Run a minimal Python proof-of-concept that detects schema drift (new column in CSV), diagnoses, and creates a PR suggestion (mock).

Usage:

```bash
python src/agent/main.py --mode suggest-pr --input samples/input_with_new_col.csv
```

Modes:
- `alert`: only detect and log
- `suggest-pr`: create PR suggestion file under `prs/`
- `auto-staging`: apply non-destructive change to `staging/expected_schema.json`
