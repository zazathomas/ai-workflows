# SCAN-05 — Consequence Scan

## Purpose

Search for existing fields, statuses, APIs, routes, fixtures, tests, migrations, consumers, and business rules that could be affected before planning or editing.

## Entry Criteria

- Discovery is complete.
- The task may affect behavior, data shape, API contracts, persistence, frontend consumers, tests, or docs.

## Required Actions

- Search relevant symbols, routes, strings, types, schemas, statuses, config keys, and docs.
- Identify direct and indirect consumers.
- Check tests, fixtures, serializers/adapters, migrations, and generated artifacts when relevant.
- Record potential collisions, compatibility concerns, and out-of-scope areas.

## Exit Criteria

- Impacted surfaces and consumers are listed.
- Required follow-up checks are converted into `todos.md` rows.
- If scan is skipped, the reason is explicit and low-risk.
- `state.json.current_stage` advances to `SPEC-10`.

## Supporting References

- `references/phase-0-5-consequence-scan.md`
- `references/api-interface-design.md` for public contracts
- `references/deprecation-migration.md` for replacement/removal work

## Stage Boundary Commit

Before advancing:

1. Update `todos.md` with status, owner, evidence, and blockers.
2. Update `checkpoint.md` with completed work, decisions, risks, and next action.
3. Update `state.json.completed_stages`, `state.json.current_stage`, and `state.json.next_action`.
4. Add or update `snapshots/SCAN-05-summary.md` using `templates/stage-summary.md`.
5. If any exit criterion is not met, stay in this stage or mark the task blocked.
