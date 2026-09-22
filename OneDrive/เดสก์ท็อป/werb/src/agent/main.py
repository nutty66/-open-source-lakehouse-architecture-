import argparse
import json
import os
from datetime import datetime

from detector import detect_schema_drift
from diagnoser import diagnose
from repair import create_pr_suggestion, apply_staging_change, rollback_staging
from ge_checks import run_all_checks
from github_integration import create_pr_fallback_local, create_github_pr
from langchain_integration import render_prompt, generate_pr_text_with_openai


def load_expected(path='expected_schema.json'):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def write_audit(audit_record, path='audit_log.json'):
    logs = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            try:
                logs = json.load(f)
            except Exception:
                logs = []
    logs.append(audit_record)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def run(mode, input_csv, force_fail: bool = False):
    expected = load_expected()
    expected_cols = expected.get('columns', [])
    new_cols, missing_cols = detect_schema_drift(input_csv, expected_cols)
    diag = diagnose(new_cols, missing_cols)

    ts = datetime.utcnow().isoformat() + 'Z'
    audit = {
        'time': ts,
        'input': input_csv,
        'expected_columns': expected_cols,
        'new_columns': new_cols,
        'missing_columns': missing_cols,
        'diagnosis': diag,
        'mode': mode,
    }

    print('Diagnosis:', diag)

    if mode == 'alert':
        write_audit(audit)
        print('Alert mode: logged audit only')
        return

    if mode == 'suggest-pr':
        pr = create_pr_suggestion('expected_schema.json', new_cols, input_csv)
        # generate PR text using LLM fallback
        input_json = json.dumps({'new_columns': new_cols, 'input_file': input_csv}, ensure_ascii=False)
        prompt = render_prompt(input_json)
        pr_text = generate_pr_text_with_openai(prompt)
        # append LLM text to PR file
        try:
            with open(pr, 'a', encoding='utf-8') as f:
                f.write('\n\n## Suggested PR Text\n')
                f.write('Title: ' + pr_text['title'] + '\n\n')
                f.write(pr_text['body'])
        except Exception:
            pass
        audit['pr'] = pr
        write_audit(audit)
        print('Created PR suggestion at', pr)
        return

    if mode == 'auto-staging':
        # apply staging change with backup
        staging_path, backup = apply_staging_change('expected_schema.json', new_cols)
        print('Applied change to staging at', staging_path, 'backup:', backup)
        # run GE-like checks
        ok, results = run_all_checks(input_csv, json.load(open(staging_path, encoding='utf-8')))
        if force_fail:
            ok = False
            results = results + ['(forced failure)']
        print('GE-check results:', results)
        if not ok:
            # rollback
            rolled = rollback_staging(backup)
            audit['staging'] = staging_path
            audit['rollback'] = rolled
            write_audit(audit)
            print('Checks failed — rolled back:', rolled)
            return
        # on success, optionally create PR to promote to main (local fallback)
        branch = 'agent-auto-staging/' + datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        title = f'Agent: add columns {new_cols}'
        body = 'Auto-applied to staging. GE checks passed. Promote to main via PR.'
        token = os.environ.get('GITHUB_TOKEN')
        repo = os.environ.get('GITHUB_REPO')
        pr_location = None
        if token and repo:
            try:
                pr_resp = create_github_pr(token, repo, branch, title, body)
                pr_location = pr_resp.get('html_url')
            except Exception as e:
                pr_location = create_pr_fallback_local(branch, title, body)
        else:
            pr_location = create_pr_fallback_local(branch, title, body)

        audit['staging'] = staging_path
        audit['pr'] = pr_location
        write_audit(audit)
        print('Staging OK. PR created at', pr_location)
        return

    print('Unknown mode')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['alert', 'suggest-pr', 'auto-staging'], default='alert')
    parser.add_argument('--input', required=True)
    parser.add_argument('--force-fail', action='store_true', help='Force GE check failure to demonstrate rollback')
    args = parser.parse_args()
    run(args.mode, args.input, force_fail=args.force_fail)
