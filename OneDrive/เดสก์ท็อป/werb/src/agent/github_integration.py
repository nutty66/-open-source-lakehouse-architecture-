import os
import requests

def create_github_pr(token: str, repo: str, branch: str, title: str, body: str) -> dict:
    """Create a PR on GitHub. `repo` format: owner/repo"""
    if not token:
        raise ValueError('GITHUB token required')
    api = 'https://api.github.com'
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
    # create a PR
    owner_repo = repo
    url = f'{api}/repos/{owner_repo}/pulls'
    payload = {'title': title, 'head': branch, 'base': 'main', 'body': body}
    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()
    return r.json()

def create_pr_fallback_local(branch: str, title: str, body: str) -> str:
    os.makedirs('prs', exist_ok=True)
    # sanitize branch for filename
    safe_branch = branch.replace('/', '_').replace(':', '_')
    path = os.path.join('prs', f'pr_github_{safe_branch}.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('# PR (local fallback)\n')
        f.write('Branch: ' + branch + '\n\n')
        f.write('Title: ' + title + '\n\n')
        f.write(body)
    return path
