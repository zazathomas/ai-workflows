# Artifact Manifest

Task ID: `temp-YYYYMMDD-short-name`

| Artifact | Purpose | Stage | Status | Notes |
| --- | --- | --- | --- | --- |
| `state.json` | Canonical workflow state | all | active | |
| `todos.md` | Completion ledger | all | active | |
| `checkpoint.md` | Resume point | all | active | |
| `PLAN.md` | Implementation plan | PLAN-20 | pending | |
| `snapshots/` | Stage-boundary summaries | all | pending | |

## Rules

- Add every durable plan, spec, review note, generated file, handoff, and validation output that future agents may need.
- Mark stale artifacts as superseded instead of deleting context silently.
