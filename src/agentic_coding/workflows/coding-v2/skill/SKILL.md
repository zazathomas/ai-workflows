---
name: agentic-coding-v2
description: "Use when building or modifying software projects through a recoverable staged agentic coding lifecycle with durable state, explicit stage gates, resumable context, delegation handoffs, TDD, review, documentation, and shipping validation."
version: 2.1.0
author: Zaza Thomas + Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [agentic-coding, software-development, staged-workflow, delegation, tdd, security, state-machine, resumable-workflows, review, shipping]
    related_skills: [subagent-driven-development, test-driven-development, writing-plans, requesting-code-review, systematic-debugging, frontend-design, claude-design, web-design-guidelines, design-md, github-pr-workflow]
---

# Agentic Coding v2

## Overview

Agentic Coding v2 is Zaza's recoverable software-engineering workflow for Hermes. It uses a staged lifecycle plus durable task artifacts so long coding runs do not depend on chat memory alone.

The core design is:

- **Workflow kernel:** this `SKILL.md` defines invariants, state, gates, delegation, and final validation.
- **Stage cards:** `references/stage-*.md` files define entry/exit criteria for each stage.
- **Runtime artifacts:** `docs/temp-{id}/state.json`, `todos.md`, `checkpoint.md`, `artifacts.md`, and snapshots preserve context across tool calls, subagents, interruptions, and compaction.

Use the lightest mode that protects correctness, user work, security, and maintainability. Do not blindly run the whole lifecycle for tiny edits; do not skip gates for risky work.

## Lifecycle State Machine

```text
DISC-00 → SCAN-05 → SPEC-10 → PLAN-20 → BUILD-30 → VERIFY-40 → REVIEW-50 → DOC-60 → SHIP-70
```

| Stage ID | Stage | Stage Card | Purpose |
| --- | --- | --- | --- |
| `DISC-00` | Discover / Safety | `references/stage-discovery.md` | Understand repo, task, docs, branch, dirty worktree, commands, and constraints. |
| `SCAN-05` | Consequence Scan | `references/stage-scan.md` | Search impacted models, APIs, fixtures, consumers, tests, migrations, and rules. |
| `SPEC-10` | Specify | `references/stage-specify.md` | Capture acceptance criteria, assumptions, constraints, non-goals, risk, and mode. |
| `PLAN-20` | Plan | `references/stage-plan.md` | Create dependency-ordered tasks, model tiers, touched files, validation, and approval gate. |
| `BUILD-30` | Build | `references/stage-build.md` | Implement one vertical slice at a time using TDD or equivalent regression proof. |
| `VERIFY-40` | Verify | `references/stage-verify.md` | Run tests/build/lint/browser/API checks and gather evidence for acceptance criteria. |
| `REVIEW-50` | Review | `references/stage-review.md` | Review diff, security, API/interface, migration, performance, and acceptance traceability. |
| `DOC-60` | Document | `references/stage-document.md` | Update README/spec/architecture/docs index/ADRs or record why not needed. |
| `SHIP-70` | Ship | `references/stage-ship.md` | Final status, diff checks, optional commit, rollout/rollback notes, and handoff. |

### Allowed Transitions

- Default transition is the next stage in order.
- `BUILD-30` may loop back to `SPEC-10`, `PLAN-20`, or `SCAN-05` when implementation reveals wrong assumptions.
- `VERIFY-40` may loop back to `BUILD-30` on failing validation.
- `REVIEW-50` may loop back to `BUILD-30`, `VERIFY-40`, or `DOC-60` depending on findings.
- `SHIP-70` is allowed only when all required stages are completed, explicitly skipped with reasons, blocked, or user-scoped out.

### No Hidden Advancement

A stage completed only in reasoning does **not** count. A stage counts only when:

1. its exit gate is satisfied,
2. evidence is recorded in `todos.md`, `checkpoint.md`, or a stage artifact,
3. `state.json.completed_stages` includes the stage or the stage is explicitly skipped with reason,
4. `state.json.current_stage` is advanced.

