# Soft-cancel refactor pattern

Use this reference when a product task asks to replace a destructive operator action (for example, "Delete booking") with a reversible or auditable status transition (for example, "Cancel booking").

## Pattern

1. **Map both semantics before editing.** Identify the existing hard-delete path, the existing soft/status-transition path, and every UI/API consumer. Do not assume the delete endpoint is the right implementation path.
2. **Reuse the status-transition service when it already encodes domain rules.** Keep guest/self-service semantics intact when an existing endpoint serves both public and authenticated callers; split authorization/verification logic carefully rather than duplicating cancellation rules.
3. **Preserve auditability.** Prefer marking the record cancelled/archived over removing it from persistence when the user asks for cancellation semantics.
4. **Honor requested UI placement exactly.** If the user says the action belongs on a detail page rather than a list/admin table, implement the action there and avoid reintroducing destructive controls elsewhere.
5. **Gate by role and state.** Backend authorization should match the acceptance criteria; frontend controls should also disable invalid terminal states such as completed, checked-in, already-cancelled, or already-archived records.
6. **Use explicit confirmation copy.** Confirmation text should say the action keeps the record and changes its status, so operators understand it is not a hard delete.
7. **Refresh both aggregate and detail state after mutation.** After a detail-page cancellation, reload dashboard/list data and the selected detail record so status, buttons, and summaries agree.

## Verification checklist

- Targeted backend tests cover:
  - authorized operator/manager/owner cancellation without public verification fields,
  - public/guest cancellation still requiring its verification field,
  - domain-invalid states still rejected.
- Targeted frontend tests cover:
  - the cancellation action appears in the requested detail/context location,
  - confirmation calls the supplied mutation handler,
  - terminal states disable the action.
- Search for stale destructive UI strings and callbacks, e.g. `Delete <thing>`, `deleteThing`, `onDeleteThing`, and confirm none remain in the operator UI.
- Run the relevant build/typecheck so callback prop changes and status unions are verified.

## Pitfalls

- Do not rename a button from Delete to Cancel while still calling a hard-delete endpoint.
- Do not loosen guest/public cancellation verification while adding authenticated operator cancellation.
- Do not put the action in a convenient table/list if the user explicitly requested detail-page placement.
- Do not remove maintenance/admin hard-delete internals unless the task explicitly asks for API deprecation/removal; a UI refactor can leave backend maintenance primitives in place when out of scope.
