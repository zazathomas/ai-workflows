# Phase 5 — Review, Security, and Acceptance

## Goal
Prove the change is correct, safe, scoped, maintainable, and satisfies the requested outcome before finalizing.

## Diff-First Review

Run:

```bash
git status --short
git diff --stat
git diff --check
git diff
```

Review for:

- Unrelated files.
- Formatting-only drift.
- Generated/lock/snapshot changes.
- Secret exposure.
- Debug logs, TODOs, dead code.
- Tests and docs matching behavior.

## Five-Axis Review

Evaluate:

1. **Correctness** — requirements, edge cases, error paths, concurrency/data consistency.
2. **Readability & Simplicity** — names, control flow, unnecessary abstractions, duplication.
3. **Architecture** — boundaries, conventions, coupling, migration/deprecation shape.
4. **Security** — auth/authz, validation, secrets, injection, tenant isolation, sensitive logs.
5. **Performance** — N+1 queries, unbounded operations, payload size, expensive render paths.

## Security Review

Use risk-appropriate checks:

- Input validation and output encoding.
- Auth/authz on every state-changing or sensitive endpoint.
- Tenant isolation and platform-owner separation.
- Secrets/config handling.
- DTO exposure and sensitive fields.
- Injection, SSRF, deserialization, file upload/download, command execution.
- CORS/CSRF/session/token handling.
- Dependency advisories and install scripts when deps changed.
- Sensitive logging and deployment defaults.

Run available tools when appropriate: `npm audit`, `pip-audit`, `bandit`, `gosec`, `cargo audit`, secret scanning, native tests. Note missing tools honestly.

## Acceptance Traceability

For Standard/Strict work, trace every acceptance criterion:

| Acceptance criterion | Implementation | Validation evidence | Status |
| --- | --- | --- | --- |
| ... | files/functions | test/manual command/browser/API smoke | Done/Deferred/Blocked |

Passing tests are not enough if requested behavior is missing.

## Full-Stack CRUD Proof

For full-stack CRUD/API/UI changes, verify at least one representative path through the real client:

1. Change a visible form field or trigger state-changing action.
2. Save/submit.
3. Confirm persistence via API readback, DB/read model, or page refresh/re-query.
4. Verify unauthorized roles and dependency-blocked deletes when relevant.

## Independent / Doubt Review

Use `doubt-driven-review.md` for 🔴 Tier 3 work, unfamiliar architecture, security boundaries, or decisions that feel plausible but unproven.

## Output

Final review summary should include:

- What changed.
- Validation evidence with command exit codes where possible.
- Security findings fixed or accepted.
- Acceptance traceability.
- `todos.md` status: every stage item completed; if anything is blocked/deferred, the request is incomplete unless the user explicitly changed scope.
- Known limitations/blockers.
- Follow-ups.