### Standalone CLI Productization

If converting this workflow into a standalone application, follow `references/standalone-cli-productization.md`. The agreed direction is: `agentic` is an automation-first standalone Python/uv CLI; `coding-v2` is the bundled workflow; task state remains under `docs/temp-<task-id>/`; `.agentic/current` selects the current task; Hermes becomes an integration layer that calls the CLI after the core is working.

## Native FSM Runner

Use the bundled Hermes-native runner as the deterministic transition controller whenever runtime artifacts are required:

```bash
python ~/.hermes/skills/software-development/agentic-coding-v2/scripts/agentic_coding_fsm.py --root "$REPO" init \
  --goal "<task goal>" \
  --mode standard \
  --risk medium \
  --tier tier-2-normal \
  --acceptance "<criterion>"

python ~/.hermes/skills/software-development/agentic-coding-v2/scripts/agentic_coding_fsm.py --root "$REPO" status --task-id <task-id>

python ~/.hermes/skills/software-development/agentic-coding-v2/scripts/agentic_coding_fsm.py --root "$REPO" complete \
  --task-id <task-id> \
  --evidence "<real command/file/review evidence>"
```

The runner is the control plane, not the coding agent. It enforces legal stage transitions, writes `state.json`, records `fsm_events`, creates checkpoint/snapshot files, blocks hidden advancement without evidence, requires explicit skip reasons, and requires `--user-approved` before `PLAN-20 -> BUILD-30` for Standard/Strict work.

Every `init`, `complete`, `skip`, `block`, and `assert-final` command must print a brief current-state payload after it writes state. Keep it precise enough to paste into chat or a handoff:

```json
{
  "ok": true,
  "state": {
    "task_id": "temp-...",
    "current_stage": "SCAN-05",
    "stage_name": "Consequence Scan",
    "previous_stage": "DISC-00",
    "transition": "DISC-00->SCAN-05",
    "next_action": "Complete SCAN-05 — Consequence Scan gate.",
    "state_path": ".../docs/temp-.../state.json"
  }
}
```

When using the runner in a coding session, summarize this payload in one short line after each transition, e.g. `FSM: DISC-00 -> SCAN-05; current=SCAN-05 Consequence Scan; next=scan impacted consumers.` Do not paste the full `state.json` unless the user asks or debugging requires it.

Manual edits to `state.json.current_stage`, `completed_stages`, or `skipped_stages` are allowed only to repair a corrupt artifact. Normal stage transitions must go through `scripts/agentic_coding_fsm.py`.

## Mandatory Controller Loop

For every non-trivial task, run this loop. This is the primary anti-context-loss mechanism.

1. **Identify state.** Read existing `docs/temp-{id}/state.json` or initialize artifacts with `scripts/agentic_coding_fsm.py init`.
2. **Set one active stage.** Only one lifecycle stage may be active at a time; the active stage is `state.json.current_stage`.
3. **Load current stage card.** Load only the active `references/stage-*.md` plus narrowly relevant supporting references/skills.
4. **Execute one bounded slice.** Keep the slice small enough to verify before moving on.
5. **Update artifacts.** Update task evidence, decisions, validation, and handoff notes after every stage, major decision, delegated result, or validation run.
6. **Verify exit gate.** Do not advance until the current stage card's exit criteria are met and evidence is recorded.
7. **Transition through the FSM runner.** Use `scripts/agentic_coding_fsm.py complete`, `skip`, or `block`; do not manually advance stages in normal operation.
8. **Report current state briefly.** After every runner transition, emit one precise line: `FSM: <from> -> <to>; current=<stage> <name>; next=<next action>`. For blocks/skips, include the blocker/skip reason in one short phrase.
9. **Checkpoint transition.** Confirm the runner wrote/updated `checkpoint.md` and `snapshots/<stage>-summary.md` before entering the next stage.
10. **Re-anchor after heavy work.** After long tool output, multiple edits, or any subagent result, re-read `state.json` and `checkpoint.md` before continuing.

