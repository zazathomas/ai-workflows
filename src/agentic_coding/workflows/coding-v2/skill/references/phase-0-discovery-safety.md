# Phase 0 — Discovery and Safety

## Goal
Understand the repo, protect user work, and identify the smallest safe path before editing.

## Existing Repo Checklist

Run from the working directory when a repo may be involved:

```bash
git rev-parse --show-toplevel
git status --short
git branch --show-current
git diff --name-only
git diff --stat
```

Then:

1. Determine scope: new project, feature, bug fix, refactor, dependency/tooling, docs-only.
2. Record risk: low, medium, high.
3. Identify expected touched files and files explicitly out of scope.
4. Read `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, README, build/package config, and test config as needed.
5. If `docs/index.md` exists, read it first as the navigation map, then verify live paths before editing.
6. If `docs/DESIGN.md` exists and UI is affected, read it before frontend work.
7. Identify exact validation commands: targeted tests, affected-area tests, lint/typecheck/build, browser/API smoke, security/audit tools.

## Business/Product Source of Truth

Before product-model, pricing, tiering, feature-gating, or go-to-market decisions, search `~/`, repo root, and `docs/` for:

```text
*business*plan*  *strategy*  *pricing*  *roadmap*  *PRD*  *DESIGN*
```

Read relevant documents before asking questions or designing behavior. Existing business/strategy docs override plausible assumptions.

## Dirty Worktree Rules

- Do not modify files with pre-existing user changes unless approved.
- Keep an expected touched-file list.
- After each substantial task, inspect `git diff --name-only` and `git diff --stat`.
- Treat unexplained diff expansion as workflow failure.
- Do not run repo-wide formatters unless required by task or convention.
- Generated/lockfile/snapshot changes require justification and generator command identification.

## New Project Checklist

For new projects:

```bash
git init -b main
# if unsupported: git init && git branch -M main
```

Add `.gitignore`, baseline tooling, minimal docs, and only the rigor required by the chosen mode.

## Worktree Isolation

For risky, parallel, or exploratory implementation, prefer a branch or `git worktree` per independent workstream. Do not let multiple subagents edit the same working tree unless file scopes are disjoint.

## Output
Record in todo/plan/final summary:

- Repo root and branch.
- Dirty/clean status and user-owned files.
- Mode, risk, and model tier.
- Expected touched files.
- Validation commands.
- Docs/index/design/business files consulted.
