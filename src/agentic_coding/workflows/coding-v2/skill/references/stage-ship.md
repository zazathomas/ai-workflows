# SHIP-70 — Ship / Finalize

## Purpose

Prepare the final handoff: current status, validation evidence, diff summary, known blockers, rollback/observability notes, and optional commit behavior.

## Entry Criteria

- Documentation stage is complete or intentionally skipped.
- All prior required stages are complete, skipped with reason, blocked, or user-scoped out.

## Required Actions

- Run final `git status --short`.
- Run `git diff --stat`; run `git diff --check` when code changed.
- Re-open `state.json`, `todos.md`, and `checkpoint.md`; ensure they match actual repo state.
- Confirm all acceptance criteria have evidence or blockers.
- Commit only if requested or clearly implied. Push only with explicit approval.
- Include rollout/rollback/observability notes for production-facing work.

## Exit Criteria

- Final response accurately reports what changed, what was verified, and what remains blocked/deferred.
- No hidden incomplete required item remains.
- User has clear next steps if push/deploy/approval is needed.

## Supporting References

- `references/phase-6-validation-commit-ship.md`

## Stage Boundary Commit

Before finishing:

1. Update `todos.md` with final status, evidence, and blockers.
2. Update `checkpoint.md` with final state and next action.
3. Update `state.json.completed_stages`, `state.json.current_stage`, and `state.json.next_action`.
4. Add or update `snapshots/SHIP-70-summary.md` using `templates/stage-summary.md`.
5. If any exit criterion is not met, report the task as blocked or incomplete instead of claiming completion.
