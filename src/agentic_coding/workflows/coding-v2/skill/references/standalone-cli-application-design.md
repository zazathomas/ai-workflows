# Standalone CLI Application Design Notes

Use when productizing `agentic-coding-v2` from a Hermes skill/FSM runner into a standalone CLI application.

## Resolved Product Decisions

- Application boundary: standalone application. The Hermes skill becomes an integration/consumer, not the source of truth.
- CLI command: `agentic`.
- Repository/package naming:
  - distribution/repo: `agentic-coding`
  - Python package: `agentic_coding`
  - console script: `agentic`
- Primary UX: strict automation engine first; interactive helpers later.
- Default workflow: `coding-v2`.
- Workflow display name: `Agentic Coding v2`.
- Workflow definitions: bundled external data files, not hardcoded Python policy.
- v1 implementation stack: Python + uv.
- CLI framework: Typer, with framework-independent core logic.
- State models: Pydantic v2, with JSON Schema export for interoperability.

## Storage and Task Selection

- Task artifacts live under `docs/temp-<task-id>/` by default.
- Task IDs use `temp-<UTC timestamp>-<goal-slug>`.
  - Example: `temp-20260619-143012-add-billing-settings-page`.
- Multiple tasks may exist in a repo.
- Exactly one selected/current task is tracked per repo by default.
- Current-task pointer lives at `.agentic/current`.
- Task artifacts are ephemeral local state by default and should usually be gitignored.
- Do not silently edit `.gitignore`; support explicit `--update-gitignore` / doctor fix commands.
- Provide explicit export commands for durable handoff/review artifacts.

## Workflow Definition Layout

Recommended bundled package resource layout:

```text
agentic_coding/workflows/coding-v2/workflow.yaml
agentic_coding/workflows/coding-v2/stages/DISC-00.md
agentic_coding/workflows/coding-v2/stages/SCAN-05.md
agentic_coding/workflows/coding-v2/stages/SPEC-10.md
agentic_coding/workflows/coding-v2/stages/PLAN-20.md
agentic_coding/workflows/coding-v2/stages/BUILD-30.md
agentic_coding/workflows/coding-v2/stages/VERIFY-40.md
agentic_coding/workflows/coding-v2/stages/REVIEW-50.md
agentic_coding/workflows/coding-v2/stages/DOC-60.md
agentic_coding/workflows/coding-v2/stages/SHIP-70.md
agentic_coding/workflows/coding-v2/templates/...
```

`workflow.yaml` should own product policy:
- workflow ID and version
- stage order
- allowed transitions
- required artifacts
- human gates
- mode/risk/tier rules
- skip policy
- final assertion rules
- schema version

Python code should own mechanics:
- loading workflow definitions
- validating state
- enforcing transitions
- locking and atomic writes
- rendering artifacts
- CLI UX
- migrations

In v1, support only bundled `coding-v2`, but design loaders so custom workflows can be added later.

## State, Events, and Evidence

- `state.json` is the current snapshot.
- Add append-only `events.jsonl` in v1.
- Every mutating command should:
  1. acquire a per-task lock,
  2. read and validate state,
  3. validate the requested operation,
  4. write updated state atomically,
  5. append an event,
  6. update managed markdown artifacts.
- Include basic per-task locking with a lock file like `docs/temp-<task-id>/.agentic.lock`.
- Use atomic writes for `state.json`.

Evidence rules:
- Every stage completion requires non-empty evidence.
- `skip` requires a non-empty reason.
- `block` requires a non-empty reason.
- Evidence may be flexible text in v1; do not attempt semantic proof initially.
- Support evidence from command logs and artifact files.

Approvals:
- Model approvals as explicit durable events/scopes, not just a boolean flag.
- Required v1 approval scope: `plan_to_build`.
- Standard/Strict `PLAN-20 -> BUILD-30` requires an approval event or convenience flag such as `--user-approved`.

Blocking:
- `block` and `unblock` are first-class v1 commands.
- Blocked is distinct from skipped or failed.
- Unresolved blockers prevent normal advancement.

## Markdown Artifact Ownership

The CLI should own/update standard markdown artifacts automatically:
- `todos.md`
- `checkpoint.md`
- `artifacts.md`
- `snapshots/<stage>-summary.md`

Use managed sections so human/agent notes are not overwritten:

```markdown
<!-- agentic:managed:start -->
Generated content.
<!-- agentic:managed:end -->

## Notes

Freeform notes live here.
```

Add `agentic note add` in v1:
- appends to unmanaged notes sections,
- records `note_added` in `events.jsonl`,
- does not count as transition evidence unless explicitly added as evidence.

## Command Set for v1

Core lifecycle:
- `agentic init`
- `agentic status`
- `agentic list`
- `agentic use`
- `agentic complete`
- `agentic skip`
- `agentic block`
- `agentic unblock`
- `agentic approve`
- `agentic assert-final`

Evidence/artifacts:
- `agentic run -- <command...>`
- `agentic evidence add`
- `agentic artifact add`
- `agentic note add`
- `agentic export`

Workflow/schema:
- `agentic workflow list`
- `agentic workflow show`
- `agentic workflow validate`
- `agentic schema state`
- `agentic validate`

Doctor/maintenance:
- `agentic doctor`
- `agentic repair` as advanced/experimental

Defer:
- full TUI
- web UI
- watch mode
- agent orchestration
- GitHub PR integration
- commit/push helpers
- custom workflows
- cloud sync

## Command Semantics

- `agentic complete` infers the active stage from `state.current_stage`.
- Optional `--stage` is a safety assertion only; it must match current stage and cannot jump stages.
- `agentic skip` uses the current stage by default and is constrained by workflow-defined skip policy.
- `agentic run --as-evidence` records evidence but does not automatically complete the current stage.
- Add a simple command runner in v1:
  - execute command in repo root,
  - capture exit code/stdout/stderr/timestamps,
  - save full logs under `docs/temp-<id>/artifacts/commands/`,
  - optionally attach log as current-stage evidence.

## Final Assertion and Git Scope

`agentic assert-final` should do both:
- deterministic workflow/state checks,
- passive repo hygiene checks.

State checks include:
- no unresolved blockers,
- required stages completed or skipped with reasons,
- required approvals present,
- evidence exists for required completions,
- acceptance criteria have evidence.

Passive repo checks may include:
- detect repo root and branch,
- show `git status --short`,
- optionally run `git diff --check`,
- warn if task artifacts are not ignored,
- warn if code changed but no validation evidence exists.

Do not run expensive tests automatically unless configured/requested.

Git integration in v1 should be read-only/passive, except explicit `.gitignore` updates:
- no automatic commit,
- no push,
- no PR creation,
- no branch creation,
- no stash/reset/checkout.

## Design Pitfalls

- Do not keep the standalone CLI dependent on `~/.hermes/skills/...`; that keeps it Hermes-native instead of standalone.
- Do not hardcode stage policy in Python when it belongs in workflow definitions.
- Do not let command execution imply stage completion.
- Do not hide user approvals as ordinary evidence; make them explicit events.
- Do not silently mutate `.gitignore` or Git history.
- Do not support arbitrary custom workflows before the `workflow.yaml` schema is stable.
