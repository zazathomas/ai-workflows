# Stateless JWT Auth Migration Notes

Use this reference when replacing cookie/session authentication with bearer-token JWT auth in a full-stack app.

## Durable lessons

- Treat auth/session-to-JWT as **Strict / Tier 3** work: it crosses authn/authz, tenant isolation, frontend client behavior, CSRF, tests, production config, and audit/security logging.
- Consequence-scan both backend and frontend for: `session`, cookie names, `credentials: "include"`, CSRF header/cookie helpers, logout assumptions, auth test fixtures, tenant headers, invite acceptance, admin login, and role gates.
- With bearer tokens, server logout is usually stateless. Tests and clients must clear the local `Authorization` header / token store after logout; otherwise old tokens remain valid and stale privileged context can accidentally leak into later assertions.
- Login, registration, admin-login, and invite-acceptance endpoints should all be checked for whether they return a token. If a test/client expects the newly authenticated identity immediately after registration/invite acceptance, explicitly install the returned bearer token before the next protected request.
- Frontend API clients should usually switch from cookie behavior (`credentials: "include"` + CSRF cookie/header extraction) to `credentials: "omit"` and `Authorization: Bearer <access_token>` from local token state. Update tests to assert both header presence and token clearing.
- Tenant isolation tests are especially prone to false positives/negatives during migration. Authenticated host/admin endpoints should resolve tenant from the validated JWT/auth context, not from spoofable public tenant headers.
- Documentation drift is common after the code/tests pass. Update README, PRD/spec, architecture, docs index, roadmap/gap-analysis docs, and add an ADR when the auth model changes. Search docs for high-signal stale terms such as cookie/session names, `auth_sessions`, `credentials: "include"`, `x-csrf-token`, `csrf-token`, `session-protected`, `session-authenticated`, `require a session`, `session required`, `session auth/RBAC`, and old auth/session UI wording.

## Verification pattern

1. Add failing tests first for:
   - Login/register return `access_token` and `token_type: "bearer"`.
   - Protected routes reject missing/invalid/expired bearer tokens.
   - Protected routes accept `Authorization: Bearer <token>`.
   - Logout/client token clearing removes access from subsequent requests.
   - Register/invite-acceptance flows switch identity only when their returned token is used.
   - Tenant/role gates still reject spoofed tenant headers and non-owner users.
2. Implement backend token issue/verify helpers and replace cookie/session dependencies.
3. Update frontend API client and tests.
4. Run targeted auth/tenant/production tests before broad suites.
5. For frontend validation, run the focused API-client tests first, then the full frontend suite and production build. If lint fails, separate migration-introduced lint from pre-existing unrelated lint: fix errors in touched auth/client files immediately, rerun focused tests, and report unrelated component lint separately instead of widening the migration diff without user approval.
6. Update docs and ADRs for bearer auth/stateless logout semantics before shipping; historical docs may keep prior-session wording only when clearly labeled as historical/superseded.
7. Finish with diff/security review for leftover cookie/session/CSRF assumptions and accidental secret/token logging.
