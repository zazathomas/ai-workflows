# API and Interface Design

## Goal
Design stable, predictable contracts that minimize accidental breakage and make consumers easy to reason about.

## When to Use

Use for REST/GraphQL/RPC endpoints, module APIs, CLI flags, config schemas, DTOs, database-facing service contracts, exported types, and component props used across boundaries.

## Principles

1. **Hyrum's Law:** If behavior is observable, some consumer may depend on it.
2. **Contract first:** Define inputs, outputs, errors, and compatibility before implementation.
3. **Prefer additive changes:** Add fields/endpoints before mutating/removing existing ones.
4. **Consistent error semantics:** Preserve status codes/error shapes unless intentionally versioned.
5. **Validate at boundaries:** Reject invalid inputs early with clear errors.
6. **Separate input/output types:** Do not leak internal persistence fields by default.
7. **Predictable naming:** Follow existing domain language; avoid synonyms for existing lifecycle concepts.

## Checklist

- [ ] Request/response shape documented.
- [ ] Existing consumers searched and updated.
- [ ] Error cases tested.
- [ ] Pagination/filtering/sorting semantics explicit for collections.
- [ ] Partial update semantics clear: merge vs replace.
- [ ] Auth/authz and tenant predicates verified.
- [ ] Backward compatibility or versioning addressed.
- [ ] Frontend DTOs, fixtures, tests, and docs updated.

## Red Flags

- Backend tests pass but frontend fixture/app mocks crash.
- Optional arrays are rendered without defensive defaults.
- A delete/archive endpoint has weaker auth than create/update.
- A new status value is added without dashboard/action predicate review.
- A rename updates UI labels but not hash routes, tests, fixtures, docs, or compatibility aliases.

## Output

Record the contract, consumers audited, compatibility impact, and validation evidence.
