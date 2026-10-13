# Phase 6 — Final Validation, Commit, and Ship

## Goal
Leave the repo in a validated, intentional final state. Commit or push only according to user intent.

## Final Validation

Always run cheap final checks:

```bash
git status --short
git diff --stat
git diff --check
```

Then run project-specific final validation appropriate to risk:

- Targeted and affected tests.
- Full test suite where feasible/needed.
- Lint/typecheck/build.
- Browser/API smoke.
- Security/dependency audit.
- Migration dry-run or rollback validation when applicable.

If `docs/temp-{id}/todos.md` exists, inspect it before finalizing. The request is not complete until every checklist item across every stage is completed. Blocked or deferred items mean the request is incomplete unless the user explicitly changes scope and the checklist is updated accordingly. Update the file before final response so it matches reality.

If validation fails, fix narrowly and rerun the failing command at minimum. Do not report success on unverified or fabricated output.

## Final State Decision

- **No commit requested:** stop after validated changes and summarize.
- **Commit requested or clearly implied:** commit only after validation succeeds or limitations are accepted.
- **Blocked/incomplete:** do not commit partial work unless user requests a checkpoint.
- **Remote push:** ask before pushing unless the user explicitly requested push/deploy.

## Atomic Commit Guidance

If commits are requested:

- Prefer one atomic commit per completed task/checkpoint for autonomous multi-task work.
- Stage only files owned by the task; avoid blind `git add -A` when unrelated files exist.
- Keep generated/lockfile changes in the same commit as the source change that caused them, or separate mechanical commits if clearer.
- Use descriptive messages that explain intent.

Example:

```bash
git add <task-owned files>
git commit -m "feat: implement <concise behavior>"
```

## Shipping / Rollout

For production-facing releases, include:

- Success signal and failure signal.
- Post-deploy smoke checks.
- Monitoring/logs/metrics/traces to watch.
- Rollback trigger.
- Rollback steps and migration/data caveats.
- Feature flag or staged rollout notes when relevant.

Use `observability-launch.md` for deeper launch readiness.

## Final Summary Template

```md
Implemented:
- ...

Validation:
- `command` → exit code / result

Security / risk:
- ...

Docs updated:
- ...

Acceptance traceability:
- ...

Todos ledger:
- `docs/temp-{id}/todos.md` inspected; all required items completed

Commit:
- <hash or not requested>

Follow-ups / limitations:
- ...
```
