# Resumable Workflow Hardening

Use this reference when agentic coding work starts skipping stages, losing context mid-run, or becoming hard to resume after compaction, subagent delegation, or long tool output.

## Durable Control Techniques

1. **Externalize state from chat.** Keep `state.json` as the canonical stage pointer and compact source of truth. Chat summaries are advisory only.
2. **Use a single active stage.** Prevent stage bleed by allowing only one active lifecycle stage at a time.
3. **Gate transitions with evidence.** A stage is complete only when its artifact/checklist/evidence exists and `state.json` advances.
4. **Maintain a live ledger.** `todos.md` should show stage ID, owner, status, evidence, and blocker/skip reason for each active unit of work.
5. **Snapshot at boundaries.** Write `snapshots/<stage>-summary.md` at each stage transition so future context can be reconstructed without reading full chat history.
6. **Re-anchor after noisy work.** After subagent returns, large command output, many file edits, or context compaction, re-read `state.json`, `checkpoint.md`, and the active stage card before continuing.
7. **Prefer compact context capsules for delegation.** Give subagents only the scoped goal, acceptance criteria, in/out-of-scope files, decisions, commands, and expected output.
8. **Make skips explicit.** Omission is not a skip. Any skipped stage or task needs a reason in both `todos.md` and `state.json`.
9. **Treat validation as evidence, not intention.** Record exact commands run and results; do not mark validation done from a plan alone.
10. **Use loops deliberately.** Failed verification loops to `BUILD-30`; wrong assumptions loop to `SPEC-10`/`PLAN-20`/`SCAN-05`; review findings loop to the narrowest corrective stage.

## Minimal Pass Sequence for Hardening a Skill

- **Pass 1 — Kernel:** rewrite the main skill into a state-machine/controller-loop kernel with lifecycle IDs and no-hidden-advancement rules.
- **Pass 2 — Artifacts:** add reusable templates for `state.json`, `todos.md`, `checkpoint.md`, `context-capsule.md`, `artifacts.md`, and `stage-summary.md`.
- **Pass 3 — Stage Cards:** split detailed stage behavior into `references/stage-*.md` cards with entry criteria, required actions, exit gates, evidence, and common failure modes.

## Verification Pattern

When updating this skill or a similar staged workflow skill:

- Validate SKILL.md frontmatter starts at byte 0 with `---` and contains `name` and `description`.
- Validate total SKILL.md size is under the Hermes limit.
- Parse JSON templates.
- Confirm every referenced stage card/template exists.
- Scan authored files for accidental placeholder markers such as `[truncated]`.
- Use `skill_view` afterward to confirm the loader can read the skill and linked files.

## Pitfalls

- Adding a longer checklist without a durable state pointer; this makes context loss worse.
- Letting `checkpoint.md`, `todos.md`, and `state.json` diverge.
- Trusting subagent summaries without controller verification.
- Recording one-off session narrative instead of reusable state-machine mechanics.
