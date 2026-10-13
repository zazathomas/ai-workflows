# Doubt-Driven Review

## Goal
Subject high-risk or uncertain decisions to a fresh, adversarial review before they become implementation or final output.

## When to Use

Use for:

- 🔴 Tier 3 work.
- Auth/authz, tenant isolation, payments, secrets, crypto, migrations.
- Public API/interface contract decisions.
- Architecture choices that are hard to reverse.
- Changes where the obvious solution may conflict with existing model semantics.
- Unfamiliar code or domain where confidence is low.

## Process

1. **Claim:** State the design/implementation claim clearly.
2. **Artifact:** Extract the smallest reviewable artifact: plan excerpt, diff, schema, endpoint, component, or test.
3. **Contract:** State what must be true: security boundary, acceptance criteria, compatibility, performance, etc.
4. **Doubt:** Ask a fresh reviewer/subagent to find flaws, missed consumers, simpler alternatives, security issues, and hidden assumptions.
5. **Reconcile:** Accept, reject with reason, or re-plan based on findings.
6. **Stop:** Do not recursively review forever; one or two bounded passes is enough.

## Reviewer Prompt Template

```text
Review this artifact adversarially. Assume it may be subtly wrong.

CLAIM:
...

CONTRACT / MUST-HOLD PROPERTIES:
...

ARTIFACT:
...

Find:
- correctness flaws
- missed consumers
- security/tenant/auth issues
- migration/backward compatibility issues
- simpler safer alternatives
- tests that would expose the flaw

Return Critical / Important / Suggestion findings with concrete evidence.
```

## Rules

- Use read-only review where possible.
- Do not let the reviewer modify files unless explicitly delegated as a fix task.
- Controller decides final reconciliation.
- Document accepted risks.

## Output

Record:

- Claim reviewed.
- Reviewer findings.
- Changes made or reasons for rejecting findings.
- Remaining risks.
