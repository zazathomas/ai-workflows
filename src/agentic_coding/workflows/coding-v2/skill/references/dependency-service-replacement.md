# Dependency / Service Replacement in Software Projects

Use this reference when a task asks to replace a runtime dependency or backing service, such as Redis → RabbitMQ, local filesystem → S3, SQLite → Postgres, or an in-process queue → external broker.

## Core rule

Separate **repo-scoped dependency replacement** from **host/operator mutation**.

- Repo-scoped changes: manifests, imports, config defaults, env vars, tests, Dockerfiles, compose files, docs, scripts, CI, lockfiles.
- Host/operator changes: uninstalling OS packages, stopping/removing system services, deleting volumes, pruning Docker resources, removing databases, changing global config.

Repo-scoped replacement can proceed under the task's code-change approval. Host/operator mutation is destructive or environment-wide and needs explicit user approval unless the user has already authorized that exact action in the current turn.

## Scan checklist

1. Dependency manifests and lockfiles.
2. App configuration defaults and environment variable names.
3. Runtime startup scripts, systemd/supervisor files, Dockerfiles, Compose/Kubernetes manifests, CI workflows.
4. Code imports/client creation/connection strings.
5. Tests that assert old defaults or mock old clients.
6. README, `.env.example`, docs index, architecture docs, runbooks, troubleshooting notes.
7. Local data/cache directories and ignored runtime artifacts.

## Implementation pattern

1. Keep a compatibility seam where possible: env-driven URL/client settings instead of hard-coded service URLs.
2. Pick a safe default for local development that matches the new supported stack.
3. Update tests before or alongside code so old-service defaults cannot silently survive.
4. Update docs and example env vars in the same slice as code.
5. Validate both config shape and runtime where possible: unit tests, app import, `docker compose config`, image build, then smoke startup if Docker is available.

## Pitfalls

- Do not interpret "remove X" as permission to uninstall host OS packages without saying the scope. Prefer: "I removed X from the project; host package uninstall needs explicit approval."
- Do not leave old service names in docs/scripts after changing code; stale quick-start docs are part of the bug.
- Do not swap only the broker/client library and forget result backend, health checks, workers/beat/schedulers, or delayed task APIs.
- Do not hard-code container hostnames in app code; put them in Compose env vars and keep localhost-friendly defaults for non-container local runs.
