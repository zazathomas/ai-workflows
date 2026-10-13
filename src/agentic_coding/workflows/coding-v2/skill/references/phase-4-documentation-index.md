# Phase 4 — Documentation and Index

## Goal
Make durable project knowledge match the code so future humans and agents do not rediscover or misinterpret the system.

## Update Docs When

Update docs if the task changes:

- Setup, commands, environment variables, scripts, or deployment.
- User-facing behavior, workflows, or examples.
- API/interface contracts.
- Architecture, components, data flows, trust boundaries.
- Design tokens, UI language, navigation, or accessibility patterns.
- Product scope, acceptance criteria, or business assumptions.
- Important file/module locations future agents need.

## Common Artifacts

- `README.md` — setup, usage, commands, configuration, examples.
- `docs/PRD.md` or `SPEC.md` — scope, assumptions, acceptance criteria.
- `docs/architecture.md|html|svg` — components, flows, trust boundaries.
- `docs/DESIGN.md` — durable frontend design language and tokens.
- `docs/index.md` — codebase map.
- ADRs — durable architecture decisions and alternatives.
- Changelog/release notes — user-visible release changes.

## docs/index.md Requirements

If present, keep it accurate. If missing and the task changes structure meaningfully, create it.

Recommended sections:

```md
# Codebase Index

## Overview
## Entry Points
## Major Directories
## Domain Modules
## API / Interfaces
## Data / Persistence
## Frontend / Design
## Tests
## Commands
## Operational Notes
## Recently Changed Areas
```

Rules:

- Verify paths against the live repo.
- Keep entries navigational, not verbose implementation duplication.
- Omit generated/vendor/build artifacts.
- Prune stale “recently changed” notes.

## DESIGN.md Rules

- If `docs/DESIGN.md` exists, frontend changes must follow it unless intentionally evolving the design system.
- For new selected design directions, freeze tokens, rationale, layout patterns, and do/don't guidance.
- Lint with project/design tooling when available.

## ADR Rules

Write an ADR when a decision is hard to reverse or affects architecture, storage, API contracts, security boundaries, deployment, or major dependencies.

ADR sections:

```md
# ADR-NNN: Title
## Status
## Date
## Context
## Decision
## Alternatives Considered
## Consequences
```

## Output

Summarize docs updated, docs intentionally skipped, and any future-doc follow-ups.
