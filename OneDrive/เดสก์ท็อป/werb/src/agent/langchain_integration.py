import os
from typing import Dict

PROMPT_TEMPLATE = '''
You are an automated PR author for a data engineering repo.
Given the proposed schema change, write a concise PR title and body describing:
- what changed (which columns added/removed),
- rationale, tests to run (dbt + GE),
- rollback steps.

Input JSON:
{input_json}

Respond in JSON with keys: title, body
'''

def render_prompt(input_json: str) -> str:
    return PROMPT_TEMPLATE.format(input_json=input_json)

def generate_pr_text_with_openai(prompt: str):
    # optional: use OpenAI via LangChain or requests
    # this function is a placeholder; if OPENAI_API_KEY set use simple completion via requests
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        # fallback: simple deterministic text
        return {
            'title': 'Auto PR: add nullable columns',
            'body': 'Proposed: add columns as nullable. Run dbt test and GE checks. Rollback by restoring previous schema.'
        }
    # If user has LangChain/OpenAI configured, they can implement here.
    return {
        'title': 'Auto PR: add nullable columns (LLM)',
        'body': 'LLM-generated body (user has OPENAI_API_KEY so integrate LangChain here)'
    }
