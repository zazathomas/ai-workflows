# VERIFY-40 — Verify

## Purpose

Prove the implementation satisfies acceptance criteria with real commands, tests, builds, browser/API checks, or other concrete evidence.

## Entry Criteria

- Implementation slice(s) are complete or ready for validation.

## Required Actions

- Run planned validation commands.
- Add missing validation if discovered coverage is inadequate.
- Capture command, result, and evidence pointer in `todos.md`/`state.json.validation`.
- For full-stack work, validate the actual client/browser/API path when relevant.
- If validation fails, update blockers and return to `BUILD-30` or `PLAN-20`.
- For containerization tasks, validate with the real container runtime when available (`docker compose config/build/up` or equivalent). If no runtime is installed, do not mark the stack fully verified; run a static syntax/structure fallback such as YAML parsing, record the runtime validation as blocked, and state the missing verification clearly in the final report.

## Exit Criteria

- Every acceptance criterion has passing evidence or a clearly stated blocker/deferred reason.
- Failed checks are fixed, blocked, or explicitly accepted by user.
- `state.json.current_stage` advances to `REVIEW-50`.

## Supporting References

- `references/phase-5-review-security-acceptance.md` for acceptance traceability

## Stage Boundary Commit

Before advancing:

1. Update `todos.md` with status, owner, evidence, and blockers.
2. Update `checkpoint.md` with completed work, decisions, risks, and next action.
3. Update `state.json.completed_stages`, `state.json.current_stage`, and `state.json.next_action`.
4. Add or update `snapshots/VERIFY-40-summary.md` using `templates/stage-summary.md`.
5. If any exit criterion is not met, stay in this stage or mark the task blocked.
