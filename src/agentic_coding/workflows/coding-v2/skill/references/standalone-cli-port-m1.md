# Standalone CLI Port: M1 Decisions and Smoke Pattern

Use this when converting Agentic Coding v2 from a Hermes skill/FSM script into a standalone CLI application, or when updating the Hermes skill to consume that CLI.

## Locked product decisions from the M1 design session

- Standalone app is the source of truth; Hermes skill becomes an integration/consumer layer.
- CLI command: `agentic`.
- Repo/distribution/package: `agentic-coding` / `agentic_coding`.
- Python + `uv` for v1.
- Typer for CLI layer; keep core logic framework-independent.
- Pydantic v2 for state/workflow models; JSON Schema export planned after M1.
- Bundled workflow ID: `coding-v2`; display name: `Agentic Coding v2`.
- `agentic init` defaults to `coding-v2`.
- Task state remains repo-local at `docs/temp-<task-id>/` for continuity.
- Task ID format: `temp-<UTC timestamp>-<goal-slug>`.
- Current task pointer: `.agentic/current`.
- Multiple tasks may exist; one current task per repo.
- Treat `docs/temp-*` and `.agentic/current` as ephemeral/gitignored by default; M1 warns only, later versions may add explicit gitignore mutation.
- Append-only event log: `events.jsonl`.
- CLI owns generated markdown artifacts using managed sections and preserves unmanaged notes.
- Include per-task file locking and atomic `state.json` writes from M1.
- Do not add built-in external AI agent spawning in v1; use JSON/state/capsule artifacts as integration surface.
- Direct Hermes integration is a follow-up milestone, not part of standalone CLI M1.

## M1 vertical slice acceptance

M1 is complete only when all are true:

1. `uv run agentic --help` works.
2. `agentic workflow list` and `agentic workflow show coding-v2` work.
3. `agentic init --goal "Test task" --acceptance "Demo criterion"` creates:
   - `docs/temp-<task-id>/state.json`
   - `events.jsonl`
   - `todos.md`
   - `checkpoint.md`
   - `context-capsule.md`
   - `.agentic/current`
4. `agentic status` reads `.agentic/current`.
5. `agentic complete --stage DISC-00 --evidence "Repo discovery completed"` validates the stage assertion, records evidence, appends an event, writes `snapshots/DISC-00-summary.md`, advances to `SCAN-05`, and refreshes markdown artifacts.
6. `agentic status --json` returns stable JSON with `ok`, `command`, `state`, `warnings`, and `errors`.
7. Failure cases are tested: missing evidence and wrong stage assertion.
8. Tests pass with `uv run pytest`.
9. Packaging smoke passes: `uv build`, install built wheel in a temp env, run installed `agentic --help`, `workflow list`, and `init` outside the source tree.

## Implementation notes that mattered

- `importlib.resources.files()` may return a `MultiplexedPath`; call `.joinpath()` one segment at a time for compatibility, e.g. `files(pkg).joinpath(workflow_id).joinpath("workflow.yaml")`.
- With hatchling, package data under the included package may already be included. Avoid duplicate `force-include` entries that add the same workflow files twice to the wheel.
- On minimal Ubuntu/Debian images, `python3 -m venv` may fail if `python3-venv`/`ensurepip` is missing. For packaging smoke in Hermes-style environments, prefer `uv venv` plus `uv pip install --python <venv>/bin/python <wheel>`.
- When the new project directory is not itself a Git repo, do not treat `git status`/`git diff --check` failure as product failure; run smoke tests inside temporary Git repos instead.

## Recommended M1 project skeleton

```text
agentic-coding/
  pyproject.toml
  README.md
  docs/
  src/agentic_coding/
    cli.py
    constants.py
    exit_codes.py
    core/
      artifacts.py
      events.py
      locking.py
      models.py
      paths.py
      repo.py
      responses.py
      state_io.py
      transitions.py
      workflow_loader.py
    workflows/coding-v2/
      workflow.yaml
      stages/*.md
      templates/*.md
  tests/
```

## Post-M1 expansion order

After M1, add commands in this order:

1. `skip`, `block`, `unblock`, `approve`
2. `assert-final`
3. `run -- <command...>` with log artifacts and optional evidence recording
4. `evidence add`, `artifact add`, `note add`
5. `acceptance` and `files` subcommands
6. `next`, `capsule show/refresh`, `export`
7. `schema`, `validate`, `workflow validate`, `migrate`
8. Hermes skill migration to call `agentic` instead of the bundled FSM script
