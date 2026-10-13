# BUILD-30 — Build

## Purpose

Implement one verified vertical slice at a time while preserving user work and keeping the repo in a testable state.

## Entry Criteria

- Plan is approved if Standard/Strict.
- Current slice is listed in `todos.md`.
- Required context and files are known.

## Required Actions

- Prefer TDD: reproduce bug or write/update focused test before production changes when practical.
- Edit only scoped files unless new evidence requires plan revision.
- Keep each slice small and compilable/testable.
- Record changed files and rationale.
- Re-anchor to `state.json` and `checkpoint.md` after long tool output or delegated work.
- Run targeted validation for each slice where possible.

## Exit Criteria

- Planned implementation slices are done or explicitly blocked/deferred.
- Touched files are recorded.
- Targeted checks for each slice are recorded.
- `state.json.current_stage` advances to `VERIFY-40`.

## Supporting References

- `references/phase-3-implementation-tdd-delegation.md`
- `test-driven-development`
- `systematic-debugging` when failures/bugs drive the work
- `references/source-driven-development.md` when framework/library details matter

## Stage Boundary Commit

Before advancing:

1. Update `todos.md` with status, owner, evidence, and blockers.
2. Update `checkpoint.md` with completed work, decisions, risks, and next action.
3. Update `state.json.completed_stages`, `state.json.current_stage`, and `state.json.next_action`.
4. Add or update `snapshots/BUILD-30-summary.md` using `templates/stage-summary.md`.
5. If any exit criterion is not met, stay in this stage or mark the task blocked.