If the state files and chat context disagree, trust the state files only after checking current repo evidence (`git status`, relevant files, tests). Do not guess.

## Runtime Artifacts

For Standard and Strict work, create `docs/temp-{id}/` and maintain these files. For Lightweight work, create them when the task has multiple steps, more than one tool-heavy phase, or any risk of interruption.

| Artifact | Template | Required For | Purpose |
| --- | --- | --- | --- |
| `state.json` | `templates/state.json` | Standard/Strict; multi-step Lightweight | Canonical current stage, goal, acceptance criteria, blockers, next action, validation state. |
| `todos.md` | `templates/todos.md` | Any multi-step task | Live completion ledger with stage IDs, owner, status, evidence, and blockers. |
| `checkpoint.md` | `templates/checkpoint.md` | Standard/Strict; any resumed task | Compact human/agent resume point. |
| `artifacts.md` | `templates/artifacts.md` | Standard/Strict | Manifest of plans, specs, snapshots, review notes, generated files, and validation evidence. |
| `context-capsule.md` | `templates/context-capsule.md` | Delegation/handoff | Scoped context package for subagents and resume handoffs. |
| `snapshots/<stage>-summary.md` | `templates/stage-summary.md` | Stage boundaries | Compact stage-boundary context to prevent prompt bloat. |

### Artifact Rules

- `state.json` is the authoritative stage pointer.
- `todos.md` is the authoritative task ledger.
- `checkpoint.md` is the first file to read when resuming.
- `artifacts.md` records every important file, command output location, review note, and handoff.
- Skipped stages must appear in `todos.md` and `state.json` with a reason; omission is not a skip.

## Resume Protocol

If interrupted, context is unclear, the conversation grows long, or another agent resumes the task:

1. Read `docs/temp-{id}/state.json`.
2. Read `docs/temp-{id}/checkpoint.md`.
3. Read `docs/temp-{id}/todos.md`.
4. Read `docs/temp-{id}/artifacts.md` if present.
5. Run or inspect `git status --short` for the active repo.
6. Re-read only the active stage card and any referenced stage artifact.
7. Continue from the first incomplete or blocked required item in `todos.md`.
8. Do **not** infer skipped work from memory. If evidence is missing, mark the item incomplete and verify it.

### Context-Compression Resume

When the chat begins with a preserved active task list or a context-compaction handoff, treat it as a resume hint, not as canonical state or approval:

1. Reconcile the preserved chat todo list with `state.json`, `checkpoint.md`, and `todos.md` before doing new work.
2. If the user repeats a preserved task list with no new instruction, continue the current FSM stage only after artifact reconciliation; do not reinterpret the repetition as approval to cross a human gate.
3. If the artifacts say PLAN-20 is blocked on user approval, ask for approval or requested changes instead of advancing to BUILD-30.
4. If chat todos and artifact todos disagree, update the session todo list to mirror verified artifact state, then proceed from the artifact-backed blocker or next action.

## Choose Workflow Mode

| Mode | Use For | Required Rigor |
| --- | --- | --- |
| Lightweight | Small bug fixes, isolated refactors, tests-only/docs/config/tooling, roughly <=3 touched files and no coupled behavior risk | Session todo or `todos.md`, touched-file list, targeted validation, docs only if behavior/setup changed, security review if relevant |
| Standard | Normal feature work or meaningful behavior changes | `state.json`, `todos.md`, checkpoint, requirements/spec or clear acceptance criteria, plan, small tasks, TDD/proof, affected-area validation, docs updates |
| Strict | New apps, major features, auth/authz, secrets, crypto, payments, migrations, multi-tenant data, file handling, public exposure, deployment/IaC, risky multi-agent work | Full artifacts, architecture/trust boundaries, consequence scan, human approval, independent/doubt review, security audit, rollback/observability notes, acceptance traceability |

