# Phase 3 — Implementation, TDD, and Delegation

## Goal
Implement one verified slice at a time using TDD, scoped delegation, and controller verification.

## Increment Cycle

```text
Pick task → RED test → minimal GREEN code → targeted validation → simplify → affected-area validation → review diff → next task
```

Each increment should leave the system compilable, testable, and rollback-friendly.

## TDD Rules

For new behavior:

1. Write or update a test that describes expected behavior.
2. Confirm it fails for the expected reason when practical.
3. Implement the minimum code to pass.
4. Run the focused test and affected-area tests.
5. Refactor/simplify while tests stay green.

For bug fixes:

1. Reproduce the bug with a failing test or reliable manual repro.
2. Fix the root cause, not just the symptom.
3. Add a guard against recurrence.
4. Verify end-to-end if user-visible.

## Delegation Rules

Delegate only when it adds value. Avoid delegation for tiny local edits, fragile migrations/deploys, secret-file changes, or work where verification requires doing the whole task manually.

When delegating, provide:

- Exact task text and acceptance criteria.
- Mode, risk, and model tier.
- Repo root, stack, commands.
- Context files already read.
- Files allowed/forbidden to modify.
- Test commands and expected evidence.
- Scope boundaries: no broad repo scans, no dependencies, no commits unless instructed.

## Model Tier Routing

- 🟢 Tier 1: bundle mechanical tasks; route to cheapest configured model when available.
- 🟡 Tier 2: default/main model.
- 🔴 Tier 3: controller or best model; use exhaustive context and extra verification if delegated.

## Subagent Return Contract

Require:

```md
- Summary:
- Files changed:
- Tests added/updated:
- Commands run:
  - command:
    exit_code:
    result:
- TDD evidence:
  - failing test summary:
  - passing test summary:
- Known limitations:
- Suggested controller verification:
```

## Controller Verification

After every delegated or local task:

```bash
git diff --name-only
git diff --stat
git diff --check
```

Then verify using file reads, tests, lint/build, API/browser smoke, or security checks as appropriate. Do not mark complete from a subagent summary alone.

## Frontend Runtime Verification

For UI work, source checks are not enough:

- Run the app.
- Browser-smoke the actual dev-server URL/port.
- Use screenshots or DOM measurements for visual claims.
- Check responsive widths when mobile/tablet behavior is relevant.
- Verify persistence through UI/API readback for CRUD changes.

## Failure Handling

When validation fails:

1. Preserve exact command and output.
2. Classify cause: implementation, pre-existing, environment, dependency, bad plan.
3. Fix narrowly and rerun.
4. After two failed attempts, stop and re-plan.
5. Revert unrelated/off-scope edits.
