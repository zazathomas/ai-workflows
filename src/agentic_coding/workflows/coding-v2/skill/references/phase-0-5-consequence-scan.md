# Phase 0.5 — Consequence Scan

## Goal
Catch second-order effects before planning: naming collisions, duplicate lifecycle fields, API consumer breakage, hidden fixtures/tests/docs impact, and security or tenant-isolation regressions.

## When Required

Run this scan for changes involving:

- Data models, schemas, migrations, enum/status values, lifecycle states.
- API response/request shapes, DTOs, public interfaces, CLI flags, config names.
- Domain renames or terminology changes.
- Auth/authz, tenant boundaries, payment, file handling, shell execution.
- Dashboard/action queue predicates.
- Shared components/utilities used by multiple consumers.

Skip only for tiny local changes with no consumer or model impact, and record why.

## Procedure

1. Identify 2–3 relevant scan categories.
2. Search for existing names/states/consumers before planning.
3. Document findings under “Potential Conflicts & Assumptions”.
4. Adjust the plan to avoid conflicts or ask the user if the conflict changes product semantics.
5. Do not proceed with unresolved naming/lifecycle/API conflicts.

## Useful Detection Patterns

Use project-appropriate search tools. Examples:

```bash
# Field/name/status consumers
git grep -n "status\|state\|type\|role\|tenant_id\|owner\|viewer"

# Exact old/new terminology
git grep -n "OldTerm\|old-term\|old_term"

# API/DTO/interface consumers
git grep -n "fetch(\|axios\|request(\|Response\|DTO\|interface .*Props"

# Frontend fixtures and tests
git grep -n "mock\|fixture\|getByText\|getByRole\|status:" -- '*test*' '*spec*' '*.tsx' '*.ts'

# File size / complexity hotspots
python3 - <<'PY'
from pathlib import Path
for p in Path('.').rglob('*'):
    if p.is_file() and p.suffix in {'.ts','.tsx','.py','.go','.rs','.js','.jsx'}:
        n=sum(1 for _ in p.open(errors='ignore'))
        if n > 500:
            print(n, p)
PY
```

## Category Prompts

### Data Model / Lifecycle
- Is there already a field with overlapping semantics?
- Are statuses/states exhaustive in backend, frontend, fixtures, dashboards, exports, and tests?
- Do overlap/conflict checks include terminal/cancelled states correctly?

### API / Interface
- Which clients consume this shape?
- Are optional collections defaulted defensively at render boundaries?
- Is this additive or a breaking mutation?
- Are error semantics preserved?

### Auth / Tenant Isolation
- Is this tenant-scoped or platform-scoped?
- Are backend guards the actual boundary, not frontend hiding?
- Does every query include the right tenant/platform predicate?

### UI / Navigation
- Do route/hash IDs, labels, tests, fixtures, and docs all use the new terminology?
- Are semantic links/buttons preserved?
- Are accessibility states and keyboard paths preserved?

### Dependencies / Tooling
- Is a new dependency truly needed?
- Does it have install scripts, suspicious ownership, license issues, or known advisories?
- Does the lockfile change match the intended package operation?

## Output Template

```md
## Potential Conflicts & Assumptions
- Antipattern scan categories:
- Commands/searches run:
- Conflicts found:
- Consumers found:
- Existing conventions to follow:
- Open questions / accepted risks:
- Model tier classification:
```