Risk levels:

- **Low:** docs, tests, local tooling, isolated UI copy, non-prod scripts.
- **Medium:** app behavior, API shape, query logic, dependency changes, significant refactors, user-visible UX.
- **High:** auth, secrets, crypto, payments, migrations, destructive operations, public network exposure, deployment/IaC, multi-tenant data, file upload/download, shell/command execution.

### Lightweight Mode Is Forbidden When

Use Standard or Strict if the task involves:

- auth/authz, secrets, crypto, payments, destructive actions, file upload/download, shell/command execution, or public network exposure,
- database migrations or persistence semantics,
- public API/interface shape, SDK contracts, or external consumers,
- multi-tenant data, permissions, or data isolation,
- production deployment, IaC, observability, or rollback,
- cross-module behavior coupling or more than 3 behavior-coupled files.

Always record mode, risk, and overall model tier in `state.json`, `todos.md`, plan, or final summary.

## Stage Activation and Supporting References

Use stage cards first. Load older phase references only when they are relevant to the active stage. For standalone CLI productization, load `references/standalone-cli-application-design.md` before planning the application boundary, command set, state storage, workflow loader, or packaging.

| Situation | Load / follow |
| --- | --- |
| Existing repo or code change | `references/stage-discovery.md`; optionally `references/phase-0-discovery-safety.md` |
| Data model/API/status/enum/rename/consumer-impact change | `references/stage-scan.md` + `references/phase-0-5-consequence-scan.md` |
| Requirements unclear or product-affecting | `references/stage-specify.md` + `references/phase-1-requirements-spec.md` |
| Need task breakdown, delegation, or multi-file implementation | `references/stage-plan.md` + `references/phase-2-planning-decomposition.md` |
| Delegating a scoped coding task | `templates/context-capsule.md` + `references/delegation-template-v2.md` |
| Writing or changing behavior | `references/stage-build.md` + `references/phase-3-implementation-tdd-delegation.md` + `test-driven-development` |
| Bug/failing test/build/runtime issue | `systematic-debugging` before broad changes |
| Framework/library-specific pattern matters | `references/source-driven-development.md` |
| High-risk/uncertain decision | `references/doubt-driven-review.md` |
| After green tests or generated/bloated code | `references/code-simplification.md` |
| API/module/interface/public contract work | `references/api-interface-design.md` |
| Optional media/array field across backend model, persistence, API, fixtures, and UI | `references/full-stack-optional-media-field.md` |
| User-editable personal details/profile flow available to all signed-in roles | `references/full-stack-user-profile-details.md` |
| Auth/session-to-JWT or stateless-auth migration | `references/stateless-jwt-auth-migration.md` + `references/deprecation-migration.md` |
| Deprecation, migration, or replacing old paths | `references/deprecation-migration.md` |
| Replacing a runtime dependency/backing service (e.g., Redis → RabbitMQ, local → managed service) | `references/dependency-service-replacement.md` |
| Replacing destructive operator UI with cancel/archive/status semantics | `references/soft-cancel-refactor.md` |
| Production-facing feature or deploy | `references/observability-launch.md` |
| Workflow starts skipping stages, losing context, or needing resumability hardening | `references/resumable-workflow-hardening.md` |
| Converting this skill/FSM into a standalone `agentic` CLI application | `references/standalone-cli-productization.md`; M1 decisions/smoke checklist: `references/standalone-cli-port-m1.md` |
| Final docs/index/update pass | `references/stage-document.md` + `references/phase-4-documentation-index.md` |
| Final acceptance/security/diff review | `references/stage-review.md` + `references/phase-5-review-security-acceptance.md` |
| Final acceptance/security/diff review | `references/stage-review.md` + `references/phase-5-review-security-acceptance.md` |
| Commit, release, push, rollout | `references/stage-ship.md` + `references/phase-6-validation-commit-ship.md` |

