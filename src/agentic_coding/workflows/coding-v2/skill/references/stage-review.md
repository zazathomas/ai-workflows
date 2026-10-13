# REVIEW-50 — Review

## Purpose

Catch quality, security, acceptance, interface, migration, performance, and maintainability issues before documentation and shipping.

## Entry Criteria

- Verification evidence exists or the task is blocked.

## Required Actions

- Inspect `git diff` and changed files.
- Run `git diff --check` for code changes.
- Perform security review proportional to risk.
- Check API/interface/backward compatibility when relevant.
- Check migrations/deprecations/observability/rollback when relevant.
- Simplify accidental complexity after green validation.
- Trace acceptance criteria to evidence.

## Exit Criteria

- Review findings are resolved, blocked, or explicitly documented.
- Security/API/migration/observability checks are complete or not applicable with reason.
- `state.json.current_stage` advances to `DOC-60`.

## Supporting References

- `references/phase-5-review-security-acceptance.md`
- `references/doubt-driven-review.md`
- `references/code-simplification.md`
- `references/api-interface-design.md`
- `references/deprecation-migration.md`
- `references/observability-launch.md`

## Stage Boundary Commit

Before advancing:

1. Update `todos.md` with status, owner, evidence, and blockers.
2. Update `checkpoint.md` with completed work, decisions, risks, and next action.
3. Update `state.json.completed_stages`, `state.json.current_stage`, and `state.json.next_action`.
4. Add or update `snapshots/REVIEW-50-summary.md` using `templates/stage-summary.md`.
5. If any exit criterion is not met, stay in this stage or mark the task blocked.
