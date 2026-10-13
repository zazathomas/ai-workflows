# DOC-60 — Document

## Purpose

Update durable project knowledge so future users and agents understand the new behavior, setup, architecture, or decisions.

## Entry Criteria

- Review is complete or documentation is needed to resolve review findings.

## Required Actions

- Update README, docs index, PRD/spec, architecture, DESIGN.md, ADRs, changelog, or runbooks when affected.
- Remove or revise stale docs that contradict the new behavior.
- Record docs intentionally not needed for tiny/internal changes.
- Update `artifacts.md` with documentation paths.

## Exit Criteria

- Required docs are updated or explicitly not needed with reason.
- Documentation reflects actual implementation and validation state.
- `state.json.current_stage` advances to `SHIP-70`.

## Supporting References

- `references/phase-4-documentation-index.md`
- `references/observability-launch.md` for production-facing launches

## Stage Boundary Commit

Before advancing:

1. Update `todos.md` with status, owner, evidence, and blockers.
2. Update `checkpoint.md` with completed work, decisions, risks, and next action.
3. Update `state.json.completed_stages`, `state.json.current_stage`, and `state.json.next_action`.
4. Add or update `snapshots/DOC-60-summary.md` using `templates/stage-summary.md`.
5. If any exit criterion is not met, stay in this stage or mark the task blocked.
