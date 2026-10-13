# PLAN-20 — Plan

## Purpose

Break the work into small, dependency-ordered vertical slices with model tiers, owners, touched files, validation commands, and approval gates.

## Entry Criteria

- Acceptance criteria and risk/mode are recorded.

## Required Actions

- Create or update `PLAN.md` for Standard/Strict work.
- Populate `todos.md` with all activated stages, including skipped stages with reasons.
- Map each task to acceptance criteria and validation evidence.
- Assign model tier and owner/controller/subagent.
- Identify delegation context capsules where needed.
- For Standard/Strict, stop for human approval before `BUILD-30`.

## Exit Criteria

- Plan is dependency-ordered and scoped.
- Validation commands and evidence expectations are listed.
- Human approval has been obtained for Standard/Strict work, or the task is blocked awaiting approval.
- `state.json.current_stage` advances to `BUILD-30` only after required approval.

## Supporting References

- `references/phase-2-planning-decomposition.md`
- `templates/context-capsule.md`
- `references/delegation-template-v2.md`

## Stage Boundary Commit

Before advancing:

1. Update `todos.md` with status, owner, evidence, and blockers.
2. Update `checkpoint.md` with completed work, decisions, risks, and next action.
3. Update `state.json.completed_stages`, `state.json.current_stage`, and `state.json.next_action`.
4. Add or update `snapshots/PLAN-20-summary.md` using `templates/stage-summary.md`.
5. If any exit criterion is not met, stay in this stage or mark the task blocked.
