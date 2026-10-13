# Full-stack user-editable personal details

Use this reference when adding or extending "my profile / my details" flows where every signed-in user, including low-privilege roles, can edit their own personal metadata.

## Implementation pattern

1. **Separate self-service details from account administration.** Add/update a self-scoped endpoint such as `PUT /api/auth/me/details` guarded only by normal authentication. Do not reuse owner/manager-only team-management routes for self-edits.
2. **Extend the identity/session shape end-to-end.** Update backend auth/user models, session serialization, frontend session types, and API client methods together so `/auth/me` returns the new fields after login, refresh, and update.
3. **Persist through migrations, not seed-only changes.** Add nullable/default columns or equivalent migration/backfill for existing users. Keep new databases and existing databases on the same schema path.
4. **Constrain writable fields.** The self-service endpoint should accept only personal profile fields (for example first name, last name, phone, address), trim/coerce missing values consistently, and never accept role, tenant, email verification, password, or platform-owner fields through this path.
5. **Expose one obvious all-role UI entry point.** Add a navigation item/page that all signed-in roles can reach, then wire it to the self-service API rather than hiding it behind owner/admin setup screens.
6. **Refresh local session state after save.** Use the endpoint response to replace/update the frontend session so the saved display name/details appear immediately without requiring re-login.
7. **Document the self-service contract.** If a new auth/session endpoint or user-field payload is added, update the repo's README/docs API surface and any architecture/index files that list auth/account routes. Treat this as part of the feature, not optional cleanup.

## Tests to include

- Backend: privileged user can update their own details.
- Backend: low-privilege user (viewer/read-only equivalent) can update their own details even though they cannot manage accounts.
- Backend: `/auth/me` reflects saved details after update.
- Frontend: direct route to the details page renders for a low-privilege session.
- Frontend: form submission calls the self-service endpoint and updates visible session/display data.
- Frontend: fetch/API mocks are route-aware and cover both `GET /auth/me` and the update endpoint response shape.

## Pitfalls

- Invite/acceptance flows often return a new access token but do not automatically attach it to test clients. When testing a newly accepted low-privilege user, update the test client's `Authorization` header from the acceptance response before calling authenticated self-service endpoints.
- Avoid asserting only the happy-path owner/admin role. The whole point of this feature class is that non-admin users can update their own details.
- Do not conflate business/host profile fields with personal user fields unless product requirements explicitly say they are the same object.
