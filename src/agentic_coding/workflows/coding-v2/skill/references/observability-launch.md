# Observability and Launch Readiness

## Goal
For production-facing work, define how to know the change works, how to detect failure, and how to roll back safely.

## When to Use

Use for:

- Deployments, public endpoints, auth/payment/data changes.
- Background jobs, webhooks, queues, sync, or integrations.
- Features with reliability, performance, or support impact.
- Strict-mode work that may reach users or production-like systems.

## Define Working Before Instrumenting

Answer:

- What user/system behavior proves success?
- What error or metric proves failure?
- What logs/metrics/traces should exist?
- Who or what needs alerting?
- What is the rollback trigger?

## Signals

Prefer structured signals:

- Logs: request IDs, tenant IDs where safe, operation names, error classes. Avoid secrets/PII.
- Metrics: counts, rates, latency, failures, queue depth, retries.
- Traces: external API calls, DB queries, worker spans, critical path timings.
- Health checks: readiness/liveness and dependency checks.

## Launch Checklist

- [ ] Tests/lint/build pass.
- [ ] Security review complete.
- [ ] Config/secrets documented and not committed.
- [ ] Feature flag/staged rollout considered.
- [ ] Dashboard/log query/runbook or smoke command documented.
- [ ] Rollback trigger and steps documented.
- [ ] Migration rollback/data caveats documented.
- [ ] Post-deploy smoke path defined.

## Rollback Template

```md
## Rollback Plan
- Trigger:
- Steps:
- Data/migration caveats:
- Expected time:
- Verification after rollback:
```

## Output

Include success/failure signals, observability changes, post-launch checks, and rollback notes in the final summary or durable docs.
