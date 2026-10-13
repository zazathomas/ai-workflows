# DISC-00 — Discovery / Safety

## Purpose

Understand the task, repository, current branch, dirty worktree, project docs, commands, and constraints before making changes.

## Entry Criteria

- User has requested a code/build/debug/project change.
- No reliable current task state exists, or `state.json.current_stage` is `DISC-00`.

## Required Actions

- Identify repo root and current working directory.
- Inspect branch and `git status --short` for user changes.
- Inspect relevant README, docs index, design docs, business docs, or existing plans.
- Identify likely touched areas and validation commands.
- Initialize runtime artifacts for Standard/Strict or multi-step Lightweight work.
- Record mode, risk, and initial model tier.

## Exit Criteria

- Worktree state is understood and user changes are protected.
- Relevant docs/context have been read or explicitly marked not applicable.
- Runtime artifacts are initialized or intentionally skipped with reason.
- `state.json.current_stage` advances to `SCAN-05`, or `SCAN-05` is explicitly skipped with reason.

## Supporting References

- `references/phase-0-discovery-safety.md`

## Stage Boundary Commit

Before advancing:

1. Update `todos.md` with status, owner, evidence, and blockers.
2. Update `checkpoint.md` with completed work, decisions, risks, and next action.
3. Update `state.json.completed_stages`, `state.json.current_stage`, and `state.json.next_action`.
4. Add or update `snapshots/DISC-00-summary.md` using `templates/stage-summary.md`.
5. If any exit criterion is not met, stay in this stage or mark the task blocked.
