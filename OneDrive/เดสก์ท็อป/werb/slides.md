# Workshop: Self-Healing Data Agent (25 นาที)

## 1. Problem (2 min)
- Example: nightly ELT fails — CSV from Sales team has a new column → pipeline fails.

## 2. Detection (3 min)
- Signals: schema drift, dbt/GE test failures, row-count diffs, parse errors, downstream SLA alerts.

## 3. Architecture (5 min)
- Components: Detector, Diagnoser, Repair-suggester, Orchestrator, Auditor.
- Tech: LangChain / LangGraph, CrewAI/AutoGen (multi-agent), dbt, Great Expectations, OpenLineage, GitHub.

## 4. Agentic Loop (5 min)
1. Detect → 2. Triage → 3. Probe → 4. Decide (policy) → 5. Execute (guarded) → 6. Validate → 7. Promote/Rollback → 8. Audit

## 5. Guardrails & HIL (3 min)
- No destructive ops without approval, least-privilege creds, budget caps, kill-switch, explicit rollback plan.

## 6. Demo walkthrough (5 min)
- Show POC: detect schema drift, create PR suggestion, auto-staging with GE-like checks, and rollback on failure.

## 7. Next steps / Q&A (2 min)
- POC → integrate LangChain LLM for PR text, connect GitHub and CI, extend GE suites, measure ROI.
