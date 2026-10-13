# SPEC-10 — Specify

## Purpose

Turn the request and discovered context into explicit acceptance criteria, assumptions, constraints, non-goals, risk level, and mode.

## Entry Criteria

- Discovery is complete.
- Consequence scan is complete or explicitly skipped.

## Required Actions

- Write acceptance criteria that can be verified.
- Record assumptions and open questions.
- Identify non-goals and files/areas out of scope.
- Record security/privacy/performance/compatibility concerns.
- Confirm mode and risk; upgrade mode if lightweight is forbidden.
- Ask only blocker-first questions after available context has been read.

## Exit Criteria

- Acceptance criteria are in `state.json.acceptance_criteria` and/or `PLAN.md`.
- Open questions are answered, non-blocking, or explicitly deferred.
- Mode/risk/model tier are recorded.
- `state.json.current_stage` advances to `PLAN-20`.

## Supporting References

- `references/phase-1-requirements-spec.md`

## Stage Boundary Commit

Before advancing:

1. Update `todos.md` with status, owner, evidence, and blockers.
2. Update `checkpoint.md` with completed work, decisions, risks, and next action.
3. Update `state.json.completed_stages`, `state.json.current_stage`, and `state.json.next_action`.
4. Add or update `snapshots/SPEC-10-summary.md` using `templates/stage-summary.md`.
5. If any exit criterion is not met, stay in this stage or mark the task blocked.
