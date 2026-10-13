# Source-Driven Development

## Goal
Ground framework/library-specific implementation in authoritative, version-relevant sources instead of stale memory.

## When to Use

Use when correctness depends on current behavior of:

- Frameworks: React, Vite, Next, FastAPI, Django, Rails, etc.
- Auth/payment/cloud SDKs.
- Database/migration tooling.
- Browser/platform APIs.
- Security-sensitive libraries.
- Any package where APIs, recommended patterns, or defaults may have changed.

Skip for pure language logic, local variable renames, or code where version-specific APIs do not matter.

## Process

1. Detect installed version from lockfile/package config/imports.
2. Prefer official docs, package docs, source repo, or in-repo examples.
3. Check migration/deprecation notes for the installed major version.
4. Implement using documented patterns.
5. Cite the source or repo evidence in plan/final summary when it influenced the change.

## Detection Examples

```bash
# JS/TS
node -p "require('./package.json').dependencies?.vite || require('./package.json').devDependencies?.vite"

# Python
python3 - <<'PY'
import importlib.metadata as m
for name in ['fastapi','pydantic','django']:
    try: print(name, m.version(name))
    except m.PackageNotFoundError: pass
PY
```

## Red Flags

- Writing config from memory for a tool with recent major releases.
- Using blog snippets without checking official docs.
- Ignoring installed version and reading docs for latest only.
- Treating TypeScript compile success as proof that bundler/runtime behavior is valid.

## Output

Record:

- Version detected.
- Source/docs checked.
- Pattern chosen.
- Any version caveats.
