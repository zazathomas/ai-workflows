# Standalone CLI Productization Decisions

Use this reference when converting Agentic Coding v2 from a Hermes skill/FSM script into a standalone CLI application.

## Product Boundary

- Build a standalone CLI application, not a thin wrapper around `~/.hermes/skills/...`.
- The CLI becomes the source of truth for workflow state, stage rules, schemas, artifacts, and transitions.
- The Hermes skill becomes an integration/consumer layer that calls the CLI later.
- Preserve compatibility with current artifact names and stage IDs so existing Hermes workflows can migrate cleanly.

## UX and Command Philosophy

- Automation-first: deterministic, scriptable commands before interactive UX.
- Interactive helpers may be layered later, but core behavior must work non-interactively.
- Every core/mutating/read-only automation command should support `--json`.
- Use stable documented exit codes so agents/CI can distinguish approval-needed, blocked, validation-failed, and usage-error states.

## Naming and Packaging

- CLI binary: `agentic`.
- Repository/distribution: `agentic-coding`.
- Python package: `agentic_coding`.
- Workflow ID: `coding-v2`.
- Display name: `Agentic Coding v2`.
- Implement v1 in Python with `uv`.
- Use Typer for the CLI layer, but keep core FSM/workflow logic framework-independent.
- Use Pydantic v2 for internal models and expose JSON Schema for external tools.

## Default Storage Model

- Task artifacts live under `docs/temp-<task-id>/` by default.
- Task IDs use `temp-<UTC timestamp>-<goal-slug>`, e.g. `temp-20260619-143012-add-billing-settings`.
- Multiple task dirs may exist, but one current task is selected per repo.
- Current task pointer lives at `.agentic/current`.
- Treat task artifacts as ephemeral/local by default and recommend ignoring `docs/temp-*`; do not silently mutate `.gitignore` unless explicitly requested.
- Provide export commands for deliberate handoff/review artifacts.

## Workflow Definition Model

- Do not hardcode stages directly in Python.
- Bundle versioned workflow data files, e.g. `workflows/coding-v2/workflow.yaml`, `stages/*.md`, and templates.
- v1 supports only bundled `coding-v2`; design loader for future project/org overrides but defer custom workflow support.
- Pin each task to `workflow_id` and `workflow_version` at init.
- Load stage cards on demand; do not copy all stage cards into every task at init.
- Bundle only core policy, stage cards, and templates in v1; leave specialized legacy references out unless promoted later.

## State, Events, and Artifacts

- `state.json` is the current snapshot.
- Add append-only `events.jsonl` in v1 for audit/replay/recovery.
- Include a minimal explicit state migration framework from day one: `state_schema_version`, `agentic migrate`, backups, and migration tests.
- Preserve read/migrate compatibility with current `agentic_coding_fsm.py` state directories.
- CLI owns and updates standard markdown artifacts automatically using managed sections:
  - `todos.md`
  - `checkpoint.md`
  - `artifacts.md`
  - `context-capsule.md`
  - `snapshots/<stage-id>-summary.md`
- Freeform human/agent notes live outside managed sections; support `agentic note add`.
- Keep separate stage-boundary snapshots in v1; `checkpoint.md` is the current resume point, not the historical record.

## Core v1 Commands

Core lifecycle:
- `agentic init`
- `agentic status`
- `agentic next`
- `agentic list`
- `agentic use`
- `agentic complete`
- `agentic skip`
- `agentic block`
- `agentic unblock`
- `agentic approve`
- `agentic revisit`
- `agentic assert-final`

Evidence/artifacts:
- `agentic run -- <command...>`
- `agentic evidence add`
- `agentic artifact add`
- `agentic note add`
- `agentic export`
- `agentic capsule show/refresh`
- `agentic files add/list/scan`
- `agentic acceptance add/list/complete`

Workflow/schema/maintenance:
- `agentic workflow list/show/validate`
- `agentic schema state/workflow/event`
- `agentic validate`
- `agentic migrate`
- `agentic doctor`
- advanced/experimental `agentic repair`

## Transition Rules and Evidence

- `complete` infers `state.current_stage`; optional `--stage` is a safety assertion only and cannot jump stages.
- Every stage completion requires non-empty evidence.
- `skip` requires non-empty reason and must obey workflow skip policy.
- `block`/`unblock` are first-class; unresolved blockers prevent normal advancement.
- Human approvals are explicit durable events/scopes, not only booleans in state.
- For Standard/Strict, `PLAN-20 -> BUILD-30` requires explicit `plan_to_build` approval.
- Support explicit workflow-constrained loops via `agentic revisit <stage> --reason ...`.
- Revisits preserve historical completions but mark target/downstream stages invalidated via `invalidated_stages` and `stage_attempts` until refreshed evidence exists.

## Mode, Risk, Tier, and Acceptance Criteria

- Make `mode`, `risk`, and `model_tier` first-class controlled fields.
- Defaults: `standard`, `medium`, `tier-2-normal`.
- Enforce explicit contradictions such as high-risk/tier-3 work being lightweight; warn on inferred risk signals rather than hard-blocking keyword matches.
- Acceptance criteria are structured first-class items with IDs, status, and evidence.
- Init may omit acceptance criteria for Lightweight/Standard with warnings.
- Strict requires at least one criterion or an explicit deferred-acceptance reason.
- Final assertion fails if acceptance criteria are missing/incomplete unless explicitly scoped out.

## Command Runner and Git

- Include simple `agentic run -- <command...>` in v1 for evidence capture.
- It may run explicit arbitrary commands, but v1 must not support automatic configured shell hooks.
- `run --as-evidence` records evidence only; it does not auto-complete stages.
- Save command logs under `docs/temp-<id>/artifacts/commands/`.
- Git integration is read-only/passive by default: detect repo root, branch, status, diff stat/check, and warnings.
- `.gitignore` mutation only with explicit flags such as `--update-gitignore` or `doctor --fix-gitignore`.
- Defer commit/push/PR helpers.

## Repo Root and Config

Repo root detection priority:
1. explicit `--root`
2. nearest parent containing `.git`
3. nearest parent containing `.agentic/config.toml`
4. current working directory

- v1 includes minimal project config at `.agentic/config.toml`.
- Defer global user config until after v1 to keep behavior reproducible.

## Final Assertion

`agentic assert-final` should combine:
- deterministic workflow/state checks
- passive repo hygiene checks

It should not automatically run expensive validation unless explicitly requested.

## Development Plan

Start with a thin vertical slice before the full surface:
1. `uv` project skeleton
2. Typer CLI entry point
3. bundled `coding-v2` workflow definition
4. Pydantic state models
5. `agentic init`
6. `.agentic/current`
7. `agentic status`
8. `agentic complete`
9. `events.jsonl`
10. managed `checkpoint.md` and `todos.md`
11. JSON output
12. tests for init/status/complete

Then expand to skip/block/unblock/approve, run/evidence/artifact/note, assert-final, migrate, export, workflow/schema/doctor.

## Tests and Docs

- Include real docs from day one: README, workflow docs, state schema docs, exit codes, and future Hermes integration notes.
- Require migration tests for the current FSM runner state format under `tests/fixtures/legacy/`.
- Test init/status/complete, JSON output, event logging, managed markdown updates, current pointer behavior, and transition enforcement.