## Universal Rules

1. **Protect the worktree.** Check repo root, branch, status, and diff before editing. Do not overwrite user changes.
2. **Scan consequences before planning** when a change may collide with existing model fields, statuses, APIs, tests, fixtures, consumers, or business rules.
3. **Clarify success before building.** Ask blocker-first questions only after reading available repo/business docs.
4. **Use staged rigor.** Lightweight tasks can stay light; Strict tasks require gates.
5. **Use source-grounding when versions matter.** Do not write framework/library-specific code from stale memory if official docs or installed versions matter.
6. **Use TDD for behavior.** For bugs, reproduce first. For features, write/update tests before production code when practical.
7. **Build in vertical slices.** Keep every increment compilable, testable, rollback-friendly, and scoped.
8. **Delegate selectively.** Small mechanical tasks can go to cheaper configured models when configured; critical/security-sensitive tasks stay with the controller or best model.
9. **Verify subagent claims yourself.** Subagent summaries are hints, not proof.
10. **Simplify after green.** Remove accidental complexity, dead code, and agent bloat while preserving behavior.
11. **Review before final.** Diff, security, acceptance traceability, and docs must match the change risk.
12. **Commit only when requested or clearly implied. Push only with explicit approval.**

## Human Gates

- After creating an implementation plan for any Standard or Strict work, stop and request explicit user input before `BUILD-30`. Offer clear options: **Approve plan** or **Request changes**.
- If the user requests changes, revise the plan and ask again.
- Lightweight work may proceed without a formal approval gate only when the plan is a short session todo and the task is low risk.
- Auth, security, migrations, multi-file behavior changes, public APIs, and production-facing changes are never lightweight for this rule.
- Pause if acceptance criteria conflict, validation repeatedly fails, diff expands beyond scope, a new dependency/migration/secret/destructive action is needed, or a subagent needs out-of-scope edits.
- Treat hedged approval as not approved for Strict work.

## Model Tier Routing

Assign a model tier to the overall change and every planned task:

- 🟢 **Tier 1 — Mechanical:** Config/doc typos, simple one-file test additions, field renames with no logic change, lockfile updates, formatting. Suitable for cheaper configured models. Bundle related mechanical work.
- 🟡 **Tier 2 — Normal:** Feature work, API changes, queries, extending existing patterns, tests for new functions. Use default/main model.
- 🔴 **Tier 3 — Critical:** Auth/authz, crypto, migrations, destructive operations, data model design, security-sensitive changes, public API contracts. Use best model; delegate only when necessary and verify extra thoroughly.

When changing Hermes delegation routing itself, use `hermes-agent` and validate with a real no-side-effect smoke test plus gateway restart before expecting Discord/Telegram sessions to pick up config changes.

## Delegation Context Capsule

Before delegating, write or paste a context capsule with:

- current stage,
- goal and acceptance criteria,
- exact files/directories in scope,
- files/directories out of scope,
- decisions already made,
- relevant commands and expected validation,
- definition of done,
- required output format.

On return, record the subagent result in `todos.md`, update `state.json.validation` or `blockers`, and independently verify changed files and claimed commands.

## Pre-Final Consistency Check

Before final response:

- [ ] `state.json.current_stage` is `SHIP-70`, or the task is explicitly blocked/deferred/user-scoped out.
- [ ] For FSM-managed tasks, `scripts/agentic_coding_fsm.py assert-final --task-id <task-id> --evidence "<summary>"` passes before claiming completion.
- [ ] Every `todos.md` item is done, blocked, skipped with reason, or explicitly deferred by the user.
- [ ] Every required skipped stage has a reason in `todos.md` and `state.json`.
- [ ] `git status --short` inspected for code repos.
- [ ] `git diff --check` run when code changed.
- [ ] Validation evidence exists for each acceptance criterion, or missing evidence is called out as a blocker.
- [ ] Docs updated or explicitly not needed.
- [ ] If behavior, public API, storage, dependencies, or environment variables changed, inspect and update the repo's setup/config docs before final: README, `.env.example`, architecture/spec/PRD, docs index, and any runbooks that mention the changed path.
- [ ] Final response matches actual state, not intended state.

