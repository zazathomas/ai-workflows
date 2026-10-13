# Phase 2 — Planning and Decomposition

## Goal
Turn requirements into small, dependency-ordered, verifiable tasks with model tiers, touched-file boundaries, and validation commands.

## Planning Rules

1. Plan in read-only mode first.
2. Use Phase 0 and Phase 0.5 findings as constraints.
3. Prefer vertical slices that deliver one end-to-end behavior path.
4. Make every task independently verifiable.
5. Assign a model tier to every task.
6. Include enough context that subagents do not need broad repo rediscovery.
7. Parallelize only independent file scopes.
8. Include tests for every behavior change unless explicitly impossible.
9. Identify human gates and stop conditions.
10. For Standard/Strict work, create or update `docs/temp-{id}/todos.md` as the full-stage completion ledger before requesting plan approval.
11. Ensure `todos.md` includes every task across every activated stage, including docs, review, validation, and delegated subtasks; skipped stages must appear with explicit reasons.

## Dependency Graph

Before writing tasks, identify:

- Foundation tasks that unblock others.
- API/backend/frontend contract dependencies.
- Schema/migration dependencies.
- Tests that must be written before implementation.
- Docs/design/observability tasks.
- Tasks unsafe to run in parallel.

## Task Shape

```md
- [ ] T###: Short task title
  - Model tier: 🟢/🟡/🔴
  - Goal:
  - Context:
  - Dependencies:
  - Files to inspect:
  - Files to create/modify:
  - Files out of scope:
  - Required tests:
  - Validation commands:
  - Acceptance criteria:
  - Risk notes:
```

## Plan Shape

```md
# Implementation Plan

## Scope Summary
- Workflow mode:
- Risk level:
- Model tier:
- Feature/fix summary:

## Potential Conflicts & Assumptions
- Consequence scan results:
- Existing conventions:
- Known conflicts:
- Assumptions:

## Architecture / Interface Notes
- Data model/storage:
- API/interface:
- UI/design:
- Security/trust boundaries:

## Ordered Tasks
...

## Validation Strategy
- Targeted:
- Affected-area:
- Final:

## Rollback / Recovery
...

## Docs / Observability
...
```

## Human Gate

For Standard/Strict work, present the plan summary to the user before implementation and stop for explicit input. Offer two clear choices:

1. **Approve plan** — proceed to Phase 3 implementation.
2. **Request changes** — user provides adjustments; revise the plan and ask again.

The plan summary must include:

- Key tasks.
- Expected touched files.
- Risk level and model tiers.
- Acceptance criteria.
- Validation commands.
- `todos.md` location and confirmation that it covers all activated stages.
- Any unresolved assumptions.

Do not begin Phase 3 until the user chooses **Approve plan**. If the user chooses or implies changes, revise and re-request approval.

## Stop Conditions

Pause and re-plan if:

- Requirements conflict.
- Plan requires out-of-scope files.
- New dependency/migration/secret/destructive action is needed.
- Diff would expand beyond expected files.
- Existing tests are too broken to prove regression.
- Subagents disagree on direction or overlap changes.
