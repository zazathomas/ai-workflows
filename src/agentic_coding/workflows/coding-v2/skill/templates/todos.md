# Task Ledger

Task ID: `temp-YYYYMMDD-short-name`  
Goal: TODO  
Mode/Risk/Tier: TODO  
Current Stage: `DISC-00`

## Ledger

| ID | Stage | Task | Owner | Status | Evidence | Blocker/Skip Reason |
| --- | --- | --- | --- | --- | --- | --- |
| T-001 | DISC-00 | Inspect repo root, branch, and dirty worktree | controller | pending | | |
| T-002 | SCAN-05 | Consequence scan or explicit skip reason | controller | pending | | |
| T-003 | SPEC-10 | Acceptance criteria and constraints recorded | controller | pending | | |
| T-004 | PLAN-20 | Plan and validation commands recorded | controller | pending | | |
| T-005 | BUILD-30 | Implementation slices completed | controller | pending | | |
| T-006 | VERIFY-40 | Validation evidence collected | controller | pending | | |
| T-007 | REVIEW-50 | Diff/security/acceptance review completed | controller | pending | | |
| T-008 | DOC-60 | Docs updated or skipped with reason | controller | pending | | |
| T-009 | SHIP-70 | Final status/diff/ship checks completed | controller | pending | | |

## Status Vocabulary

- `pending`
- `in_progress`
- `done`
- `blocked`
- `skipped`
- `deferred-by-user`

## Rules

- Every activated stage must have at least one row.
- Skipped stages require a reason.
- Done rows require evidence.
- The final response is not allowed while required rows remain `pending` or `in_progress`.