## Common Pitfalls

1. Treating this skill as a long checklist instead of a state machine.
2. Updating `todos.md` but forgetting `state.json.current_stage`.
3. Bypassing `scripts/agentic_coding_fsm.py` and manually advancing `state.json` without a repair reason.
4. Advancing stages because the chat summary says work is done, without artifact evidence.
5. Applying Strict workflow to tiny edits and wasting time.
6. Self-classifying real behavior/API/auth/migration work as Lightweight.
7. Skipping `SCAN-05` for enum/status/API/rename changes.
8. Planning without reading existing docs/index/design/business documents.
9. Delegating broad vague tasks instead of passing a context capsule.
10. Trusting subagent claims without controller verification.
11. Running repo-wide formatters and creating review noise.
12. Shipping without docs, rollback, or observability notes for production-facing changes.
13. Treating `Docs updated or explicitly not needed` as a mental checkbox. For API/storage/env/dependency changes, explicitly search and update `.env.example`, README setup sections, architecture docs, PRDs/specs, and runbooks before claiming done.
14. Committing or pushing by reflex.
15. For self-service profile/detail features, testing only owner/admin paths. Always include a low-privilege authenticated role and refresh/apply any token returned by invite/acceptance flows before calling the self-service endpoint.
17. For dependency/backing-service replacement tasks, separate repo-scoped removal from host/operator mutation. Remove old clients/config/docs/tests from the project, but do not uninstall OS packages, stop global services, delete volumes, or mutate host state without explicit current-user approval.
18. If the runtime blocks a command with `BLOCKED ... Do NOT retry this command` (approval timed out), treat that as final for the command: stop it, do NOT re-run a rephrased or piped variant to reach the same outcome, and do not attempt the outcome via a different tool. Report the blocker and continue with unblocked work. Long chained commands with inline interpreters (`npx ... | python3 -c ...`, multi-stage `&&` chains) are the usual trigger — prefer single-purpose short commands, especially for FSM runner transitions.
19. In React+TS repos, read `eslint.config.js` during DISC-00. The react-refresh + react-hooks v7 rules are hard gates: keep component-only files separate from hook/util files (`react-refresh/only-export-components`), use type-only imports for types, and reset form state inside submit handlers rather than in effects (`react-hooks/set-state-in-effect`).

## Verification Checklist

- [ ] Workflow mode, risk level, and model tier recorded.
- [ ] Runtime artifacts initialized or intentionally skipped with reason.
- [ ] Current stage loaded from `state.json` or initialized.
- [ ] Discovery safety completed; worktree state understood.
- [ ] Relevant docs and source-grounded references read.
- [ ] Consequence scan completed or intentionally skipped with reason.
- [ ] Requirements/acceptance criteria clarified or assumptions documented.
- [ ] Plan/tasks are small, vertical, dependency-ordered, scoped, and include validation commands.
- [ ] Human approval obtained after Standard/Strict plan and before `BUILD-30`.
- [ ] TDD or equivalent regression proof used for behavior changes.
- [ ] Subagent outputs independently verified by controller.
- [ ] Code simplification pass completed after green tests where useful.
- [ ] Security, API/interface, migration, and observability checks run according to risk.
- [ ] Acceptance criteria traced to implementation and validation evidence.
- [ ] README/spec/architecture/docs index/DESIGN/ADRs updated as needed.
- [ ] Final `git status`, `git diff --stat`, `git diff --check`, and relevant tests/lint/build/security checks completed.
- [ ] `state.json`, `todos.md`, `checkpoint.md`, and snapshots match actual final state.
- [ ] Commit/push behavior matches user intent; push approval requested if needed.
