# Deprecation and Migration

## Goal
Replace, rename, migrate, or remove old behavior safely without breaking hidden consumers or losing data.

## When to Use

Use when:

- Removing or renaming APIs, fields, routes, statuses, components, configs, or commands.
- Migrating storage/schema/data format.
- Replacing a subsystem with a new implementation.
- Introducing compatibility shims or feature flags.

## Principles

- Code is liability, but removal is a product/API event.
- Build the replacement before removing the old path.
- Prefer compatibility windows for public or multi-consumer contracts.
- Make migration reversible or explicitly document irreversibility.
- Test both old and new paths during transition when both are supported.

## Migration Process

1. Inventory consumers and data.
2. Build replacement path.
3. Add compatibility/adapters if needed.
4. Migrate incrementally.
5. Validate parity and data integrity.
6. Announce/document changed behavior.
7. Remove old path only after criteria are met.
8. Delete zombie code/tests/CSS/docs deliberately.

## Checklist

- [ ] Consumer search completed.
- [ ] Data migration and rollback plan documented.
- [ ] Backward compatibility decision recorded.
- [ ] Tests cover old path, new path, and migration/adapter if applicable.
- [ ] Fixtures/docs/routes/labels updated.
- [ ] Feature flags or staged rollout considered.
- [ ] Dead code removed only after verifying no consumers.

## Red Flags

- Renaming a field without migration or aliases.
- Removing a route because “tests pass” while external clients may depend on it.
- Updating source but leaving stale fixtures or docs that teach future agents the old model.
- Running destructive migrations without explicit approval.

## Output

Record migration steps, compatibility window, rollback notes, and removal criteria.
