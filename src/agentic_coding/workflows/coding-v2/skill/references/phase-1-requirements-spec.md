# Phase 1 — Requirements and Spec

## Goal
Define success before building. Capture enough requirements, constraints, acceptance criteria, and non-goals for the chosen mode.

## Inputs to Read First

Before asking questions, read relevant repo and user documents discovered in Phase 0:

- README and setup docs.
- Existing PRD/SPEC/architecture/design docs.
- Business plan, strategy, pricing, roadmap, or product docs.
- Issue text, user prompt, screenshots, logs, and failing tests.

Do not ask the user for facts the repo already answers.

## Question Discipline

Ask one concise batch of blocker-first questions only when answers materially change implementation. If non-critical, proceed with explicit assumptions.

Cover as applicable:

- Problem and target users.
- Must-haves, nice-to-haves, and non-goals.
- User workflows and edge cases.
- Data/persistence/API/interface needs.
- Auth, security, privacy, compliance.
- UI style, responsive behavior, accessibility.
- Performance, reliability, observability.
- Tests and acceptance criteria.
- Timeline/scope constraints.

## Spec Requirements by Mode

### Lightweight
A session todo or scoped plan is enough if it states:

- Goal.
- Touched files.
- Validation command(s).
- Risk/security notes.
- Docs impact.

### Standard
Create or update a spec/PRD when requirements are not already clear. Include:

- Objective.
- Scope and non-goals.
- Users/workflows.
- Acceptance criteria.
- Commands and stack notes.
- Boundaries and assumptions.

### Strict
Create or update a full PRD/spec plus architecture/trust-boundary notes. Include:

- Security/privacy/compliance requirements.
- Data model and migration expectations.
- Rollback and observability expectations.
- Acceptance traceability plan.

## Frontend/UI Requirements

For frontend/product UI work:

- If new design language or major redesign: use sketch exploration before app implementation.
- If existing `docs/DESIGN.md` exists: follow it unless user asks to evolve the design system.
- Capture visual tone, typography, color, spacing, motion, responsive behavior, accessibility, and screenshot/browser-smoke expectations.

## Output

A spec, PRD update, or scoped requirements summary with:

- Mode/risk/model tier.
- Assumptions.
- Acceptance criteria.
- Non-goals.
- Validation expectations.
- Human approval needed before Standard/Strict implementation unless waived.
